"""Métricas e análise estatística do LAB05 (canais de atendimento da PBH).

Pergunta principal: para um MESMO serviço, o tempo de encerramento e a proporção
de solicitações encerradas diferem conforme o canal?

Definições (fixadas antes de olhar os resultados; ver FONTE_DA_VERDADE §6 e §9):

* Elegível: registro não inconsistente, de canal comparável (Portal de Serviços,
  PBH APP, Telefone 156, Presencial) e com **seguimento ≥ horizonte** (90 dias):
  só entra quem teve tempo de ser encerrado. Sem isso, solicitações recentes
  pareceriam "abertas" apenas por falta de tempo (censura à direita).
* Taxa de encerramento em H dias = encerradas com tempo ≤ H / elegíveis. Totalmente
  observada para todos os elegíveis (nenhum censurado), é a medida de proporção
  usada nos testes. A taxa "até o corte" (qualquer tempo) é só descritiva.
* Tempo de encerramento = dias entre criação e encerramento, só de encerradas
  (aberta nunca vira 0). Mediana/IQR entre encerradas é condicional a encerrar;
  como verificação, a mediana de Kaplan–Meier trata abertas como censuradas.
* Mesmo serviço = estratificação por ``servico_chave``. Cada serviço entra num
  teste de um par de canais só se as duas células têm ≥ ``min_celula`` registros.
* Testes: proporções por serviço com qui-quadrado (ou Fisher se esperado < 5);
  tempos por serviço com Mann–Whitney; ≥ 3 canais no mesmo serviço, qui-quadrado
  r×2 e Kruskal–Wallis. Estratificado entre serviços: Cochran–Mantel–Haenszel
  (proporções) e van Elteren (tempos). Efeitos: diferença de risco (IC de
  Newcombe), razão de chances, h de Cohen, delta de Cliff (IC por DeLong/Cliff).
  Correção de Holm por família de testes.
* Convenção de sinal: para o par (A, B), delta de Cliff > 0 = A tende a levar MAIS
  tempo que B; diferença de risco > 0 = A encerra MAIS (em H dias) que B.

Nenhum valor é "inventado": tudo vem da base analítica.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import asdict

import numpy as np
import pandas as pd
from scipy import stats

import config as C

Z95 = 1.959963984540054
PARES = list(itertools.combinations(C.CANAIS_COMPARAVEIS, 2))


# ---------------------------------------------------------------------------
# Utilidades estatísticas
# ---------------------------------------------------------------------------

def holm(pvalores) -> np.ndarray:
    """Correção de Holm–Bonferroni (ajusta p-valores; ``nan`` é preservado)."""
    p = np.asarray(pvalores, dtype=float)
    saida = np.full(p.shape, np.nan)
    validos = np.flatnonzero(~np.isnan(p))
    if validos.size == 0:
        return saida
    ordem = validos[np.argsort(p[validos], kind="stable")]
    m = ordem.size
    corrente = 0.0
    for rank, idx in enumerate(ordem):
        corrente = max(corrente, (m - rank) * p[idx])
        saida[idx] = min(1.0, corrente)
    return saida


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Intervalo de Wilson para uma proporção."""
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centro - meia), min(1.0, centro + meia))


def diferenca_newcombe(k1: int, n1: int, k2: int, n2: int, z: float = Z95):
    """Diferença de proporções p1 − p2 com IC híbrido de Newcombe (método 10)."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, z)
    l2, u2 = wilson(k2, n2, z)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), \
        d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


def razao_de_chances(a: int, b: int, c: int, d: int):
    """OR de [[a, b], [c, d]] (a,b = grupo A sucesso/falha; c,d = grupo B) com IC de Woolf.

    Com célula zero aplica a correção de Haldane–Anscombe (+0,5 em todas).
    """
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    lor = math.log(a * d / (b * c))
    ep = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return math.exp(lor), math.exp(lor - Z95 * ep), math.exp(lor + Z95 * ep), lor, ep


def h_cohen(p1: float, p2: float) -> float:
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def magnitude_delta(delta: float) -> str:
    """Classes de Romano et al. (2006) para |delta de Cliff|."""
    a = abs(delta)
    if math.isnan(a):
        return "indefinida"
    return ("desprezível" if a < 0.147 else "pequena" if a < 0.33
            else "média" if a < 0.474 else "grande")


def magnitude_h(h: float) -> str:
    """Classes de Cohen para |h| (0,2 / 0,5 / 0,8)."""
    a = abs(h)
    if math.isnan(a):
        return "indefinida"
    return ("desprezível" if a < 0.2 else "pequena" if a < 0.5
            else "média" if a < 0.8 else "grande")


def cliff(x, y) -> dict:
    """Delta de Cliff de x contra y, Mann–Whitney e variância (DeLong).

    delta = P(X > Y) − P(X < Y). A variância vem dos valores de colocação de
    DeLong (1988), válidos com empates (contam 1/2). O IC usa a fórmula assimétrica
    de Cliff (1996) com esse erro-padrão. ``p_empate`` = P(X = Y).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n1, n2 = x.size, y.size
    xs, ys = np.sort(x), np.sort(y)
    # por elemento de x: quantos y menores / iguais / maiores
    menor_y = np.searchsorted(ys, x, side="left")
    ate_y = np.searchsorted(ys, x, side="right")
    d_i = (menor_y - (n2 - ate_y)) / n2
    # por elemento de y: quantos x maiores / menores (mesmo sinal: x > y positivo)
    menor_x = np.searchsorted(xs, y, side="left")
    ate_x = np.searchsorted(xs, y, side="right")
    d_j = ((n1 - ate_x) - menor_x) / n1
    delta = float(d_i.mean())
    # U de x (contagem de pares x > y, empate = 1/2)
    u1 = float(((menor_y + ate_y) / 2).sum())
    p_empate = float(((ate_y - menor_y) / n2).mean())
    # DeLong: colocações V10_i = (1 + d_i)/2 ; V01_j = (1 + d_j)/2
    if n1 > 1 and n2 > 1:
        var_auc = np.var((1 + d_i) / 2, ddof=1) / n1 + np.var((1 + d_j) / 2, ddof=1) / n2
        s = 2 * math.sqrt(var_auc)  # EP do delta
    else:
        s = float("nan")
    lo, hi = ic_cliff(delta, s)
    return {"n_a": n1, "n_b": n2, "delta": delta, "ep": s, "ic_lo": lo, "ic_hi": hi,
            "u_a": u1, "p_empate": p_empate}


def ic_cliff(delta: float, s: float, z: float = Z95) -> tuple[float, float]:
    """IC de Cliff (1996) para o delta, dado o erro-padrão ``s``."""
    if math.isnan(s):
        return (float("nan"), float("nan"))
    if s == 0 or abs(delta) >= 1:
        return (delta, delta)
    den = 1 - delta ** 2 + (z * s) ** 2
    raiz = z * s * math.sqrt((1 - delta ** 2) ** 2 + (z * s) ** 2)
    return (max(-1.0, (delta - delta ** 3 - raiz) / den),
            min(1.0, (delta - delta ** 3 + raiz) / den))


def mann_whitney(x, y) -> dict:
    """Mann–Whitney bicaudal (assintótico com correção de empates e de continuidade).

    O método exato do scipy não vale com empates; aqui os empates são a regra (muitos
    encerramentos no mesmo dia), portanto sempre assintótico.
    """
    r = stats.mannwhitneyu(x, y, alternative="two-sided", method="asymptotic",
                           use_continuity=True)
    return {"u": float(r.statistic), "p": float(r.pvalue)}


def kruskal_wallis(grupos: list[np.ndarray]) -> dict:
    """Kruskal–Wallis com épsilon² como tamanho de efeito (H·(n+1)/(n²−1))."""
    r = stats.kruskal(*grupos)
    n = sum(len(g) for g in grupos)
    eps2 = float(r.statistic * (n + 1) / (n ** 2 - 1)) if n > 1 else float("nan")
    return {"h": float(r.statistic), "p": float(r.pvalue), "gl": len(grupos) - 1,
            "epsilon2": eps2, "n": int(n)}


def teste_proporcoes(tabela) -> dict:
    """Qui-quadrado (sem correção) ou Fisher exato (2×2 com esperado < 5).

    ``tabela``: linhas = grupos, colunas = (sucesso, falha). Verifica o pressuposto
    de frequências esperadas e escolhe o teste. Cramér V como tamanho de efeito.
    """
    t = np.asarray(tabela, dtype=float)
    n = t.sum()
    if n == 0 or (t.sum(axis=0) == 0).any() or (t.sum(axis=1) == 0).any():
        return {"teste": "degenerado", "p": 1.0, "esperado_min": float("nan"),
                "cramer_v": 0.0, "chi2": 0.0}
    esperado = np.outer(t.sum(axis=1), t.sum(axis=0)) / n
    emin = float(esperado.min())
    if t.shape == (2, 2) and emin < 5:
        p = float(stats.fisher_exact(t.astype(int))[1])
        return {"teste": "fisher", "p": p, "esperado_min": emin,
                "cramer_v": float("nan"), "chi2": float("nan")}
    chi2, p, _, _ = stats.chi2_contingency(t, correction=False)
    v = math.sqrt(chi2 / (n * (min(t.shape) - 1)))
    return {"teste": "qui2", "p": float(p), "esperado_min": emin,
            "cramer_v": float(v), "chi2": float(chi2)}


# ---------------------------------------------------------------------------
# Cochran–Mantel–Haenszel e van Elteren
# ---------------------------------------------------------------------------

def cmh(estratos: list[tuple[int, int, int, int]]) -> dict:
    """CMH sobre tabelas 2×2 [(a, b, c, d)]: A sucesso/falha, B sucesso/falha.

    Devolve OR de Mantel–Haenszel, IC (Robins–Breslow–Greenland), χ² de CMH com
    correção de continuidade e heterogeneidade (Q de Cochran sobre ln OR de Woolf,
    I²). Estratos sem informação (margens zero) contribuem 0, como no método.
    """
    if not estratos:
        return {"k": 0}
    t = np.asarray(estratos, dtype=float)
    a, b, c, d = t.T
    n = a + b + c + d
    r_i, s_i = a * d / n, b * c / n
    p_i, q_i = (a + d) / n, (b + c) / n
    R, S = r_i.sum(), s_i.sum()
    out: dict = {"k": int(len(t)), "n_total": int(n.sum())}
    if R > 0 and S > 0:
        or_mh = R / S
        var = ((p_i * r_i).sum() / (2 * R ** 2)
               + ((p_i * s_i + q_i * r_i).sum()) / (2 * R * S)
               + (q_i * s_i).sum() / (2 * S ** 2))
        ep = math.sqrt(var)
        out.update(or_mh=or_mh, or_ic_lo=or_mh * math.exp(-Z95 * ep),
                   or_ic_hi=or_mh * math.exp(Z95 * ep))
    else:
        out.update(or_mh=float("nan"), or_ic_lo=float("nan"), or_ic_hi=float("nan"))
    e_a = (a + b) * (a + c) / n
    v_a = (a + b) * (c + d) * (a + c) * (b + d) / np.where(n > 1, n ** 2 * (n - 1), np.inf)
    if v_a.sum() > 0:
        chi2 = (max(abs((a - e_a).sum()) - 0.5, 0.0)) ** 2 / v_a.sum()
        out.update(chi2=float(chi2), p=float(stats.chi2.sf(chi2, 1)))
    else:
        out.update(chi2=0.0, p=1.0)
    # heterogeneidade (Woolf)
    lors, pesos = [], []
    for ai, bi, ci, di in t:
        if min(ai, bi, ci, di) == 0:
            ai, bi, ci, di = ai + .5, bi + .5, ci + .5, di + .5
        lors.append(math.log(ai * di / (bi * ci)))
        pesos.append(1 / (1 / ai + 1 / bi + 1 / ci + 1 / di))
    lors, pesos = np.array(lors), np.array(pesos)
    if len(t) > 1:
        media = (pesos * lors).sum() / pesos.sum()
        q = float((pesos * (lors - media) ** 2).sum())
        gl = len(t) - 1
        out.update(q_cochran=q, q_p=float(stats.chi2.sf(q, gl)),
                   i2=float(max(0.0, (q - gl) / q)) if q > 0 else 0.0)
    return out


def van_elteren(estratos: list[tuple[np.ndarray, np.ndarray]]) -> dict:
    """Wilcoxon estratificado de van Elteren (pesos 1/(N_i + 1)), bicaudal.

    z > 0 indica que o grupo A (primeiro de cada par) tende a valores maiores.
    Com um único estrato coincide com o Mann–Whitney assintótico sem correção de
    continuidade.
    """
    t_obs = e_t = v_t = 0.0
    for x, y in estratos:
        n1, n2 = len(x), len(y)
        n = n1 + n2
        if n1 == 0 or n2 == 0 or n < 3:
            continue
        w = 1.0 / (n + 1)
        _, contagens = np.unique(np.concatenate([x, y]), return_counts=True)
        u1 = stats.mannwhitneyu(x, y, method="asymptotic").statistic
        soma_postos_a = u1 + n1 * (n1 + 1) / 2
        var = n1 * n2 / 12 * ((n + 1) - (contagens ** 3 - contagens).sum() / (n * (n - 1)))
        t_obs += w * soma_postos_a
        e_t += w * n1 * (n + 1) / 2
        v_t += w * w * var
    if v_t <= 0:
        return {"z": float("nan"), "p": float("nan")}
    z = (t_obs - e_t) / math.sqrt(v_t)
    return {"z": float(z), "p": float(2 * stats.norm.sf(abs(z)))}


def teste_dos_sinais(n_a: int, n_b: int) -> float:
    """p bicaudal exato (binomial, p = 0,5) para n_a "A" contra n_b "B"; ignora empates."""
    n = n_a + n_b
    if n == 0:
        return float("nan")
    return float(stats.binomtest(n_a, n, 0.5).pvalue)


def km_mediana(tempo_evento: np.ndarray, tempo_censura: np.ndarray) -> float:
    """Mediana de Kaplan–Meier (dias inteiros). ``nan`` se a curva não chega a 0,5.

    ``tempo_evento``: dias até o encerramento (evento). ``tempo_censura``: dias de
    seguimento das solicitações ainda abertas (censuradas). Tempos inteiros ≥ 0.
    """
    ev = np.asarray(tempo_evento, dtype=int)
    ce = np.asarray(tempo_censura, dtype=int)
    if ev.size == 0:
        return float("nan")
    m = int(max(ev.max(), ce.max() if ce.size else 0)) + 1
    d = np.bincount(ev, minlength=m)
    c = np.bincount(ce, minlength=m) if ce.size else np.zeros(m, dtype=int)
    em_risco = (d + c)[::-1].cumsum()[::-1]  # quem ainda estava sob observação em t
    with np.errstate(divide="ignore", invalid="ignore"):
        fator = np.where(em_risco > 0, 1 - d / em_risco, 1.0)
    surv = np.cumprod(fator)
    idx = np.flatnonzero(surv <= 0.5)
    return float(idx[0]) if idx.size else float("nan")


# ---------------------------------------------------------------------------
# Elegibilidade e descritivas
# ---------------------------------------------------------------------------

def selecionar_elegiveis(base: pd.DataFrame, horizonte: int) -> pd.DataFrame:
    """Aplica os critérios de elegibilidade e cria ``encerrada`` e ``encerrada_h``."""
    m = ((base["status_registro"] != C.STATUS_INCONSISTENTE) & base["comparavel"]
         & (base["seguimento_dias"] >= horizonte))
    el = base.loc[m].copy()
    el["encerrada"] = el["status_registro"] == C.STATUS_ENCERRADA
    el["encerrada_h"] = el["encerrada"] & (el["tempo_dias"] <= horizonte)
    return el


def funil_elegibilidade(base: pd.DataFrame, horizonte: int) -> pd.DataFrame:
    """Quantos registros saem em cada filtro (transparência sobre a população)."""
    n0 = len(base)
    sem_inc = base[base["status_registro"] != C.STATUS_INCONSISTENTE]
    comp = sem_inc[sem_inc["comparavel"]]
    mad = comp[comp["seguimento_dias"] >= horizonte]
    linhas = [
        ("Registros na base analítica (sem duplicatas)", n0),
        ("Excluídos: inconsistentes", n0 - len(sem_inc)),
        ("Excluídos: canal não comparável (integração, origem interna, e-mail)",
         len(sem_inc) - len(comp)),
        (f"Excluídos: seguimento < {horizonte} dias (coorte imatura)", len(comp) - len(mad)),
        ("Elegíveis (análise principal)", len(mad)),
    ]
    return pd.DataFrame(linhas, columns=["etapa", "registros"])


def status_por_canal(base: pd.DataFrame) -> pd.DataFrame:
    """Contagem de encerradas, abertas e inconsistentes por canal (base inteira)."""
    t = pd.crosstab(base["canal"], base["status_registro"])
    for col in (C.STATUS_ENCERRADA, C.STATUS_ABERTA, C.STATUS_INCONSISTENTE):
        if col not in t:
            t[col] = 0
    t = t[[C.STATUS_ENCERRADA, C.STATUS_ABERTA, C.STATUS_INCONSISTENTE]]
    t["total"] = t.sum(axis=1)
    t.insert(0, "rotulo", [C.ROTULO_CANAL.get(c, c) for c in t.index])
    return t.reset_index()


def descritiva_canal(el: pd.DataFrame, horizonte: int) -> pd.DataFrame:
    """Métricas por canal (população elegível)."""
    linhas = []
    for canal in C.CANAIS_COMPARAVEIS:
        g = el[el["canal"] == canal]
        n = len(g)
        if n == 0:
            continue
        enc = g[g["encerrada"]]
        k_enc, k_h = int(g["encerrada"].sum()), int(g["encerrada_h"].sum())
        t = enc["tempo_dias"].to_numpy(dtype=float)
        abertas = g.loc[~g["encerrada"], "seguimento_dias"].to_numpy()
        lo, hi = wilson(k_h, n)
        linhas.append({
            "canal": canal, "rotulo": C.ROTULO_CANAL[canal], "solicitacoes": n,
            "encerradas": k_enc, "abertas": n - k_enc,
            "taxa_encerramento_corte": k_enc / n,
            f"taxa_encerramento_{horizonte}d": k_h / n,
            "taxa_ic_lo": lo, "taxa_ic_hi": hi,
            "mediana_dias": float(np.median(t)) if t.size else float("nan"),
            "q1_dias": float(np.percentile(t, 25)) if t.size else float("nan"),
            "q3_dias": float(np.percentile(t, 75)) if t.size else float("nan"),
            "p90_dias": float(np.percentile(t, 90)) if t.size else float("nan"),
            "media_dias": float(t.mean()) if t.size else float("nan"),
            "pct_encerradas_mesmo_dia": float((t == 0).mean()) if t.size else float("nan"),
            "mediana_km_dias": km_mediana(t, abertas),
            "servicos": int(g["servico_chave"].nunique()),
        })
    return pd.DataFrame(linhas)


# ---------------------------------------------------------------------------
# Comparação dentro do mesmo serviço
# ---------------------------------------------------------------------------

def _celulas(el: pd.DataFrame) -> dict:
    """{servico_chave: {canal: dict(n, k_h, k_enc, tempos, servico)}}"""
    celulas: dict = {}
    for (chave, canal), g in el.groupby(["servico_chave", "canal"], observed=True, sort=True):
        celulas.setdefault(chave, {})[canal] = {
            "servico": g["servico"].iloc[0],
            "n": int(len(g)),
            "k_h": int(g["encerrada_h"].sum()),
            "k_enc": int(g["encerrada"].sum()),
            "tempos": g.loc[g["encerrada"], "tempo_dias"].to_numpy(dtype=float),
        }
    return celulas


def tabela_servico_canal(celulas: dict, horizonte: int, min_celula: int) -> pd.DataFrame:
    linhas = []
    for chave, por_canal in celulas.items():
        for canal, c in por_canal.items():
            t = c["tempos"]
            linhas.append({
                "servico_chave": chave, "servico": c["servico"], "canal": canal,
                "solicitacoes": c["n"], "encerradas": c["k_enc"],
                f"taxa_encerramento_{horizonte}d": c["k_h"] / c["n"],
                "mediana_dias": float(np.median(t)) if t.size else float("nan"),
                "celula_valida_proporcao": c["n"] >= min_celula,
                "celula_valida_tempo": t.size >= min_celula,
            })
    return pd.DataFrame(linhas)


def comparar_pares_por_servico(celulas: dict, p: C.Parametros) -> pd.DataFrame:
    """Um teste por (serviço, par de canais): proporção e tempo, com Holm por família."""
    linhas = []
    for chave, por_canal in celulas.items():
        for ca, cb in PARES:
            if ca not in por_canal or cb not in por_canal:
                continue
            a, b = por_canal[ca], por_canal[cb]
            ok_prop = a["n"] >= p.min_celula and b["n"] >= p.min_celula
            ok_tempo = len(a["tempos"]) >= p.min_celula and len(b["tempos"]) >= p.min_celula
            if not (ok_prop or ok_tempo):
                continue
            lin = {"servico_chave": chave, "servico": a["servico"], "canal_a": ca,
                   "canal_b": cb, "n_a": a["n"], "n_b": b["n"]}
            if ok_prop:
                pa, pb = a["k_h"] / a["n"], b["k_h"] / b["n"]
                rd, lo, hi = diferenca_newcombe(a["k_h"], a["n"], b["k_h"], b["n"])
                orr = razao_de_chances(a["k_h"], a["n"] - a["k_h"], b["k_h"], b["n"] - b["k_h"])
                tp = teste_proporcoes([[a["k_h"], a["n"] - a["k_h"]],
                                       [b["k_h"], b["n"] - b["k_h"]]])
                h = h_cohen(pa, pb)
                lin.update(taxa_a=pa, taxa_b=pb, dif_risco_pp=100 * rd,
                           dif_risco_ic_lo_pp=100 * lo, dif_risco_ic_hi_pp=100 * hi,
                           razao_chances=orr[0], rc_ic_lo=orr[1], rc_ic_hi=orr[2],
                           h_cohen=h, h_magnitude=magnitude_h(h),
                           teste_prop=tp["teste"],
                           p_prop=(np.nan if tp["teste"] == "degenerado" else tp["p"]),
                           esperado_min=tp["esperado_min"])
            if ok_tempo:
                cl = cliff(a["tempos"], b["tempos"])
                mw = mann_whitney(a["tempos"], b["tempos"])
                lin.update(encerradas_a=len(a["tempos"]), encerradas_b=len(b["tempos"]),
                           mediana_a=float(np.median(a["tempos"])),
                           mediana_b=float(np.median(b["tempos"])),
                           delta_cliff=cl["delta"], delta_ic_lo=cl["ic_lo"],
                           delta_ic_hi=cl["ic_hi"], delta_magnitude=magnitude_delta(cl["delta"]),
                           p_empate=cl["p_empate"], p_tempo=mw["p"])
            linhas.append(lin)
    df = pd.DataFrame(linhas)
    if df.empty:
        return df
    for col in ("p_prop", "p_tempo"):
        if col not in df:
            df[col] = np.nan
    df["p_prop_holm"] = holm(df["p_prop"])
    df["p_tempo_holm"] = holm(df["p_tempo"])
    df["sig_prop"] = df["p_prop_holm"] < p.alfa
    df["sig_tempo"] = df["p_tempo_holm"] < p.alfa
    return df


def omnibus_por_servico(celulas: dict, p: C.Parametros) -> pd.DataFrame:
    """Serviços com ≥ 3 canais válidos: qui-quadrado r×2 e Kruskal–Wallis, com Holm."""
    linhas = []
    for chave, por_canal in celulas.items():
        canais_prop = [c for c in C.CANAIS_COMPARAVEIS
                       if c in por_canal and por_canal[c]["n"] >= p.min_celula]
        canais_tempo = [c for c in C.CANAIS_COMPARAVEIS
                        if c in por_canal and len(por_canal[c]["tempos"]) >= p.min_celula]
        if len(canais_prop) < 3 and len(canais_tempo) < 3:
            continue
        lin = {"servico_chave": chave,
               "servico": next(iter(por_canal.values()))["servico"]}
        if len(canais_prop) >= 3:
            tab = [[por_canal[c]["k_h"], por_canal[c]["n"] - por_canal[c]["k_h"]]
                   for c in canais_prop]
            r = teste_proporcoes(tab)
            lin.update(canais_prop=",".join(canais_prop),
                       p_prop=(np.nan if r["teste"] == "degenerado" else r["p"]),
                       cramer_v=r["cramer_v"], esperado_min=r["esperado_min"])
        if len(canais_tempo) >= 3:
            r = kruskal_wallis([por_canal[c]["tempos"] for c in canais_tempo])
            lin.update(canais_tempo=",".join(canais_tempo), kw_h=r["h"], p_tempo=r["p"],
                       epsilon2=r["epsilon2"])
        linhas.append(lin)
    df = pd.DataFrame(linhas)
    if df.empty:
        return df
    for col in ("p_prop", "p_tempo"):
        if col not in df:
            df[col] = np.nan
    df["p_prop_holm"] = holm(df["p_prop"])
    df["p_tempo_holm"] = holm(df["p_tempo"])
    return df


def comparacao_ingenua(el: pd.DataFrame, horizonte: int) -> dict:
    """Comparação global SEM controlar o serviço (mostra o viés de composição)."""
    out: dict = {}
    tab = [[int(g["encerrada_h"].sum()), int((~g["encerrada_h"]).sum())]
           for _, g in el.groupby("canal", observed=True) if len(g)]
    canais = [c for c in C.CANAIS_COMPARAVEIS if (el["canal"] == c).any()]
    out["proporcao"] = {**teste_proporcoes(tab), "canais": canais}
    grupos = [el.loc[(el["canal"] == c) & el["encerrada"], "tempo_dias"].to_numpy()
              for c in canais]
    out["tempo"] = {**kruskal_wallis([g for g in grupos if len(g)]), "canais": canais}
    return out


def _estratificar_proporcao(celulas: dict, ca: str, cb: str, min_celula: int):
    est, chaves = [], []
    for chave, por_canal in celulas.items():
        if ca in por_canal and cb in por_canal:
            a, b = por_canal[ca], por_canal[cb]
            if a["n"] >= min_celula and b["n"] >= min_celula:
                est.append((a["k_h"], a["n"] - a["k_h"], b["k_h"], b["n"] - b["k_h"]))
                chaves.append(chave)
    return est, chaves


def estratificado_por_par(celulas: dict, p: C.Parametros) -> pd.DataFrame:
    """Compara cada par de canais ajustando por serviço (estratos = serviços)."""
    linhas = []
    for ca, cb in PARES:
        lin = {"canal_a": ca, "canal_b": cb}
        # --- proporção: CMH + consistência entre serviços
        est, _ = _estratificar_proporcao(celulas, ca, cb, p.min_celula)
        lin["servicos_prop"] = len(est)
        if est:
            r = cmh(est)
            rds = [e[0] / (e[0] + e[1]) - e[2] / (e[2] + e[3]) for e in est]
            a_maior = sum(x > 0 for x in rds)
            b_maior = sum(x < 0 for x in rds)
            lin.update(
                solicitacoes_prop=r["n_total"], or_mh=r.get("or_mh"),
                or_ic_lo=r.get("or_ic_lo"), or_ic_hi=r.get("or_ic_hi"),
                cmh_chi2=r.get("chi2"), p_cmh=r.get("p"),
                heterogeneidade_q=r.get("q_cochran"), heterogeneidade_i2=r.get("i2"),
                mediana_dif_risco_pp=100 * float(np.median(rds)),
                servicos_a_encerra_mais=a_maior, servicos_b_encerra_mais=b_maior,
                p_sinais_prop=teste_dos_sinais(a_maior, b_maior))
        # --- tempo: delta combinado + van Elteren + consistência
        pares_t, deltas, vars_, pesos = [], [], [], []
        for chave, por_canal in celulas.items():
            if ca in por_canal and cb in por_canal:
                x, y = por_canal[ca]["tempos"], por_canal[cb]["tempos"]
                if len(x) >= p.min_celula and len(y) >= p.min_celula:
                    cl = cliff(x, y)
                    pares_t.append((x, y))
                    deltas.append(cl["delta"])
                    vars_.append(cl["ep"] ** 2)
                    pesos.append(len(x) * len(y))
        lin["servicos_tempo"] = len(pares_t)
        if pares_t:
            w = np.array(pesos, dtype=float)
            d = np.array(deltas)
            pooled = float((w * d).sum() / w.sum())
            ep = math.sqrt(float((w ** 2 * np.array(vars_)).sum()) / w.sum() ** 2)
            lo, hi = ic_cliff(pooled, ep)
            ve = van_elteren(pares_t)
            a_lento = int((d > 0).sum())
            b_lento = int((d < 0).sum())
            lin.update(delta_combinado=pooled, delta_ic_lo=lo, delta_ic_hi=hi,
                       delta_magnitude=magnitude_delta(pooled),
                       van_elteren_z=ve["z"], p_van_elteren=ve["p"],
                       mediana_delta_servicos=float(np.median(d)),
                       servicos_a_mais_lento=a_lento, servicos_b_mais_lento=b_lento,
                       p_sinais_tempo=teste_dos_sinais(a_lento, b_lento))
        linhas.append(lin)
    df = pd.DataFrame(linhas)
    for col in ("p_cmh", "p_van_elteren", "p_sinais_prop", "p_sinais_tempo"):
        if col not in df:
            df[col] = np.nan
        df[col + "_holm"] = holm(df[col])
    return df


def ranking_servicos(pares: pd.DataFrame, top: int) -> dict[str, pd.DataFrame]:
    """Serviços com maior diferença entre canais (maior |delta| e maior |dif. de risco|)."""
    if pares.empty:
        return {"tempo": pd.DataFrame(), "proporcao": pd.DataFrame()}
    out = {}
    if "delta_cliff" in pares:
        t = pares.dropna(subset=["delta_cliff"]).copy()
        t["abs_delta"] = t["delta_cliff"].abs()
        out["tempo"] = (t.sort_values("abs_delta", ascending=False)
                        .drop_duplicates("servico_chave").head(top)
                        [["servico", "canal_a", "canal_b", "n_a", "n_b", "mediana_a",
                          "mediana_b", "delta_cliff", "delta_ic_lo", "delta_ic_hi",
                          "delta_magnitude", "p_tempo_holm"]])
    if "dif_risco_pp" in pares:
        r = pares.dropna(subset=["dif_risco_pp"]).copy()
        r["abs_dif"] = r["dif_risco_pp"].abs()
        out["proporcao"] = (r.sort_values("abs_dif", ascending=False)
                            .drop_duplicates("servico_chave").head(top)
                            [["servico", "canal_a", "canal_b", "n_a", "n_b", "taxa_a",
                              "taxa_b", "dif_risco_pp", "dif_risco_ic_lo_pp",
                              "dif_risco_ic_hi_pp", "h_magnitude", "p_prop_holm"]])
    return out


def sensibilidade_horizonte(base: pd.DataFrame, p: C.Parametros) -> pd.DataFrame:
    """Repete a parte de proporção (CMH por par) com outros horizontes."""
    linhas = []
    for h in p.horizontes_sensibilidade:
        el = selecionar_elegiveis(base, h)
        cel = _celulas(el)
        for ca, cb in PARES:
            est, _ = _estratificar_proporcao(cel, ca, cb, p.min_celula)
            if not est:
                continue
            r = cmh(est)
            linhas.append({"horizonte_dias": h, "canal_a": ca, "canal_b": cb,
                           "servicos": len(est), "or_mh": r.get("or_mh"),
                           "or_ic_lo": r.get("or_ic_lo"), "or_ic_hi": r.get("or_ic_hi"),
                           "p_cmh": r.get("p")})
    return pd.DataFrame(linhas)


# ---------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------

def analisar(base: pd.DataFrame, p: C.Parametros | None = None) -> dict:
    """Executa toda a análise. Devolve DataFrames e um resumo serializável."""
    p = p or C.Parametros()
    el = selecionar_elegiveis(base, p.horizonte_dias)
    if el.empty:
        raise ValueError("Nenhuma solicitação elegível (verifique horizonte e base).")
    celulas = _celulas(el)
    por_canal = descritiva_canal(el, p.horizonte_dias)
    pares = comparar_pares_por_servico(celulas, p)
    omni = omnibus_por_servico(celulas, p)
    estrat = estratificado_por_par(celulas, p)
    ingenua = comparacao_ingenua(el, p.horizonte_dias)
    rank = ranking_servicos(pares, p.top_servicos)
    sens = sensibilidade_horizonte(base, p)

    pressupostos = {
        "testes_proporcao_por_servico": (
            pares["teste_prop"].value_counts().to_dict() if "teste_prop" in pares else {}),
        "empates_tempo_mediana_p_empate": (
            float(pares["p_empate"].median()) if "p_empate" in pares and len(pares) else None),
        "empates_tempo_maximo_p_empate": (
            float(pares["p_empate"].max()) if "p_empate" in pares and len(pares) else None),
        "independencia": "não verificável: a base não tem identificador do cidadão; "
                         "o mesmo cidadão pode gerar várias solicitações",
    }
    return {
        "parametros": asdict(p),
        "elegiveis": el,
        "funil": funil_elegibilidade(base, p.horizonte_dias),
        "status_por_canal": status_por_canal(base),
        "por_canal": por_canal,
        "servico_canal": tabela_servico_canal(celulas, p.horizonte_dias, p.min_celula),
        "pares_por_servico": pares,
        "omnibus_por_servico": omni,
        "estratificado_por_par": estrat,
        "comparacao_ingenua": ingenua,
        "ranking_servicos": rank,
        "sensibilidade_horizonte": sens,
        "pressupostos": pressupostos,
        "celulas": celulas,
    }
