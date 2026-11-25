"""Estimativa de impacto para quem usa o atendimento da PBH (issue #29, enunciado §5).

Funções puras sobre os DataFrames que ``estatistica.analisar`` já produz
(``elegiveis`` e ``pares_por_servico``). Este módulo não altera a análise.

O que se calcula (por serviço *s*, para o par de canais A × B; A = primeiro canal)::

    anos                  = (última − primeira data_criacao dos elegíveis, em dias, + 1) / 365,25
    vol_a_ano, vol_b_ano  = n_a / anos, n_b / anos
    dif_mediana_dias      = mediana_b − mediana_a     (só entre encerradas)
    dif_taxa              = taxa_a − taxa_b           (encerradas no horizonte)
    dias_solicitacao_ano  = vol_b_ano × dif_mediana_dias
    encerradas_90d_ano    = vol_b_ano × dif_taxa

O sufixo ``90d`` de ``encerradas_90d_ano`` é só o nome da coluna: o horizonte usado é o de
``config.Parametros`` (``horizonte_dias``, 90 dias por padrão), o mesmo de ``pares_por_servico``.

Valor positivo = B pior que A **no mesmo serviço**; negativo = B melhor que A
(por exemplo, em Portal × APP, o APP é um pouco mais rápido e os valores saem
negativos). Por par, somam-se os serviços; a diferença de mediana é a média
ponderada por ``vol_b_ano`` (só serviços com as duas medianas). O IC de 95% é um
bootstrap percentil que reamostra **serviços** com reposição.

IMPORTANTE: é um **contrafactual hipotético** ("se os pedidos de B tivessem o
desempenho de A no mesmo serviço"), **não** um efeito causal. O cidadão escolhe o
canal, a base é observacional e "encerrada" não significa "resolvida". Também não
há conversão em horas do cidadão: dias de espera até o encerramento não são
horas de esforço (pendência P5).

Só entram pares com conclusão sustentada (nenhum com Presencial, que é
inconclusivo: ``docs/interpretacao_resultados.md`` §4).
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

# Pares de impacto (A, B). Decisão fixada: sem Presencial, sem medianas globais.
PARES_IMPACTO: list[tuple[str, str]] = [
    ("portal_servicos", "pbh_app"),
    ("portal_servicos", "telefone_156"),
    ("pbh_app", "telefone_156"),
]

METRICAS = ("dif_mediana_ponderada_dias", "dias_solicitacao_ano", "encerradas_90d_ano")

COLUNAS_SERVICO = ["servico", "canal_a", "canal_b", "vol_a_ano", "vol_b_ano",
                   "dif_mediana_dias", "dif_taxa", "dias_solicitacao_ano",
                   "encerradas_90d_ano"]
COLUNAS_PAR = (["canal_a", "canal_b", "servicos", "vol_b_ano_total"]
               + [f"{m}{s}" for m in METRICAS for s in ("", "_ic_lo", "_ic_hi")])


def anos_coorte(el: pd.DataFrame) -> float:
    """Duração da coorte em anos (primeira a última criação, inclusive)."""
    datas = pd.to_datetime(el["data_criacao"])
    dias = (datas.max() - datas.min()).days + 1
    return dias / 365.25


def volume_anual_por_canal(el: pd.DataFrame) -> pd.DataFrame:
    """Solicitações elegíveis por ano de criação e canal, com os meses cobertos.

    ``meses_cobertos`` é o número de meses distintos com criação naquele ano e
    canal; abaixo de 12 indica ano parcial (não comparar com ano cheio).
    """
    datas = pd.to_datetime(el["data_criacao"])
    d = pd.DataFrame({"ano": datas.dt.year, "mes": datas.dt.month, "canal": el["canal"]})
    g = d.groupby(["ano", "canal"]).agg(solicitacoes=("mes", "size"),
                                        meses_cobertos=("mes", "nunique"))
    return g.reset_index().sort_values(["ano", "canal"]).reset_index(drop=True)


def impacto_por_servico(pares: pd.DataFrame, anos: float) -> pd.DataFrame:
    """Impacto anual por serviço, só para os pares de ``PARES_IMPACTO``."""
    if pares is None or pares.empty:
        return pd.DataFrame(columns=COLUNAS_SERVICO)
    chaves = pares[["canal_a", "canal_b"]].apply(tuple, axis=1)
    p = pares[chaves.isin(PARES_IMPACTO)]
    if p.empty:
        return pd.DataFrame(columns=COLUNAS_SERVICO)

    def col(nome):  # colunas de tempo/taxa podem faltar se nenhuma célula as validou
        return p[nome] if nome in p else pd.Series(np.nan, index=p.index)

    vol_a = p["n_a"] / anos
    vol_b = p["n_b"] / anos
    dif_mediana = col("mediana_b") - col("mediana_a")
    dif_taxa = col("taxa_a") - col("taxa_b")
    out = pd.DataFrame({
        "servico": p["servico"], "canal_a": p["canal_a"], "canal_b": p["canal_b"],
        "vol_a_ano": vol_a, "vol_b_ano": vol_b,
        "dif_mediana_dias": dif_mediana, "dif_taxa": dif_taxa,
        "dias_solicitacao_ano": vol_b * dif_mediana,
        "encerradas_90d_ano": vol_b * dif_taxa,
    })
    return out[COLUNAS_SERVICO].reset_index(drop=True)


def _soma_ou_nan(valores: np.ndarray) -> np.ndarray:
    """Soma por linha ignorando NaN; NaN se a linha não tem nenhum valor."""
    valido = ~np.isnan(valores)
    soma = np.where(valido, valores, 0.0).sum(axis=1)
    return np.where(valido.any(axis=1), soma, np.nan)


def _metricas(vol_b: np.ndarray, dif_med: np.ndarray, dif_taxa: np.ndarray,
              idx: np.ndarray) -> dict[str, np.ndarray]:
    """As três métricas do par para cada linha de índices de serviço (``idx``)."""
    vb, dm, dt = vol_b[idx], dif_med[idx], dif_taxa[idx]
    valido = ~np.isnan(dm)
    peso = np.where(valido, vb, 0.0).sum(axis=1)
    num = np.where(valido, vb * np.where(valido, dm, 0.0), 0.0).sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        ponderada = np.where(peso > 0, num / np.where(peso > 0, peso, 1.0), np.nan)
    return {"dif_mediana_ponderada_dias": ponderada,
            "dias_solicitacao_ano": _soma_ou_nan(vb * dm),
            "encerradas_90d_ano": _soma_ou_nan(vb * dt)}


def _percentil(x: np.ndarray, q: float) -> float:
    x = x[~np.isnan(x)]
    return float(np.percentile(x, q)) if x.size else np.nan


def impacto_por_par(por_servico: pd.DataFrame, semente: int, n_boot: int = 2000) -> pd.DataFrame:
    """Agrega por par e calcula o IC 95% por bootstrap (reamostra serviços)."""
    rng = np.random.default_rng(semente)
    linhas = []
    for ca, cb in PARES_IMPACTO:
        s = por_servico[(por_servico["canal_a"] == ca) & (por_servico["canal_b"] == cb)]
        if s.empty:
            continue
        vol_b = s["vol_b_ano"].to_numpy(float)
        dif_med = s["dif_mediana_dias"].to_numpy(float)
        dif_taxa = s["dif_taxa"].to_numpy(float)
        k = len(s)
        ponto = _metricas(vol_b, dif_med, dif_taxa, np.arange(k)[None, :])
        boot = _metricas(vol_b, dif_med, dif_taxa, rng.integers(0, k, size=(n_boot, k)))
        lin = {"canal_a": ca, "canal_b": cb, "servicos": k,
               "vol_b_ano_total": float(vol_b.sum())}
        for m in METRICAS:
            lin[m] = float(ponto[m][0])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                lin[f"{m}_ic_lo"] = _percentil(boot[m], 2.5)
                lin[f"{m}_ic_hi"] = _percentil(boot[m], 97.5)
        linhas.append(lin)
    return pd.DataFrame(linhas, columns=COLUNAS_PAR)
