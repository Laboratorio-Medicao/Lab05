"""Simulação de poder estatístico do LAB05 (RQ1–RQ3, família de Holm de 3 testes).

Versão 4.0 — RECONSTRUÇÃO compatível (issue #20).

O script ``power_analysis.py`` v3.2 e o arquivo ``results_v3_2.json``, citados na
proposta e no relatório de fechamento da S01, não estão no repositório (FONTE DA
VERDADE §18, D1). Esta versão 4 é um MODELO NOVO, escrito a partir da descrição
da proposta; ela não é "o v3.2 reproduzido". Os números produzidos aqui são
ESTIMATIVAS condicionadas a premissas, nunca resultados (FONTE DA VERDADE §2.3 e
§17, regra 13).

Desenho simulado
----------------
- Intrassujeitos, celular × computador, 4 sequências de contrabalanceamento
  (celular-A/computador-B, celular-B/computador-A, computador-A/celular-B,
  computador-B/celular-A), 3 tarefas por conjunto (A e B).
- RQ1: conclusão de cada tarefa ~ Bernoulli(expit(logit)), logit = intercepto do
  dispositivo + u_i (+ perturbações de conjunto, período, tarefa e sequência em
  S1/S2). Contagem 0–3 por dispositivo; dif = celular − computador; Wilcoxon
  pareado (``zero_method="wilcox"``, aproximação normal sem correção de
  continuidade, idêntica a ``scipy.stats.wilcoxon(..., method="approx")``);
  se todas as diferenças forem 0, p = 1.
- RQ2 (log-tempo) e RQ3 (SUS): diferença pareada D (celular − computador) em
  unidades de DP da diferença no cenário S0; média nominal 0,6 (d_z nominal);
  t pareado (equivalente a ``scipy.stats.ttest_rel``).
- Traço latente z_i do participante comum às três RQs: u_i = DP_u · z_i na RQ1 e
  carga λ em z_i nos resíduos de RQ2 e RQ3 (corr(RQ2, RQ3) = λ² no S0).
- Holm calculado à mão (statsmodels não está disponível no ambiente).

Perturbações dos cenários S1 e S2 (aplicadas a cada RQ com sorteios próprios)
------------------------------------------------------------------------------
Na diferença D do participante i, com g_i = +1 se o celular usou o conjunto B
(−1 se A) e h_i = +1 se o celular foi o 2º dispositivo (−1 se o 1º):

    D_i = μ + e_i + g_i·(δ + Δτ) + h_i·π + η_{s(i)}

- δ: diferença fixa de dificuldade entre os conjuntos A e B;
- Δτ = média(τ_B) − média(τ_A), com τ_k ~ N(0, σ_τ²) sorteado por replicação
  para cada uma das 6 tarefas (variação entre tarefas);
- π: efeito de período (aprendizado);
- η_s ~ N(0, σ_seq²) sorteado por replicação para cada sequência (ruído de
  sequência; não se cancela na média).
Com 8 por sequência, g e h somam zero: conjunto, tarefa e período se cancelam na
média e entram só como variância. Com sequências desbalanceadas eles deixam de
se cancelar, o que pode inflar o erro tipo I.

Na RQ1 as mesmas magnitudes entram em unidades de logit, por tarefa e por
dispositivo: ±δ/2 pelo conjunto, ±π/2 pelo período, τ_k pela tarefa e ±η_s/2
pela sequência (celular +, computador −). Os interceptos são recalculados em cada
cenário (Gauss-Hermite) para que a conclusão marginal continue 90% / 75%.

Regra de calibração (fixada ANTES da rodada completa; não reajustar depois)
---------------------------------------------------------------------------
(a) DP_u (DP de u_i em logit): escolhido para que o poder da RQ1 no S0, com Holm,
    seja 0,778 (busca por grade + bisseção, números aleatórios comuns, semente
    própria, R_cal replicações).
(b) Ruído de S1 e S2: a variância extra X = (0,6 / d_z efetivo alvo)² − 1, com
    alvos 0,557 (S1) e 0,469 (S2), é dividida em proporções fixas e declaradas:
    25% conjunto (δ²), 25% tarefa (2σ_τ²/3), 25% período (π²), 25% sequência
    (σ_seq²). Isso torna o d_z efetivo analítico exatamente igual ao alvo.
(c) Correlação entre RQ2 e RQ3 fixada em 0,5 (λ = √0,5), sem calibração.
Checagens independentes (não usadas para ajustar nada): RQ2/RQ3 com Holm nos 3
cenários; RQ1 em S1/S2; erro tipo I com sequências desbalanceadas (n = 24, 28) e
balanceadas (n = 32). Critério de compatibilidade com os valores citados:
|Δ| ≤ 3·EP_MC, EP_MC = sqrt(p(1 − p)/R).

Reprodutibilidade
-----------------
Semente 20261117. ``numpy.random.SeedSequence(20261117).spawn(len(CELULAS))``
gera uma semente filha por célula, na ordem fixa de ``CELULAS`` (a primeira é a
da calibração).

Uso::

    python scripts/power_analysis.py [--reps N] [--reps-calibracao N] [--out caminho]
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import date
from pathlib import Path

import numpy as np
import scipy
from scipy import optimize, special, stats

VERSAO_SCRIPT = "4.0"
SEMENTE = 20261117
ALFA = 0.05
N_TAREFAS = 3
R_PADRAO = 20_000
R_CALIBRACAO_PADRAO = 50_000

# Sequências: (nome, celular é o 1º dispositivo?, conjunto do celular: 0 = A, 1 = B)
SEQUENCIAS = (
    ("celular-A/computador-B", True, 0),
    ("celular-B/computador-A", True, 1),
    ("computador-A/celular-B", False, 1),
    ("computador-B/celular-A", False, 0),
)

P_COMPUTADOR = 0.90  # conclusão marginal por tarefa no computador (premissa da proposta)
P_CELULAR = 0.75  # conclusão marginal por tarefa no celular (premissa da proposta)
P_SOB_H0 = (P_COMPUTADOR + P_CELULAR) / 2  # sob H0, os dois dispositivos com 82,5%
DZ_NOMINAL = 0.6  # d_z nominal de RQ2 e RQ3 no S0
DZ_EFETIVO_ALVO = {"S0": 0.6, "S1": 0.557, "S2": 0.469}
PROPORCOES_RUIDO = {"conjunto": 0.25, "tarefa": 0.25, "periodo": 0.25, "sequencia": 0.25}
CORR_RQ2_RQ3 = 0.5
CARGA_LATENTE = float(np.sqrt(CORR_RQ2_RQ3))
ALVO_CALIBRACAO_RQ1_S0_HOLM = 0.778

# Valores citados na proposta (§4, n = 32) e no relatório (§5): poder com Holm.
CITADOS_PODER = {
    "S0": {"RQ1": 0.778, "RQ2": 0.883, "RQ3": 0.875},
    "S1": {"RQ1": 0.671, "RQ2": 0.821, "RQ3": 0.818},
    "S2": {"RQ1": 0.557, "RQ2": 0.650, "RQ3": 0.649},
}
# Proposta §7: "o erro familiar chegou a 0,068 e 0,073 no cenário realista".
CITADOS_TIPO_I = {"n24": 0.068, "n28": 0.073}

# Desbalanceamentos declarados (participantes por sequência, na ordem de SEQUENCIAS).
# n = 24: faltam 4 nas duas sequências "computador primeiro" (período desbalanceado).
# n = 28: faltam 4 na sequência computador-B/celular-A (período e conjunto desbalanceados).
CONTAGENS = {
    "n32": (8, 8, 8, 8),
    "n24": (8, 8, 4, 4),
    "n28": (8, 8, 8, 4),
}

# Ordem fixa das células; cada uma recebe uma semente filha de SeedSequence(SEMENTE).
CELULAS = (
    "calibracao_dp_u",
    "poder_S0_n32",
    "poder_S1_n32",
    "poder_S2_n32",
    "h0_S0_n32",
    "h0_S1_n32",
    "h0_S1_n24",
    "h0_S1_n28",
)

AVISO = (
    "Estimativa condicionada às premissas do modelo v4 (reconstrução compatível, "
    "não o v3.2 citado). Poder simulado NÃO é resultado empírico (FONTE DA VERDADE "
    "§2.3 e §17)."
)


# ---------------------------------------------------------------------------
# Parâmetros
# ---------------------------------------------------------------------------

def parametros_cenario(cenario: str) -> dict:
    """Parâmetros de ruído do cenário, derivados da regra de calibração (b)."""
    if cenario not in DZ_EFETIVO_ALVO:
        raise ValueError(f"cenário desconhecido: {cenario}")
    extra = (DZ_NOMINAL / DZ_EFETIVO_ALVO[cenario]) ** 2 - 1.0
    return {
        "variancia_extra": extra,
        "delta_conjunto": float(np.sqrt(PROPORCOES_RUIDO["conjunto"] * extra)),
        "dp_tarefa": float(np.sqrt(PROPORCOES_RUIDO["tarefa"] * extra * 3.0 / 2.0)),
        "efeito_periodo": float(np.sqrt(PROPORCOES_RUIDO["periodo"] * extra)),
        "dp_sequencia": float(np.sqrt(PROPORCOES_RUIDO["sequencia"] * extra)),
    }


def dz_efetivo_analitico(cenario: str, mu: float = DZ_NOMINAL) -> float:
    """d_z populacional E[D]/DP(D), com D incluindo todo o ruído (sequências balanceadas)."""
    p = parametros_cenario(cenario)
    var = (1.0 + p["delta_conjunto"] ** 2 + 2.0 * p["dp_tarefa"] ** 2 / 3.0
           + p["efeito_periodo"] ** 2 + p["dp_sequencia"] ** 2)
    return float(mu / np.sqrt(var))


def intercepto_logit(p_marginal: float, dp_normal: float, deslocamentos=(0.0,)) -> float:
    """Intercepto a tal que média(E[expit(a + c + dp·Z)]) = p_marginal (Gauss-Hermite).

    ``deslocamentos`` são deslocamentos c igualmente prováveis (combinações de
    conjunto e período); Z ~ N(0, 1).
    """
    nos, pesos = np.polynomial.hermite_e.hermegauss(80)
    pesos = pesos / pesos.sum()
    desl = np.asarray(deslocamentos, dtype=float)

    def f(a):
        return float(np.mean([(pesos * special.expit(a + c + dp_normal * nos)).sum()
                              for c in desl])) - p_marginal

    return float(optimize.brentq(f, -40.0, 40.0, xtol=1e-12))


def interceptos_cenario(cenario: str, dp_u: float, sob_h0: bool = False) -> tuple[float, float]:
    """Interceptos (computador, celular) que mantêm a conclusão marginal no cenário."""
    p = parametros_cenario(cenario)
    dp_normal = np.sqrt(dp_u ** 2 + p["dp_tarefa"] ** 2 + (p["dp_sequencia"] / 2.0) ** 2)
    d, pi_ = p["delta_conjunto"] / 2.0, p["efeito_periodo"] / 2.0
    deslocamentos = (d + pi_, d - pi_, -d + pi_, -d - pi_)
    p_comp, p_cel = (P_SOB_H0, P_SOB_H0) if sob_h0 else (P_COMPUTADOR, P_CELULAR)
    return (intercepto_logit(p_comp, dp_normal, deslocamentos),
            intercepto_logit(p_cel, dp_normal, deslocamentos))


def alocar_sequencias(contagens) -> np.ndarray:
    """Índice da sequência de cada participante (ex.: (8, 8, 8, 8) → 32 participantes)."""
    return np.repeat(np.arange(len(SEQUENCIAS)), contagens)


# ---------------------------------------------------------------------------
# Testes (vetorizados por replicação: arrays de forma (R, n))
# ---------------------------------------------------------------------------

def wilcoxon_pareado(dif: np.ndarray) -> np.ndarray:
    """p bicaudal do Wilcoxon pareado para diferenças inteiras, linha a linha.

    Igual a ``scipy.stats.wilcoxon(d, zero_method="wilcox", method="approx")``
    (aproximação normal, correção de empates, sem correção de continuidade).
    Linhas com todas as diferenças iguais a 0 recebem p = 1.
    """
    dif = np.atleast_2d(np.asarray(dif))
    if not np.issubdtype(dif.dtype, np.integer):
        if not np.all(dif == np.round(dif)):
            raise ValueError("wilcoxon_pareado espera diferenças inteiras")
        dif = dif.astype(np.int64)
    absd = np.abs(dif)
    kmax = int(absd.max()) if absd.size else 0
    n_r = np.zeros(dif.shape[0])
    r_mais = np.zeros(dif.shape[0])
    empates = np.zeros(dif.shape[0])
    acumulado = np.zeros(dif.shape[0])
    for k in range(1, kmax + 1):
        c_k = (absd == k).sum(axis=1).astype(float)
        posto_medio = acumulado + (c_k + 1.0) / 2.0
        r_mais += posto_medio * (dif == k).sum(axis=1)
        empates += c_k ** 3 - c_k
        acumulado += c_k
        n_r += c_k
    media = n_r * (n_r + 1.0) / 4.0
    var = n_r * (n_r + 1.0) * (2.0 * n_r + 1.0) / 24.0 - empates / 48.0
    p = np.ones(dif.shape[0])
    ok = var > 0
    z = (r_mais[ok] - media[ok]) / np.sqrt(var[ok])
    p[ok] = 2.0 * stats.norm.sf(np.abs(z))
    return np.minimum(p, 1.0)


def t_pareado(d: np.ndarray) -> np.ndarray:
    """p bicaudal do t pareado (t de uma amostra nas diferenças), linha a linha."""
    d = np.atleast_2d(d)
    n = d.shape[1]
    t = d.mean(axis=1) / (d.std(axis=1, ddof=1) / np.sqrt(n))
    return 2.0 * stats.t.sf(np.abs(t), n - 1)


def holm_rejeicoes(p: np.ndarray, alfa: float = ALFA) -> np.ndarray:
    """Rejeições de Holm (passo descendente) para cada linha de p (forma (R, m))."""
    p = np.atleast_2d(p)
    m = p.shape[1]
    ordem = np.argsort(p, axis=1, kind="stable")
    p_ord = np.take_along_axis(p, ordem, axis=1)
    limites = alfa / (m - np.arange(m))
    rej_ord = np.cumprod(p_ord <= limites, axis=1).astype(bool)
    rej = np.zeros_like(rej_ord)
    np.put_along_axis(rej, ordem, rej_ord, axis=1)
    return rej


def holm_ajustados(p: np.ndarray) -> np.ndarray:
    """p-valores ajustados por Holm (cada linha), limitados a 1."""
    p = np.atleast_2d(np.asarray(p, dtype=float))
    m = p.shape[1]
    ordem = np.argsort(p, axis=1, kind="stable")
    p_ord = np.take_along_axis(p, ordem, axis=1)
    aj_ord = np.minimum(np.maximum.accumulate(p_ord * (m - np.arange(m)), axis=1), 1.0)
    aj = np.empty_like(aj_ord)
    np.put_along_axis(aj, ordem, aj_ord, axis=1)
    return aj


# ---------------------------------------------------------------------------
# Geração dos dados
# ---------------------------------------------------------------------------

def _indicadores(seq: np.ndarray):
    """g (+1 se celular usou B), h (+1 se celular foi o 2º) e conjunto do celular."""
    cel_primeiro = np.array([s[1] for s in SEQUENCIAS])[seq]
    conj_cel = np.array([s[2] for s in SEQUENCIAS])[seq]
    g = np.where(conj_cel == 1, 1.0, -1.0)
    h = np.where(cel_primeiro, -1.0, 1.0)
    return g, h, conj_cel


def _diferenca_continua(rng, R, seq, e, mu, par):
    """D = μ + e + g(δ + Δτ) + hπ + η_s para RQ2 ou RQ3 (sorteios próprios da RQ)."""
    g, h, _ = _indicadores(seq)
    tau = rng.standard_normal((R, 2 * N_TAREFAS)) * par["dp_tarefa"]
    delta_tau = tau[:, N_TAREFAS:].mean(axis=1) - tau[:, :N_TAREFAS].mean(axis=1)
    eta = rng.standard_normal((R, len(SEQUENCIAS))) * par["dp_sequencia"]
    return (mu + e + g[None, :] * (par["delta_conjunto"] + delta_tau[:, None])
            + h[None, :] * par["efeito_periodo"] + eta[:, seq])


def _gerar_brutos(rng, R, contagens):
    """Sorteios-base de uma célula, na ordem fixa (permite números aleatórios comuns)."""
    seq = alocar_sequencias(contagens)
    n = seq.size
    z = rng.standard_normal((R, n))
    xi2 = rng.standard_normal((R, n))
    xi3 = rng.standard_normal((R, n))
    u_unif = rng.random((R, n, 2, N_TAREFAS))  # [.., dispositivo (0 comp, 1 cel), tarefa]
    tau1 = rng.standard_normal((R, 2 * N_TAREFAS))
    eta1 = rng.standard_normal((R, len(SEQUENCIAS)))
    return {"seq": seq, "z": z, "xi2": xi2, "xi3": xi3, "unif": u_unif,
            "tau1": tau1, "eta1": eta1, "rng": rng}


def _contagens_rq1(brutos, cenario, dp_u, sob_h0):
    """Tarefas concluídas (0–3) por participante e dispositivo: arrays (R, n)."""
    par = parametros_cenario(cenario)
    seq = brutos["seq"]
    g, h, conj_cel = _indicadores(seq)
    a_comp, a_cel = interceptos_cenario(cenario, dp_u, sob_h0)
    u = dp_u * brutos["z"]
    tau = brutos["tau1"] * par["dp_tarefa"]
    eta = brutos["eta1"] * par["dp_sequencia"]
    d2, p2 = par["delta_conjunto"] / 2.0, par["efeito_periodo"] / 2.0
    # dispositivo 0 = computador, 1 = celular
    conj = np.stack([1 - conj_cel, conj_cel], axis=1)  # (n, 2)
    sinal_conj = np.where(conj == 1, 1.0, -1.0)
    sinal_per = np.stack([-h, h], axis=1)  # computador é o 2º quando o celular é o 1º
    sinal_seq = np.array([-1.0, 1.0])
    idx_tarefa = conj[:, :, None] * N_TAREFAS + np.arange(N_TAREFAS)  # (n, 2, 3)
    logit = (np.array([a_comp, a_cel])[None, None, :, None]
             + u[:, :, None, None]
             + (sinal_conj * d2 + sinal_per * p2)[None, :, :, None]
             + tau[:, idx_tarefa]
             + (eta[:, seq][:, :, None] * sinal_seq[None, None, :] / 2.0)[..., None])
    concluidas = (brutos["unif"] < special.expit(logit)).sum(axis=3)
    return concluidas[:, :, 0], concluidas[:, :, 1]


def simular(rng, R, contagens, cenario, dp_u, sob_h0=False, brutos=None):
    """Simula uma célula e devolve p-valores (R, 3) e diagnósticos."""
    if brutos is None:
        brutos = _gerar_brutos(rng, R, contagens)
    rng = brutos["rng"]
    par = parametros_cenario(cenario)
    mu = 0.0 if sob_h0 else DZ_NOMINAL
    comp, cel = _contagens_rq1(brutos, cenario, dp_u, sob_h0)
    p1 = wilcoxon_pareado(cel - comp)
    lam = CARGA_LATENTE
    e2 = lam * brutos["z"] + np.sqrt(1 - lam ** 2) * brutos["xi2"]
    e3 = lam * brutos["z"] + np.sqrt(1 - lam ** 2) * brutos["xi3"]
    d2 = _diferenca_continua(rng, R, brutos["seq"], e2, mu, par)
    d3 = _diferenca_continua(rng, R, brutos["seq"], e3, mu, par)
    p = np.column_stack([p1, t_pareado(d2), t_pareado(d3)])
    return {
        "p": p,
        "conclusao_marginal": {"computador": float(comp.mean() / N_TAREFAS),
                               "celular": float(cel.mean() / N_TAREFAS)},
        "dz_empirico_agregado": {"RQ2": float(d2.mean() / d2.std()),
                                 "RQ3": float(d3.mean() / d3.std())},
        "dz_amostral_medio": {
            "RQ2": float(np.mean(d2.mean(axis=1) / d2.std(axis=1, ddof=1))),
            "RQ3": float(np.mean(d3.mean(axis=1) / d3.std(axis=1, ddof=1)))},
        "corr_D2_D3": float(np.corrcoef(d2.ravel(), d3.ravel())[0, 1]),
        "frac_rq1_todas_dif_zero": float(np.mean(np.all(cel == comp, axis=1))),
    }


def resumir(p: np.ndarray, alfa: float = ALFA) -> dict:
    """Taxas de rejeição: com Holm (principal), sem ajuste, ≥ 1 e as 3 juntas."""
    R = p.shape[0]
    rej_holm = holm_rejeicoes(p, alfa)
    rej_bruta = p <= alfa
    nomes = ("RQ1", "RQ2", "RQ3")

    def ep(x):
        return float(np.sqrt(x * (1 - x) / R))

    holm = {k: float(v) for k, v in zip(nomes, rej_holm.mean(axis=0))}
    bruta = {k: float(v) for k, v in zip(nomes, rej_bruta.mean(axis=0))}
    pelo_menos_um = float(rej_holm.any(axis=1).mean())
    todas = float(rej_holm.all(axis=1).mean())
    return {
        "R": R,
        "com_holm": holm,
        "ep_mc_com_holm": {k: ep(v) for k, v in holm.items()},
        "sem_ajuste": bruta,
        "ep_mc_sem_ajuste": {k: ep(v) for k, v in bruta.items()},
        "pelo_menos_uma_rejeicao_holm": pelo_menos_um,
        "ep_mc_pelo_menos_uma": ep(pelo_menos_um),
        "tres_rejeicoes_holm": todas,
    }


# ---------------------------------------------------------------------------
# Calibração (a)
# ---------------------------------------------------------------------------

def calibrar_dp_u(seed_seq, R_cal=R_CALIBRACAO_PADRAO, alvo=ALVO_CALIBRACAO_RQ1_S0_HOLM):
    """DP_u tal que o poder da RQ1 com Holm no S0 (n = 32) seja ``alvo``.

    Usa números aleatórios comuns (mesmos sorteios para todo DP_u): grade de 0 a 4
    (passo 0,25) e bisseção no primeiro intervalo que cruza o alvo.
    """
    brutos = _gerar_brutos(np.random.default_rng(seed_seq), R_cal, CONTAGENS["n32"])
    par = parametros_cenario("S0")
    lam = CARGA_LATENTE
    rng = brutos["rng"]
    e2 = lam * brutos["z"] + np.sqrt(1 - lam ** 2) * brutos["xi2"]
    e3 = lam * brutos["z"] + np.sqrt(1 - lam ** 2) * brutos["xi3"]
    p2 = t_pareado(_diferenca_continua(rng, R_cal, brutos["seq"], e2, DZ_NOMINAL, par))
    p3 = t_pareado(_diferenca_continua(rng, R_cal, brutos["seq"], e3, DZ_NOMINAL, par))

    def poder(dp_u):
        comp, cel = _contagens_rq1(brutos, "S0", dp_u, False)
        p = np.column_stack([wilcoxon_pareado(cel - comp), p2, p3])
        return float(holm_rejeicoes(p)[:, 0].mean())

    grade = np.arange(0.0, 4.0001, 0.25)
    valores = [poder(s) for s in grade]
    for i in range(1, len(grade)):
        if valores[i - 1] < alvo <= valores[i]:
            lo, hi = grade[i - 1], grade[i]
            break
    else:
        raise RuntimeError(f"alvo {alvo} fora da grade de DP_u: {valores}")
    for _ in range(30):
        meio = (lo + hi) / 2.0
        if poder(meio) < alvo:
            lo = meio
        else:
            hi = meio
    dp_u = (lo + hi) / 2.0
    return {
        "dp_u": float(dp_u),
        "poder_rq1_holm_na_calibracao": poder(dp_u),
        "R_calibracao": R_cal,
        "grade_dp_u": [float(x) for x in grade],
        "grade_poder_rq1_holm": valores,
    }


# ---------------------------------------------------------------------------
# Rodada completa
# ---------------------------------------------------------------------------

def _comparar(reproduzido: float, citado: float, R: int) -> dict:
    ep = float(np.sqrt(reproduzido * (1 - reproduzido) / R))
    delta = reproduzido - citado
    return {
        "citado": citado,
        "reproduzido": reproduzido,
        "delta": delta,
        "ep_mc": ep,
        "delta_sobre_ep": delta / ep if ep > 0 else float("inf"),
        "compativel_3ep": bool(abs(delta) <= 3 * ep),
    }


def poder_t_nao_central(dz: float, n: int, alfa: float = ALFA) -> float:
    """Poder analítico do t pareado bicaudal sem ajuste (t não central)."""
    nc = dz * np.sqrt(n)
    c = stats.t.isf(alfa / 2, n - 1)
    return float(stats.nct.sf(c, n - 1, nc) + stats.nct.cdf(-c, n - 1, nc))


def executar(R=R_PADRAO, R_cal=R_CALIBRACAO_PADRAO, semente=SEMENTE):
    inicio = time.perf_counter()
    filhas = dict(zip(CELULAS, np.random.SeedSequence(semente).spawn(len(CELULAS))))

    calib = calibrar_dp_u(filhas["calibracao_dp_u"], R_cal)
    dp_u = calib["dp_u"]

    poder = {}
    for cen in ("S0", "S1", "S2"):
        rng = np.random.default_rng(filhas[f"poder_{cen}_n32"])
        sim = simular(rng, R, CONTAGENS["n32"], cen, dp_u)
        res = resumir(sim["p"])
        res.update({k: v for k, v in sim.items() if k != "p"})
        res["dz_efetivo_analitico"] = dz_efetivo_analitico(cen)
        res["poder_t_nao_central_sem_ajuste_dz_efetivo"] = poder_t_nao_central(
            dz_efetivo_analitico(cen), 32)
        poder[cen] = res

    tipo_i = {}
    for celula, cen, chave in (("h0_S0_n32", "S0", "n32"), ("h0_S1_n32", "S1", "n32"),
                               ("h0_S1_n24", "S1", "n24"), ("h0_S1_n28", "S1", "n28")):
        rng = np.random.default_rng(filhas[celula])
        sim = simular(rng, R, CONTAGENS[chave], cen, dp_u, sob_h0=True)
        res = resumir(sim["p"])
        res["fwer_holm"] = res.pop("pelo_menos_uma_rejeicao_holm")
        res["ep_mc_fwer"] = res.pop("ep_mc_pelo_menos_uma")
        res.pop("tres_rejeicoes_holm")
        res["contagens_por_sequencia"] = list(CONTAGENS[chave])
        res["cenario"] = cen
        res["conclusao_marginal"] = sim["conclusao_marginal"]
        tipo_i[celula] = res

    comparacao_poder = {cen: {rq: _comparar(poder[cen]["com_holm"][rq], v, R)
                              for rq, v in rqs.items()}
                        for cen, rqs in CITADOS_PODER.items()}
    comparacao_tipo_i = {}
    for chave, citado in CITADOS_TIPO_I.items():
        cel = tipo_i[f"h0_S1_{chave}"]
        comparacao_tipo_i[chave] = {
            "citado": citado,
            "quantidade_citada_na_proposta": "erro familiar (FWER), cenário realista",
            "fwer_holm": _comparar(cel["fwer_holm"], citado, R),
            "por_rq_sem_ajuste": {rq: _comparar(v, citado, R)
                                  for rq, v in cel["sem_ajuste"].items()},
        }
    discrepancias = [f"poder {cen} {rq}" for cen, d in comparacao_poder.items()
                     for rq, c in d.items() if not c["compativel_3ep"]]
    discrepancias += [f"tipo I {k} (FWER)" for k, c in comparacao_tipo_i.items()
                      if not c["fwer_holm"]["compativel_3ep"]]

    return {
        "aviso": AVISO,
        "script": "scripts/power_analysis.py",
        "versao_script": VERSAO_SCRIPT,
        "natureza": "reconstrução compatível (modelo novo); o v3.2 citado segue ausente (D1)",
        "data_execucao": date.today().isoformat(),
        "ambiente": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__, "plataforma": platform.platform()},
        "semente": semente,
        "sementes_por_celula": "numpy.random.SeedSequence(semente).spawn(len(celulas)), na ordem de 'celulas'",
        "celulas": list(CELULAS),
        "R_por_celula": R,
        "alfa": ALFA,
        "parametros": {
            "n_por_sequencia": 8,
            "sequencias": [s[0] for s in SEQUENCIAS],
            "tarefas_por_conjunto": N_TAREFAS,
            "p_conclusao_computador": P_COMPUTADOR,
            "p_conclusao_celular": P_CELULAR,
            "p_conclusao_sob_h0": P_SOB_H0,
            "dz_nominal_rq2_rq3": DZ_NOMINAL,
            "dz_efetivo_alvo": DZ_EFETIVO_ALVO,
            "proporcoes_variancia_extra": PROPORCOES_RUIDO,
            "corr_rq2_rq3": CORR_RQ2_RQ3,
            "carga_latente_rq2_rq3": CARGA_LATENTE,
            "ruido_rq1": "mesmas magnitudes de RQ2/RQ3, em unidades de logit, por tarefa e dispositivo",
            "contagens_desbalanceadas": {k: list(v) for k, v in CONTAGENS.items()},
            "cenarios": {c: parametros_cenario(c) for c in ("S0", "S1", "S2")},
            "testes": {
                "RQ1": "Wilcoxon pareado (zero_method='wilcox', aproximação normal, sem correção de continuidade; p = 1 se todas as dif = 0)",
                "RQ2": "t pareado sobre a diferença do log-tempo (padronizada)",
                "RQ3": "t pareado sobre a diferença de SUS (padronizada, contínua)",
                "correcao": "Holm de 3, calculado à mão (statsmodels indisponível)",
            },
        },
        "regra_calibracao": {
            "a": f"DP_u tal que poder RQ1 S0 com Holm = {ALVO_CALIBRACAO_RQ1_S0_HOLM}",
            "b": "variância extra de S1/S2 = (0,6/d_z alvo)^2 - 1, dividida 25% conjunto, 25% tarefa, 25% período, 25% sequência",
            "c": f"corr(RQ2, RQ3) = {CORR_RQ2_RQ3}, fixada",
            "compatibilidade": "|delta| <= 3*EP_MC, EP_MC = sqrt(p(1-p)/R); sem reajuste após a rodada",
        },
        "calibracao": calib,
        "interceptos_logit": {
            c: dict(zip(("computador", "celular"), interceptos_cenario(c, dp_u)))
            for c in ("S0", "S1", "S2")},
        "poder_n32": poder,
        "erro_tipo_i": tipo_i,
        "comparacao_citado_reproduzido_poder": comparacao_poder,
        "comparacao_citado_reproduzido_tipo_i": comparacao_tipo_i,
        "discrepancias_acima_de_3ep": discrepancias,
        "tempo_execucao_s": round(time.perf_counter() - inicio, 1),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reps", type=int, default=R_PADRAO,
                        help="replicações por célula (padrão: 20000)")
    parser.add_argument("--reps-calibracao", type=int, default=R_CALIBRACAO_PADRAO,
                        help="replicações da calibração de DP_u (padrão: 50000)")
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parent.parent / "resultados" / "results_v4.json",
                        help="caminho do JSON de saída")
    args = parser.parse_args(argv)
    try:  # console do Windows (cp1252) não imprime "Δ" e "·"
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    res = executar(R=args.reps, R_cal=args.reps_calibracao)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON gravado em {args.out} ({res['tempo_execucao_s']} s)")
    print(f"DP_u calibrado: {res['calibracao']['dp_u']:.4f}")
    for cen, d in res["comparacao_citado_reproduzido_poder"].items():
        linha = "  ".join(f"{rq}: {c['reproduzido']:.3f} (citado {c['citado']:.3f}, "
                          f"Δ/EP {c['delta_sobre_ep']:+.1f})" for rq, c in d.items())
        print(f"{cen}  {linha}")
    for k, c in res["comparacao_citado_reproduzido_tipo_i"].items():
        print(f"tipo I {k}: FWER {c['fwer_holm']['reproduzido']:.4f} (citado {c['citado']})")
    if res["discrepancias_acima_de_3ep"]:
        print("DISCREPÂNCIAS > 3·EP_MC:", "; ".join(res["discrepancias_acima_de_3ep"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
