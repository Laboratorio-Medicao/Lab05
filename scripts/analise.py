"""Análise estatística do LAB05 (issue #25): descritiva, testes e tamanho do efeito.

Implementa o plano de análise da PROPOSTA §7 e da FONTE_DA_VERDADE §9.
Até a coleta só existem dados SINTÉTICOS: nada que este script produza hoje é
resultado (FONTE_DA_VERDADE §2.3 e §17).

Definições fixadas antes da coleta (não escolher teste pelo resultado):

- Diferença sempre celular − computador, por participante.
- d_z = média(dif) / DP(dif, ddof=1).
- RQ1: y = tarefas concluídas (0–3). Wilcoxon pareado
  (``zero_method="wilcox"``, ``method="approx"``: o exato com empates diverge).
  r de postos = Z / √n_nz, com n_nz = pares com dif ≠ 0 e o sinal de
  (T+ − T−); correlação rank-biserial como complemento. IC 95% da diferença
  da taxa (concluídas/3) por bootstrap de participantes, B = 10.000.
- RQ2: média de ln(tempo_s) das 3 tarefas por participante e dispositivo
  (teto 300 s; abandono/ajuda conforme o parâmetro P1). t pareado, d_z,
  razão das médias geométricas = exp(média dif), IC = exp(IC do t).
- RQ3: SUS do item (ímpares x−1, pares 5−x, soma × 2,5). t pareado, d_z.
- Holm só sobre os 3 p-valores primários (implementado à mão: statsmodels
  não está instalado no ambiente).
- RQ4: exploratória, fora do Holm, p sem ajuste; participante como unidade.
- Checagem de ordem: descritiva, fora do Holm, poder baixo e não calculado.

Parâmetros pendentes do professor:
- P1 (tempo de abandono/ajuda antes de 300 s): ``p1`` em VARIANTES_P1.
- P2 (regra de fechamento): ``p2`` em VARIANTES_P2.
A opção primária fica marcada "PENDENTE (P1/P2)"; as demais saem como
sensibilidade, rotuladas, para não abrir escolha depois de ver os dados.

Uso::

    python scripts/analise.py dados/sinteticos --saida <pasta temporária>
    python scripts/analise.py dados/brutos          # saída em resultados/
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))

import esquema as E  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
B_BOOTSTRAP = 10_000
N_SORTEIOS_PERMUTACAO = 20_000
EXATO_ATE = 16  # n ≤ 16 → permutação exata (2^16 = 65.536 combinações)

VARIANTES_P1 = {
    "teto_300": "abandono/ajuda antes de 300 s recebem tempo 300 s (tratados como falha no teto)",
    "tempo_registrado": "abandono/ajuda mantêm o tempo registrado",
    "excluir_tarefa": "abandono/ajuda saem da média do log do participante",
}
VARIANTES_P2 = {
    "p2_provisoria": "k = min(8, menor n analisável entre as sequências); os k primeiros "
                     "analisáveis de cada sequência, por ordem de realização",
    "todos_analisaveis": "todos os válidos fora do piloto (inclui excedentes)",
    "blocos_completos_por_id": "só blocos cujo número tem as 4 sequências analisáveis",
}
P1_PRIMARIA = "teto_300"
P2_PRIMARIA = "p2_provisoria"
STATUS_P1 = "PENDENTE (P1): opção provisória, sem decisão do professor"
STATUS_P2 = "PENDENTE (P2): regra provisória, sem aprovação do professor"
AVISO_SINTETICO = "DADOS SINTÉTICOS — nada aqui é resultado (FONTE_DA_VERDADE §2.3)."


# ---------------------------------------------------------------------------
# Estatísticas básicas (funções puras)
# ---------------------------------------------------------------------------

def d_z(dif) -> float:
    """Tamanho do efeito pareado: média(dif) / DP(dif, ddof=1)."""
    dif = np.asarray(dif, float)
    if len(dif) < 2:
        return float("nan")
    dp = dif.std(ddof=1)
    return float(dif.mean() / dp) if dp > 0 else float("nan")


def holm(pvalores) -> list[float]:
    """Correção de Holm (step-down), com monotonicidade e teto em 1.

    >>> holm([0.01, 0.04, 0.03])
    [0.03, 0.06, 0.06]
    """
    p = np.asarray(pvalores, float)
    m = len(p)
    ordem = np.argsort(p, kind="stable")
    ajust = np.empty(m)
    acumulado = 0.0
    for rank, i in enumerate(ordem):
        acumulado = max(acumulado, (m - rank) * p[i])
        ajust[i] = min(1.0, acumulado)
    return [round(float(x), 12) for x in ajust]


def wilcoxon_pareado(dif) -> dict:
    """Wilcoxon pareado (zero_method="wilcox", method="approx") com r e rank-biserial.

    r = Z / √n_nz, Z com o sinal de (T+ − T−). Se todas as diferenças forem
    nulas o teste é indefinido; p é reportado como 1,0 com nota.
    """
    dif = np.asarray(dif, float)
    nz = dif[dif != 0]
    out = {"n": int(len(dif)), "n_nz": int(len(nz)), "n_zeros": int(len(dif) - len(nz))}
    if len(nz) == 0:
        out.update(T=float("nan"), z=float("nan"), p=1.0, r=float("nan"),
                   rank_biserial=float("nan"),
                   nota="todas as diferenças são nulas: teste indefinido, p = 1")
        return out
    postos = stats.rankdata(np.abs(nz))
    t_mais = float(postos[nz > 0].sum())
    t_menos = float(postos[nz < 0].sum())
    res = stats.wilcoxon(dif, zero_method="wilcox", method="approx")
    sinal = np.sign(t_mais - t_menos)
    z = float(abs(res.zstatistic) * sinal)
    out.update(T=float(res.statistic), T_mais=t_mais, T_menos=t_menos, z=z,
               p=float(res.pvalue), r=z / math.sqrt(len(nz)),
               rank_biserial=(t_mais - t_menos) / (t_mais + t_menos))
    return out


def t_pareado(dif) -> dict:
    """t pareado sobre as diferenças (equivale a t de uma amostra contra 0)."""
    dif = np.asarray(dif, float)
    res = stats.ttest_1samp(dif, 0.0)
    ic = res.confidence_interval(0.95)
    return {"n": int(len(dif)), "media_dif": float(dif.mean()),
            "dp_dif": float(dif.std(ddof=1)), "t": float(res.statistic),
            "gl": int(res.df), "p": float(res.pvalue),
            "ic95": [float(ic.low), float(ic.high)], "d_z": d_z(dif)}


def bootstrap_media(x, b: int = B_BOOTSTRAP, semente: int = E.SEMENTE) -> list[float]:
    """IC 95% percentil da média por reamostragem das unidades (participantes)."""
    x = np.asarray(x, float)
    if len(x) == 0:
        return [float("nan"), float("nan")]
    rng = np.random.default_rng(semente)
    medias = x[rng.integers(0, len(x), size=(b, len(x)))].mean(axis=1)
    return [float(np.percentile(medias, 2.5)), float(np.percentile(medias, 97.5))]


def permutacao_sinais(d, n_sorteios: int = N_SORTEIOS_PERMUTACAO,
                      semente: int = E.SEMENTE, exato_ate: int = EXATO_ATE) -> dict:
    """Teste de permutação por inversão de sinais sobre a média (bicaudal).

    Exato (todas as 2^n combinações) se n ≤ ``exato_ate``; senão Monte Carlo
    com ``n_sorteios`` e p = (k + 1) / (B + 1).
    """
    d = np.asarray(d, float)
    n = len(d)
    if n == 0:
        return {"n": 0, "p": float("nan"), "metodo": "indefinido"}
    obs = abs(d.mean())
    eps = 1e-12
    if n <= exato_ate:
        bits = (np.arange(2 ** n)[:, None] >> np.arange(n)) & 1
        medias = ((1 - 2 * bits) * d).mean(axis=1)
        p = float(np.mean(np.abs(medias) >= obs - eps))
        return {"n": n, "p": p, "metodo": f"exato ({2 ** n} combinações)"}
    rng = np.random.default_rng(semente)
    sinais = rng.choice([-1.0, 1.0], size=(n_sorteios, n))
    medias = (sinais * d).mean(axis=1)
    k = int(np.sum(np.abs(medias) >= obs - eps))
    return {"n": n, "p": (k + 1) / (n_sorteios + 1),
            "metodo": f"Monte Carlo ({n_sorteios} sorteios, semente {semente})"}


def escore_sus(itens) -> np.ndarray:
    """Escore SUS (0–100). ``itens``: matriz n × 10 com respostas 1–5.

    Ímpares contribuem x − 1; pares, 5 − x; soma × 2,5.
    """
    x = np.asarray(itens, float)
    if x.ndim == 1:
        x = x[None, :]
    impares = x[:, 0::2] - 1
    pares = 5 - x[:, 1::2]
    return (impares.sum(axis=1) + pares.sum(axis=1)) * 2.5


def descrever(x) -> dict:
    x = pd.Series(np.asarray(x, float)).dropna()
    if x.empty:
        return {"n": 0}
    return {"n": int(len(x)), "media": float(x.mean()),
            "dp": float(x.std(ddof=1)) if len(x) > 1 else float("nan"),
            "mediana": float(x.median()), "q1": float(x.quantile(.25)),
            "q3": float(x.quantile(.75)), "iqr": float(x.quantile(.75) - x.quantile(.25)),
            "min": float(x.min()), "max": float(x.max())}


# ---------------------------------------------------------------------------
# Seleção da amostra (P2)
# ---------------------------------------------------------------------------

def analisaveis(participantes: pd.DataFrame) -> pd.DataFrame:
    return participantes[participantes["valida"] & ~participantes["piloto"]]


def selecionar_amostra(participantes: pd.DataFrame, regra: str = P2_PRIMARIA,
                       meta: int = E.META_POR_SEQUENCIA) -> dict:
    """Seleciona os participantes da análise conforme a variante de P2.

    Devolve ``{"ids": [...], "k": k, "fora": {id: motivo}}``.
    """
    if regra not in VARIANTES_P2:
        raise ValueError(f"regra P2 desconhecida: {regra}")
    ok = analisaveis(participantes).sort_values("ordem_realizacao")
    fora = {}
    for _, lin in participantes.iterrows():
        if lin["piloto"]:
            fora[lin["participante"]] = "piloto"
        elif not lin["valida"]:
            fora[lin["participante"]] = "sessão inválida"
    if regra == "todos_analisaveis":
        return {"ids": list(ok["participante"]), "k": None, "fora": fora}
    if regra == "blocos_completos_por_id":
        n_seq = ok.groupby("bloco")["sequencia"].nunique()
        completos = set(n_seq[n_seq == 4].index)
        sel = ok[ok["bloco"].isin(completos)]
        # dentro de um bloco completo, um único participante por sequência
        sel = sel.groupby(["bloco", "sequencia"], group_keys=False).head(1)
        for pid in set(ok["participante"]) - set(sel["participante"]):
            fora[pid] = "bloco incompleto ou repetido"
        return {"ids": list(sel["participante"]), "k": len(completos), "fora": fora}
    cont = ok.groupby("sequencia").size().reindex([1, 2, 3, 4], fill_value=0)
    k = int(min(meta, cont.min()))
    sel = ok.groupby("sequencia", group_keys=False).head(k)
    for pid in set(ok["participante"]) - set(sel["participante"]):
        fora[pid] = (f"excedente (além dos {k} primeiros da sequência; "
                     "arquivado e descrito, fora da análise primária)")
    return {"ids": list(sel["participante"]), "k": k, "fora": fora}


# ---------------------------------------------------------------------------
# Pares por participante
# ---------------------------------------------------------------------------

def _pares(df: pd.DataFrame, valor: str) -> pd.DataFrame:
    """Tabela participante × {celular, computador, dif} (dif = celular − computador)."""
    w = df.pivot(index="participante", columns="dispositivo", values=valor)
    w = w.reindex(columns=list(E.DISPOSITIVOS))
    w["dif"] = w["celular"] - w["computador"]
    return w


def tabela_rq1(sessoes: pd.DataFrame, ids) -> pd.DataFrame:
    s = sessoes[sessoes["participante"].isin(ids)]
    y = s.groupby(["participante", "dispositivo"], as_index=False)["concluida"].sum()
    return _pares(y, "concluida")


def tempo_tratado(sessoes: pd.DataFrame, p1: str) -> pd.DataFrame:
    """Aplica a variante de P1 ao tempo das tarefas abandonadas/com ajuda."""
    if p1 not in VARIANTES_P1:
        raise ValueError(f"variante P1 desconhecida: {p1}")
    s = sessoes.copy()
    afetada = s["motivo_fim"].isin(["abandono", "ajuda"])
    if p1 == "teto_300":
        s.loc[afetada, "tempo_s"] = E.TETO_S
    elif p1 == "excluir_tarefa":
        s = s[~afetada]
    return s


def tabela_rq2(sessoes: pd.DataFrame, ids, p1: str = P1_PRIMARIA,
               so_concluidas: bool = False) -> pd.DataFrame:
    s = tempo_tratado(sessoes[sessoes["participante"].isin(ids)], p1)
    if so_concluidas:
        s = s[s["concluida"]]
    s = s.assign(log_t=np.log(s["tempo_s"]))
    m = s.groupby(["participante", "dispositivo"], as_index=False)["log_t"].mean()
    w = _pares(m, "log_t").reindex(list(ids))
    return w


def tabela_rq3(sus: pd.DataFrame, ids) -> pd.DataFrame:
    u = sus[sus["participante"].isin(ids)].copy()
    u["sus"] = escore_sus(u[[f"item_{i}" for i in range(1, 11)]].to_numpy())
    return _pares(u, "sus")


# ---------------------------------------------------------------------------
# RQ1–RQ3
# ---------------------------------------------------------------------------

def analisar_rq1(sessoes, ids, semente=E.SEMENTE) -> dict:
    w = tabela_rq1(sessoes, ids)
    taxa_dif = w["dif"] / E.N_TAREFAS_POR_DISPOSITIVO
    dist = {d: {str(k): int(v) for k, v in w[d].value_counts().reindex(range(4), fill_value=0).items()}
            for d in E.DISPOSITIVOS}
    return {
        "teste": "Wilcoxon pareado (zero_method='wilcox', method='approx')",
        "primario": wilcoxon_pareado(w["dif"]),
        "descritiva": {d: {**descrever(w[d]), "taxa_pct": float(100 * w[d].mean() / 3),
                           "distribuicao_0a3": dist[d]} for d in E.DISPOSITIVOS},
        "dif_taxa_media": float(taxa_dif.mean()),
        "dif_taxa_ic95_bootstrap": bootstrap_media(taxa_dif, semente=semente),
        "_tabela": w,
    }


def analisar_rq2(sessoes, ids, p1=P1_PRIMARIA) -> dict:
    w = tabela_rq2(sessoes, ids, p1)
    t = t_pareado(w["dif"].dropna())
    so = tabela_rq2(sessoes, ids, p1, so_concluidas=True)
    so_ok = so.dropna()
    s = sessoes[sessoes["participante"].isin(ids)]
    teto = s.assign(no_teto=s["motivo_fim"] == "teto").groupby("dispositivo")["no_teto"]
    geo = np.exp(w[list(E.DISPOSITIVOS)])
    return {
        "teste": "t pareado na diferença das médias de ln(tempo)",
        "p1": {"variante": p1, "descricao": VARIANTES_P1[p1], "status": STATUS_P1},
        "primario": t,
        "razao_medias_geometricas": float(np.exp(t["media_dif"])),
        "razao_ic95": [float(np.exp(t["ic95"][0])), float(np.exp(t["ic95"][1]))],
        "nota_razao": "razão das médias geométricas COM teto de 300 s; não é razão "
                      "de médias aritméticas nem se converte em segundos/horas",
        "sensibilidade": {
            "wilcoxon_pareado": wilcoxon_pareado(w["dif"].dropna()),
            "so_concluidas": {
                **(t_pareado(so_ok["dif"]) if len(so_ok) > 1 else {"n": len(so_ok)}),
                "participantes_excluidos": int(len(so) - len(so_ok)),
                "nota": "viés de seleção: exclui quem não concluiu nenhuma tarefa "
                        "em algum dispositivo",
            },
        },
        "descritiva": {
            "media_geometrica_por_participante_s": {d: descrever(geo[d]) for d in E.DISPOSITIVOS},
            "tempo_tarefa_s": {d: descrever(s.loc[s["dispositivo"] == d, "tempo_s"])
                               for d in E.DISPOSITIVOS},
            "tarefas_no_teto": {d: {"n": int(teto.sum()[d]), "proporcao": float(teto.mean()[d])}
                                for d in E.DISPOSITIVOS},
        },
        "_tabela": w,
    }


def analisar_rq3(sus, ids) -> dict:
    w = tabela_rq3(sus, ids)
    u = sus[sus["participante"].isin(ids)]
    itens = {d: {f"item_{i}": float(u.loc[u["dispositivo"] == d, f"item_{i}"].mean())
                 for i in range(1, 11)} for d in E.DISPOSITIVOS}
    return {
        "teste": "t pareado no escore SUS",
        "primario": t_pareado(w["dif"]),
        "descritiva": {d: {**descrever(w[d]),
                           "media_menos_68": float(w[d].mean() - 68),
                           "proporcao_ge_68": float((w[d] >= 68).mean())}
                       for d in E.DISPOSITIVOS},
        "nota_68": "comparação com 68 só descritiva, sem teste",
        "itens_media": itens,
        "_tabela": w,
    }


def confirmatorias(t: dict, ids, p1=P1_PRIMARIA, semente=E.SEMENTE) -> dict:
    """RQ1–RQ3 com Holm sobre os 3 p-valores primários."""
    r1 = analisar_rq1(t["sessoes"], ids, semente)
    r2 = analisar_rq2(t["sessoes"], ids, p1)
    r3 = analisar_rq3(t["sus"], ids)
    ps = [r1["primario"]["p"], r2["primario"]["p"], r3["primario"]["p"]]
    aj = holm(ps)
    for r, a in zip((r1, r2, r3), aj):
        r["p_holm"] = a
        r["rejeita_h0_alfa_005_holm"] = bool(a < 0.05)
    return {"rq1": r1, "rq2": r2, "rq3": r3,
            "holm": {"familia": ["RQ1", "RQ2", "RQ3"], "p": ps, "p_ajustado": aj}}


# ---------------------------------------------------------------------------
# RQ4 (exploratória)
# ---------------------------------------------------------------------------

def passos_rotulados(passos: pd.DataFrame, catalogo: pd.DataFrame) -> pd.DataFrame:
    chave = ["tarefa_id", "passo_id", "dispositivo"]
    dentro = passos[passos["passo_id"] != E.PASSO_FORA]
    return dentro.merge(catalogo[chave + ["rotulo_wcag"]], on=chave, how="left",
                        validate="many_to_one")


def taxas_rq4(passos: pd.DataFrame, catalogo: pd.DataFrame, ids,
              por_tarefa: bool = False) -> pd.DataFrame:
    """Taxa de erro por passo alcançado, com × sem violação, por participante.

    Dispositivos somados; indeterminados fora; fora_do_caminho fora. Entra no
    teste quem alcançou ≥ 1 passo em cada grupo; os demais recebem o motivo.
    """
    m = passos_rotulados(passos[passos["participante"].isin(ids)], catalogo)
    m = m[m["alcancado"] & (m["rotulo_wcag"] != "indeterminado")]
    chave = ["participante"] + (["tarefa_id"] if por_tarefa else [])
    g = m.groupby(chave + ["rotulo_wcag"]).agg(alc=("passo_id", "size"),
                                                 err=("n_erros", "sum"))
    w = g.unstack("rotulo_wcag").fillna(0)
    w.columns = [f"{a}_{'com' if b == 'com_violacao' else 'sem'}" for a, b in w.columns]
    for c in ("alc_com", "alc_sem", "err_com", "err_sem"):
        if c not in w.columns:
            w[c] = 0.0
    if not por_tarefa:
        w = w.reindex(list(ids), fill_value=0.0)
    w["taxa_com"] = w["err_com"] / w["alc_com"].where(w["alc_com"] > 0)
    w["taxa_sem"] = w["err_sem"] / w["alc_sem"].where(w["alc_sem"] > 0)
    w["d"] = w["taxa_com"] - w["taxa_sem"]
    w["elegivel"] = (w["alc_com"] > 0) & (w["alc_sem"] > 0)
    motivo = np.where(w["elegivel"], "",
                      np.where((w["alc_com"] == 0) & (w["alc_sem"] == 0),
                               "nenhum passo alcançado em nenhum dos grupos",
                               np.where(w["alc_com"] == 0,
                                        "nenhum passo com violação alcançado",
                                        "nenhum passo sem violação alcançado")))
    w["motivo_exclusao"] = motivo
    return w[["alc_com", "err_com", "taxa_com", "alc_sem", "err_sem", "taxa_sem",
              "d", "elegivel", "motivo_exclusao"]]


def tabela_2x2(passos, catalogo, ids) -> dict:
    """Passo alcançado (com × sem violação) × erro ≥ 1. Fisher só descritivo."""
    m = passos_rotulados(passos[passos["participante"].isin(ids)], catalogo)
    m = m[m["alcancado"] & m["rotulo_wcag"].isin(["com_violacao", "sem_violacao_detectada"])]
    tab = pd.crosstab(m["rotulo_wcag"], m["n_erros"] >= 1).reindex(
        index=["com_violacao", "sem_violacao_detectada"], columns=[True, False], fill_value=0)
    odds, p = stats.fisher_exact(tab.to_numpy())
    return {"linhas": ["com_violacao", "sem_violacao_detectada"],
            "colunas": ["erro>=1", "sem_erro"], "contagens": tab.to_numpy().tolist(),
            "fisher_odds_ratio": float(odds), "fisher_p_descritivo": float(p),
            "nota": "apenas descritivo: agrupa passos de vários participantes "
                    "(observações dependentes); não é teste da RQ4"}


def analisar_rq4(passos, catalogo, ids, rq4_teste=True, semente=E.SEMENTE) -> dict:
    w = taxas_rq4(passos, catalogo, ids)
    el = w[w["elegivel"]]
    rot = passos_rotulados(passos[passos["participante"].isin(ids)], catalogo)
    alc = rot[rot["alcancado"]]
    ind = catalogo[catalogo["rotulo_wcag"] == "indeterminado"]
    fora = passos[passos["participante"].isin(ids) & (passos["passo_id"] == E.PASSO_FORA)]
    excl = w.loc[~w["elegivel"], "motivo_exclusao"].value_counts()
    out = {
        "rotulo": "EXPLORATÓRIA — fora do Holm, p sem ajuste, sem linguagem causal",
        "n_participantes": int(len(w)),
        "n_elegiveis": int(len(el)),
        "excluidos_por_motivo": {k: int(v) for k, v in excl.items()},
        "descritiva": {
            "passos_catalogo_por_rotulo": {k: int(v) for k, v in
                                          catalogo["rotulo_wcag"].value_counts().items()},
            "passos_alcancados_por_rotulo": {k: int(v) for k, v in
                                            alc["rotulo_wcag"].value_counts().items()},
            "erros_por_rotulo": {k: int(v) for k, v in
                                 alc.groupby("rotulo_wcag")["n_erros"].sum().items()},
            "taxa_com": descrever(el["taxa_com"]),
            "taxa_sem": descrever(el["taxa_sem"]),
            "d_i": descrever(el["d"]),
            "n_d_i_zero": int((el["d"] == 0).sum()),
            "indeterminados": {"n_passos_catalogo": int(len(ind)),
                               "motivos": {k: int(v) for k, v in
                                           ind["motivo_indeterminado"].value_counts().items()}},
            "erros_fora_do_caminho": int(fora["n_erros"].sum()),
        },
        "tabela_2x2": tabela_2x2(passos, catalogo, ids),
        "_tabela": w,
    }
    if not rq4_teste:
        out["teste"] = "desligado (rq4_teste=False): só descritiva"
        return out
    out["teste"] = "Wilcoxon pareado sobre d_i (mesmas opções da RQ1)"
    out["primario_exploratorio"] = wilcoxon_pareado(el["d"])
    out["media_d_i"] = float(el["d"].mean()) if len(el) else float("nan")
    out["media_d_i_ic95_bootstrap"] = bootstrap_media(el["d"], semente=semente)
    out["sensibilidade_permutacao_sinais"] = permutacao_sinais(el["d"], semente=semente)
    pt = taxas_rq4(passos, catalogo, ids, por_tarefa=True)
    por_tarefa = {}
    for tarefa, g in pt[pt["elegivel"]].groupby(level="tarefa_id"):
        por_tarefa[tarefa] = {"n_elegiveis": int(len(g)), "media_d_i": float(g["d"].mean()),
                              "wilcoxon": wilcoxon_pareado(g["d"])}
    out["sensibilidade_por_tarefa"] = por_tarefa
    return out


# ---------------------------------------------------------------------------
# Checagem de ordem e descritivas extras
# ---------------------------------------------------------------------------

def _dois_grupos(a, b) -> dict:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return {"n": [len(a), len(b)], "nota": "grupos pequenos demais"}
    w = stats.ttest_ind(a, b, equal_var=False)
    mw = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {"n": [int(len(a)), int(len(b))], "media": [float(a.mean()), float(b.mean())],
            "welch_t": float(w.statistic), "welch_p": float(w.pvalue),
            "mann_whitney_U": float(mw.statistic), "mann_whitney_p": float(mw.pvalue)}


def checagem_ordem(difs: dict[str, pd.Series], participantes: pd.DataFrame) -> dict:
    """Período (celular 1º × computador 1º) e conjunto (celular-A × celular-B).

    Descritiva, fora do Holm. Com 8 por sequência o poder é baixo e não
    calculado: não encontrar diferença não prova ausência de efeito de ordem.
    """
    seq = participantes.set_index("participante")["sequencia"]
    out = {"aviso": "descritiva, fora do Holm; poder baixo e não calculado"}
    for nome, dif in difs.items():
        dif = dif.dropna()
        s = seq.reindex(dif.index)
        out[nome] = {
            "periodo_celular_primeiro_vs_computador_primeiro":
                _dois_grupos(dif[s.isin([1, 2])], dif[s.isin([3, 4])]),
            "conjunto_celularA_vs_celularB":
                _dois_grupos(dif[s.isin([1, 4])], dif[s.isin([2, 3])]),
        }
    return out


def descritivas_extras(sessoes, ids) -> dict:
    s = sessoes[sessoes["participante"].isin(ids)]
    seq = {d: {str(k): int(v) for k, v in
               s.loc[s["dispositivo"] == d, "seq"].value_counts().reindex(range(1, 8), fill_value=0).items()}
           for d in E.DISPOSITIVOS}
    erros = (s.groupby(["tarefa_id", "dispositivo"])["erros"]
             .agg(["count", "mean", "median", "sum"]).reset_index())
    motivos = s.groupby(["dispositivo", "motivo_fim"]).size().unstack(fill_value=0)
    return {
        "seq_distribuicao": seq,
        "seq_mediana": {d: float(s.loc[s["dispositivo"] == d, "seq"].median())
                        for d in E.DISPOSITIVOS},
        "erros_por_tarefa": erros.to_dict(orient="records"),
        "motivo_fim_por_dispositivo": {d: {k: int(v) for k, v in motivos.loc[d].items()}
                                       for d in motivos.index},
    }


# ---------------------------------------------------------------------------
# Auditoria (Q4, descritiva)
# ---------------------------------------------------------------------------

def normalizar_axe(conteudo) -> list[dict]:
    """Converte um export do axe em linhas (regra, impacto, tags, n_nós).

    Formatos aceitos:
    1. axe-core JSON: objeto com ``violations`` (cada uma com ``id``,
       ``impact``, ``tags`` e ``nodes``);
    2. lista de objetos no formato 1;
    3. export da extensão axe DevTools com ``allIssues`` (ou ``issues``): um
       item por nó, com ``ruleId``/``rule_id``/``id``, ``impact`` e, se houver,
       ``tags``. **Formato 3 inferido, a confirmar com um export real.**
    """
    if isinstance(conteudo, list):
        return [lin for item in conteudo for lin in normalizar_axe(item)]
    if not isinstance(conteudo, dict):
        raise ValueError("JSON do axe em formato não reconhecido")
    if "violations" in conteudo:
        return [{"regra": v["id"], "impacto": v.get("impact") or "desconhecido",
                 "tags": list(v.get("tags", [])), "n_nos": len(v.get("nodes", []))}
                for v in conteudo["violations"]]
    itens = conteudo.get("allIssues", conteudo.get("issues"))
    if isinstance(itens, list):
        agg: dict[str, dict] = {}
        for it in itens:
            regra = it.get("ruleId") or it.get("rule_id") or it.get("id")
            a = agg.setdefault(regra, {"regra": regra,
                                       "impacto": it.get("impact") or "desconhecido",
                                       "tags": list(it.get("tags", [])), "n_nos": 0})
            a["n_nos"] += 1
        return list(agg.values())
    raise ValueError("JSON do axe sem 'violations' nem 'allIssues'")


def ler_lighthouse(conteudo: dict) -> dict:
    """Nota de acessibilidade (0–100), LCP (ms) e CLS de um JSON do Lighthouse."""
    cat = conteudo.get("categories", {}).get("accessibility", {})
    aud = conteudo.get("audits", {})
    nota = cat.get("score")
    return {"nota_acessibilidade": None if nota is None else 100 * float(nota),
            "lcp_ms": aud.get("largest-contentful-paint", {}).get("numericValue"),
            "cls": aud.get("cumulative-layout-shift", {}).get("numericValue")}


def analisar_auditoria(pasta: Path, sintetico: bool) -> dict | None:
    idx = E.carregar_indice_auditoria(pasta, sintetico)
    if idx is None:
        return None
    base = E.pasta_auditoria(pasta)
    linhas_axe, linhas_lh = [], []
    for _, lin in idx.iterrows():
        conteudo = json.loads((base / lin["arquivo"]).read_text(encoding="utf-8"))
        if lin["ferramenta"] == "axe":
            for v in normalizar_axe(conteudo):
                linhas_axe.append({"pagina_url": lin["pagina_url"], "modo": lin["modo"], **v})
        else:
            linhas_lh.append({"pagina_url": lin["pagina_url"], "modo": lin["modo"],
                              "execucao": int(lin["execucao"]), **ler_lighthouse(conteudo)})
    axe = pd.DataFrame(linhas_axe, columns=["pagina_url", "modo", "regra", "impacto", "tags", "n_nos"])
    lh = pd.DataFrame(linhas_lh)
    tags_wcag = set(E.TAGS_WCAG)
    axe["wcag"] = axe["tags"].map(lambda t: bool(tags_wcag & set(t)))
    axe["best_practice"] = axe["tags"].map(lambda t: "best-practice" in t)
    paginas = idx["pagina_url"].unique()
    por_pag = (axe.groupby(["pagina_url", "modo"])
               .agg(regras=("regra", "size"), nos=("n_nos", "sum"))
               .reindex(pd.MultiIndex.from_product([paginas, E.MODOS_AUDITORIA],
                                                   names=["pagina_url", "modo"]), fill_value=0))
    sev = (axe.pivot_table(index=["pagina_url", "modo"], columns="impacto", values="n_nos",
                           aggfunc="sum", fill_value=0))

    def top(df):
        g = df.groupby("regra").agg(paginas=("pagina_url", "nunique"), ocorrencias=("regra", "size"),
                                     nos=("n_nos", "sum"))
        return g.sort_values(["ocorrencias", "nos"], ascending=False).head(10).reset_index()

    out = {
        "nota_contagem": "contagem por regra = 1 por regra violada na página; "
                         "por nó = soma dos elementos afetados",
        "n_paginas": int(len(paginas)),
        "violacoes_por_pagina": {m: {"regras": descrever(por_pag.xs(m, level="modo")["regras"]),
                                     "nos": descrever(por_pag.xs(m, level="modo")["nos"])}
                                 for m in E.MODOS_AUDITORIA},
        "nos_por_severidade_total": {k: int(v) for k, v in
                                     axe.groupby("impacto")["n_nos"].sum().items()},
        "top10_regras_wcag": top(axe[axe["wcag"]]).to_dict(orient="records"),
        "regras_best_practice": top(axe[axe["best_practice"] & ~axe["wcag"]]).to_dict(orient="records"),
        "_por_pagina": por_pag.join(sev).fillna(0).reset_index(),
    }
    if not lh.empty:
        med = lh.groupby(["pagina_url", "modo"])[["nota_acessibilidade", "lcp_ms", "cls"]].median()
        mob = med.xs("mobile", level="modo") if "mobile" in med.index.get_level_values("modo") else med.iloc[0:0]
        out["lighthouse"] = {
            "nota_acessibilidade_ordinal": {m: descrever(med.xs(m, level="modo")["nota_acessibilidade"])
                                            for m in med.index.get_level_values("modo").unique()},
            "nota_obs": "nota Lighthouse é ordinal: usar mediana/distribuição, não média",
            "lcp_mobile_ms_mediana_3_execucoes": descrever(mob["lcp_ms"]),
            "cls_mobile_mediana_3_execucoes": descrever(mob["cls"]),
        }
        out["_lighthouse"] = med.reset_index()
    return out


# ---------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------

def preparar(pasta: Path) -> tuple[dict[str, pd.DataFrame], bool, str]:
    """Carrega, recusa mistura de origem e converte tipos."""
    brutas, sintetico = E.carregar_tabelas(pasta)
    origem = E.exigir_origem_unica(brutas, sintetico)
    return E.tipar(brutas), sintetico, origem


def analisar(tabelas: dict[str, pd.DataFrame], origem: str, p1: str = P1_PRIMARIA,
             p2: str = P2_PRIMARIA, rq4_teste: bool = True,
             semente: int = E.SEMENTE) -> dict:
    """Análise completa (função pura sobre as tabelas tipadas)."""
    E.exigir_origem_unica(tabelas, origem == "sintetico")
    sel = selecionar_amostra(tabelas["participantes"], p2)
    ids = sel["ids"]
    conf = confirmatorias(tabelas, ids, p1, semente)
    rq4 = analisar_rq4(tabelas["passos"], tabelas["catalogo_passos"], ids, rq4_teste, semente)
    ordem = checagem_ordem({"rq1_concluidas": conf["rq1"]["_tabela"]["dif"],
                            "rq2_log_tempo": conf["rq2"]["_tabela"]["dif"],
                            "rq3_sus": conf["rq3"]["_tabela"]["dif"]},
                           tabelas["participantes"])
    sens = {"rotulo": "SENSIBILIDADE — não substitui a análise primária",
            "p1": {}, "p2": {}}
    for v in VARIANTES_P1:
        if v != p1:
            r = analisar_rq2(tabelas["sessoes"], ids, v)
            sens["p1"][v] = {"descricao": VARIANTES_P1[v], "rq2_t_pareado": r["primario"],
                             "razao_medias_geometricas": r["razao_medias_geometricas"]}
    for v in VARIANTES_P2:
        if v != p2:
            s2 = selecionar_amostra(tabelas["participantes"], v)
            c2 = confirmatorias(tabelas, s2["ids"], p1, semente)
            sens["p2"][v] = {"descricao": VARIANTES_P2[v], "n": len(s2["ids"]),
                             "holm": c2["holm"],
                             "efeitos": {"rq1_r": c2["rq1"]["primario"]["r"],
                                         "rq2_d_z": c2["rq2"]["primario"]["d_z"],
                                         "rq3_d_z": c2["rq3"]["primario"]["d_z"]}}
    out = {
        "origem": origem,
        "aviso": AVISO_SINTETICO if origem == "sintetico" else
                 "dados reais: conferir validação e segunda pessoa antes de citar",
        "parametros": {"p1": {"variante": p1, "status": STATUS_P1},
                       "p2": {"variante": p2, "descricao": VARIANTES_P2[p2], "status": STATUS_P2},
                       "rq4_teste": rq4_teste, "semente": semente,
                       "b_bootstrap": B_BOOTSTRAP, "diferenca": "celular − computador"},
        "amostra": {"n": len(ids), "k_por_sequencia": sel["k"], "ids": ids,
                    "fora_da_analise": sel["fora"]},
        **conf,
        "rq4": rq4,
        "checagem_ordem": ordem,
        "descritivas_extras": descritivas_extras(tabelas["sessoes"], ids),
        "sensibilidades": sens,
    }
    return out


def _jsonavel(x):
    if isinstance(x, dict):
        return {str(k): _jsonavel(v) for k, v in x.items() if not str(k).startswith("_")}
    if isinstance(x, (list, tuple)):
        return [_jsonavel(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return None if math.isnan(float(x)) else float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def verificar_destino(saida: Path, sintetico: bool) -> None:
    """Sintético nunca vai para resultados/; real nunca vai para dados/sinteticos/."""
    partes = Path(saida).resolve().parts
    if sintetico and "resultados" in partes:
        raise E.ErroDeDados("Saída de dados sintéticos não pode ir para resultados/.")
    if not sintetico and "sinteticos" in partes:
        raise E.ErroDeDados("Saída de dados reais não pode ir para dados/sinteticos/.")


def destino_padrao(sintetico: bool) -> Path:
    return RAIZ / ("dados/sinteticos/saida" if sintetico else "resultados")


def graficos(res: dict, saida: Path, prefixo: str, sintetico: bool) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    marca = " — DADOS SINTÉTICOS (não é resultado)" if sintetico else ""
    feitos = []
    for chave, titulo, transf, rotulo in (
        ("rq2", "RQ2: média geométrica do tempo por participante", np.exp, "segundos (teto 300 s)"),
        ("rq3", "RQ3: escore SUS por participante", None, "SUS (0–100)"),
    ):
        w = res[chave]["_tabela"]
        dados = [w[d].dropna() for d in E.DISPOSITIVOS]
        if transf is not None:
            dados = [transf(d) for d in dados]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.boxplot(dados, tick_labels=list(E.DISPOSITIVOS))
        ax.set_ylabel(rotulo)
        ax.set_title(titulo + marca, fontsize=9)
        if chave == "rq3":
            ax.axhline(68, ls="--", lw=0.8, color="gray")
            ax.text(2.4, 68, "68", va="center", fontsize=8, color="gray")
        fig.tight_layout()
        f = saida / f"{prefixo}{chave}_boxplot.png"
        fig.savefig(f, dpi=120)
        plt.close(fig)
        feitos.append(f)
    return feitos


def gravar_saidas(res: dict, aud: dict | None, saida: Path, sintetico: bool) -> list[Path]:
    verificar_destino(saida, sintetico)
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    prefixo = E.PREFIXO_SINTETICO if sintetico else ""
    escritos = []
    resumo = {**res, "auditoria_q4": aud}
    f = saida / f"{prefixo}resumo_analise.json"
    f.write_text(json.dumps(_jsonavel(resumo), ensure_ascii=False, indent=1), encoding="utf-8")
    escritos.append(f)
    for chave in ("rq1", "rq2", "rq3", "rq4"):
        f = saida / f"{prefixo}{chave}_por_participante.csv"
        tab = res[chave]["_tabela"].copy()
        tab.insert(0, "origem", res["origem"])
        tab.to_csv(f, lineterminator="\n")
        escritos.append(f)
    if aud is not None:
        for chave in ("_por_pagina", "_lighthouse"):
            if chave in aud:
                f = saida / f"{prefixo}auditoria{chave}.csv"
                aud[chave].assign(origem=res["origem"]).to_csv(f, index=False, lineterminator="\n")
                escritos.append(f)
    escritos += graficos(res, saida, prefixo, sintetico)
    return escritos


def resumo_texto(res: dict) -> str:
    """Linhas curtas para o terminal (sempre com o aviso de origem)."""
    l = [res["aviso"], f"n = {res['amostra']['n']} (P2: {res['parametros']['p2']['variante']}, "
         f"{STATUS_P2}); P1: {res['parametros']['p1']['variante']} ({STATUS_P1})"]
    for k, nome, ef in (("rq1", "RQ1 Wilcoxon", "r"), ("rq2", "RQ2 t pareado (log)", "d_z"),
                        ("rq3", "RQ3 t pareado (SUS)", "d_z")):
        p = res[k]["primario"]
        l.append(f"{nome}: p = {p['p']:.4g}; p Holm = {res[k]['p_holm']:.4g}; {ef} = {p[ef]:.3f}")
    l.append(f"RQ2 razão das médias geométricas = {res['rq2']['razao_medias_geometricas']:.3f} "
             f"(IC95 {res['rq2']['razao_ic95'][0]:.3f}–{res['rq2']['razao_ic95'][1]:.3f})")
    r4 = res["rq4"]
    if "primario_exploratorio" in r4:
        l.append(f"RQ4 (EXPLORATÓRIA, sem ajuste): n elegíveis = {r4['n_elegiveis']}; "
                 f"Wilcoxon p = {r4['primario_exploratorio']['p']:.4g}; "
                 f"permutação p = {r4['sensibilidade_permutacao_sinais']['p']:.4g}; "
                 f"média d_i = {r4['media_d_i']:.3f}")
    return "\n".join(l)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Análise estatística do LAB05 (issue #25)")
    ap.add_argument("pasta", type=Path, help="dados/brutos ou dados/sinteticos")
    ap.add_argument("--saida", type=Path, help="pasta de saída (padrão depende da origem)")
    ap.add_argument("--p1", choices=list(VARIANTES_P1), default=P1_PRIMARIA)
    ap.add_argument("--p2", choices=list(VARIANTES_P2), default=P2_PRIMARIA)
    ap.add_argument("--sem-teste-rq4", action="store_true",
                    help="desliga o teste da RQ4 (se o professor recusar, P4)")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    tabelas, sintetico, origem = preparar(args.pasta)
    res = analisar(tabelas, origem, args.p1, args.p2, not args.sem_teste_rq4)
    aud = analisar_auditoria(args.pasta, sintetico)
    saida = args.saida or destino_padrao(sintetico)
    escritos = gravar_saidas(res, aud, saida, sintetico)
    print(resumo_texto(res))
    print(f"{len(escritos)} arquivos gravados em {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
