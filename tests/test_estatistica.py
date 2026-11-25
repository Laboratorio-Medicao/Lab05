"""Testes das métricas e da estatística (valores conferidos à mão ou contra o scipy)."""

import math

import numpy as np
import pandas as pd
import pytest
from scipy import stats

import config as C
import estatistica as E
import sintetico as S
import tratamento as T


# --- blocos estatísticos ---------------------------------------------------

def test_holm_valor_conhecido_e_nan():
    assert E.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    r = E.holm([0.5, np.nan, 0.01])
    assert r[0] == pytest.approx(0.5 * 1) or r[0] == pytest.approx(0.5)
    assert np.isnan(r[1]) and r[2] == pytest.approx(0.02)


def test_wilson_valor_conhecido():
    # referência independente: scipy (Wilson sem correção de continuidade)
    for k, n in [(81, 263), (0, 40), (40, 40), (5, 1000)]:
        ref = stats.binomtest(k, n).proportion_ci(confidence_level=0.95, method="wilson")
        assert E.wilson(k, n) == pytest.approx((ref.low, ref.high), abs=1e-6)


def test_newcombe_exemplo_publicado():
    d, lo, hi = E.diferenca_newcombe(56, 70, 48, 80)  # Newcombe (1998), tabela 1
    assert (d, lo, hi) == pytest.approx((0.2, 0.0524, 0.3339), abs=5e-4)


def test_cliff_contra_forca_bruta_e_mann_whitney():
    rng = np.random.default_rng(0)
    x = rng.integers(0, 6, 40).astype(float)
    y = rng.integers(2, 9, 55).astype(float)
    bruto = np.sign(x[:, None] - y[None, :]).mean()
    r = E.cliff(x, y)
    assert r["delta"] == pytest.approx(bruto)
    assert r["delta"] == pytest.approx(2 * r["u_a"] / (40 * 55) - 1)
    assert r["ic_lo"] <= r["delta"] <= r["ic_hi"]
    empate = (x[:, None] == y[None, :]).mean()
    assert r["p_empate"] == pytest.approx(empate)


def test_cliff_extremos():
    r = E.cliff(np.arange(10, 20.0), np.arange(0, 10.0))
    assert r["delta"] == 1.0 and r["ic_hi"] == 1.0
    assert E.cliff(np.arange(10.0), np.arange(10.0))["delta"] == pytest.approx(0.0, abs=1e-12)


def test_cobertura_do_ic_de_cliff():
    rng = np.random.default_rng(3)
    pop_x, pop_y = rng.integers(0, 6, 100000), rng.integers(2, 9, 100000)
    cx = np.bincount(pop_x, minlength=10) / pop_x.size
    cy = np.bincount(pop_y, minlength=10) / pop_y.size
    verdadeiro = sum(cx[i] * cy[j] * np.sign(i - j) for i in range(10) for j in range(10))
    acertos = 0
    n = 300
    for _ in range(n):
        r = E.cliff(rng.integers(0, 6, 60).astype(float), rng.integers(2, 9, 80).astype(float))
        acertos += r["ic_lo"] <= verdadeiro <= r["ic_hi"]
    assert 0.91 <= acertos / n <= 0.99


def test_magnitudes():
    assert E.magnitude_delta(0.10) == "desprezível" and E.magnitude_delta(-0.4) == "média"
    assert E.magnitude_delta(0.6) == "grande" and E.magnitude_h(0.3) == "pequena"


def test_teste_proporcoes_escolhe_fisher_e_qui2():
    assert E.teste_proporcoes([[3, 7], [1, 9]])["teste"] == "fisher"
    r = E.teste_proporcoes([[80, 20], [60, 40]])
    assert r["teste"] == "qui2"
    esp = stats.chi2_contingency(np.array([[80, 20], [60, 40]]), correction=False)
    assert r["p"] == pytest.approx(esp[1])
    assert E.teste_proporcoes([[10, 0], [10, 0]])["teste"] == "degenerado"


def test_cmh_um_estrato_e_dois_estratos():
    assert E.cmh([(20, 80, 10, 90)])["or_mh"] == pytest.approx(2.25)
    t = [(10, 20, 5, 25), (30, 10, 20, 20)]
    a, b, c, d = np.array(t).T
    n = a + b + c + d
    assert E.cmh(t)["or_mh"] == pytest.approx((a * d / n).sum() / (b * c / n).sum())
    # com 1 estrato o CMH é o qui-quadrado com continuidade × (N−1)/N
    tab = np.array([[20, 80], [10, 90]])
    chi = stats.chi2_contingency(tab, correction=True)[0] * (tab.sum() - 1) / tab.sum()
    assert E.cmh([(20, 80, 10, 90)])["chi2"] == pytest.approx(chi)


def test_cmh_detecta_heterogeneidade():
    r = E.cmh([(90, 10, 10, 90), (10, 90, 90, 10)])  # efeitos opostos
    assert r["i2"] > 0.9 and r["q_p"] < 1e-6


def test_van_elteren_um_estrato_igual_mann_whitney():
    rng = np.random.default_rng(1)
    a, b = rng.integers(0, 6, 50).astype(float), rng.integers(1, 8, 70).astype(float)
    mw = stats.mannwhitneyu(a, b, method="asymptotic", use_continuity=False)
    assert E.van_elteren([(a, b)])["p"] == pytest.approx(mw.pvalue, rel=1e-9)


def test_van_elteren_sinal_e_simpson():
    # em cada serviço A é mais lento; misturando, A parece mais rápido (paradoxo de Simpson)
    rng = np.random.default_rng(2)
    e1 = (rng.normal(12, 2, 300), rng.normal(10, 2, 30))
    e2 = (rng.normal(102, 2, 30), rng.normal(100, 2, 300))
    ve = E.van_elteren([e1, e2])
    assert ve["z"] > 5 and ve["p"] < 1e-6
    ingenuo = E.cliff(np.concatenate([e1[0], e2[0]]), np.concatenate([e1[1], e2[1]]))
    assert ingenuo["delta"] < 0  # a comparação ingênua inverte a conclusão


def test_km_a_mao_e_nao_definida():
    assert E.km_mediana(np.array([1, 2, 2, 3]), np.array([2, 3, 5])) == 3.0
    assert math.isnan(E.km_mediana(np.array([5]), np.array([6] * 10)))  # nunca chega a 50%
    assert E.km_mediana(np.array([0, 0, 0, 4]), np.array([], dtype=int)) == 0.0


def test_teste_dos_sinais():
    assert E.teste_dos_sinais(10, 0) == pytest.approx(2 * 0.5 ** 10)
    assert math.isnan(E.teste_dos_sinais(0, 0))


# --- métricas sobre a base sintética --------------------------------------

@pytest.fixture(scope="module")
def base_sintetica(tmp_path_factory):
    pasta = tmp_path_factory.mktemp("sint")
    caminhos = S.gerar_pasta(pasta, n=6000)
    base, _ = T.processar(caminhos, log=lambda *_: None)
    return base


def test_elegibilidade_exclui_inconsistentes_imaturos_e_outros_canais(base_sintetica):
    el = E.selecionar_elegiveis(base_sintetica, 90)
    assert (el["status_registro"] != "inconsistente").all()
    assert el["comparavel"].all() and (el["seguimento_dias"] >= 90).all()
    # jan/2023 → corte 25/07/2023: seguimento > 90 dias, todos maduros
    assert (el["arquivo_origem"] == "dadosabertos_bhdigital_2023_jan.csv").any()
    el_longo = E.selecionar_elegiveis(base_sintetica, 400)  # só 2021 tem ≥ 400 dias
    assert (el_longo["arquivo_origem"] == "dadosabertos_bhdigital_2021.csv").all()
    funil = E.funil_elegibilidade(base_sintetica, 90)
    assert funil["registros"].iloc[0] == len(base_sintetica)
    assert funil["registros"].iloc[-1] == len(el)


def test_encerrada_h_exige_prazo(base_sintetica):
    el = E.selecionar_elegiveis(base_sintetica, 30)
    assert not el.loc[el["tempo_dias"] > 30, "encerrada_h"].any()
    assert el.loc[el["encerrada_h"], "encerrada"].all()
    assert (el.loc[~el["encerrada"], "tempo_dias"].isna()).all()


def test_metricas_por_canal_batem_com_contagem_direta(base_sintetica):
    r = E.analisar(base_sintetica, C.Parametros(min_celula=30))
    el, pc = r["elegiveis"], r["por_canal"].set_index("canal")
    for canal in C.CANAIS_COMPARAVEIS:
        g = el[el["canal"] == canal]
        assert pc.loc[canal, "solicitacoes"] == len(g)
        assert pc.loc[canal, "encerradas"] == g["encerrada"].sum()
        assert pc.loc[canal, "abertas"] + pc.loc[canal, "encerradas"] == len(g)
        assert pc.loc[canal, "mediana_dias"] == g.loc[g["encerrada"], "tempo_dias"].median()
        assert pc.loc[canal, "taxa_encerramento_90d"] == pytest.approx(g["encerrada_h"].mean())


def test_recupera_efeitos_plantados(base_sintetica):
    r = E.analisar(base_sintetica, C.Parametros(min_celula=30))
    pc = r["por_canal"].set_index("canal")
    assert pc.loc["telefone_156", "mediana_dias"] > 2 * pc.loc["portal_servicos", "mediana_dias"]
    assert pc.loc["presencial", "taxa_encerramento_90d"] < 0.3
    est = r["estratificado_por_par"].set_index(["canal_a", "canal_b"])
    # Portal × Presencial: OR muito acima de 1 (Portal encerra mais), p pequeno
    lin = est.loc[("portal_servicos", "presencial")]
    assert lin["or_mh"] > 10 and lin["p_cmh_holm"] < 0.001
    # Portal × Telefone: Telefone mais lento → delta do Portal negativo
    lin = est.loc[("portal_servicos", "telefone_156")]
    assert lin["delta_combinado"] < -0.3 and lin["p_van_elteren_holm"] < 0.001
    assert lin["delta_ic_lo"] <= lin["delta_combinado"] <= lin["delta_ic_hi"]


def test_pares_por_servico_e_holm(base_sintetica):
    p = C.Parametros(min_celula=30)
    r = E.analisar(base_sintetica, p)
    par = r["pares_por_servico"]
    assert par["servico_chave"].nunique() == 3
    assert (par["p_tempo_holm"].dropna() >= par["p_tempo"].dropna()).all()
    assert (par["p_prop_holm"].dropna() <= 1).all()
    # cada linha só existe com células mínimas
    assert (par["n_a"] >= 30).all() and (par["n_b"] >= 30).all()
    lin = par[(par["canal_a"] == "portal_servicos") & (par["canal_b"] == "telefone_156")].iloc[0]
    # conferência independente do Mann–Whitney da primeira linha
    el = r["elegiveis"]
    x = el[(el["servico_chave"] == lin["servico_chave"]) & (el["canal"] == "portal_servicos")
           & el["encerrada"]]["tempo_dias"]
    y = el[(el["servico_chave"] == lin["servico_chave"]) & (el["canal"] == "telefone_156")
           & el["encerrada"]]["tempo_dias"]
    ref = stats.mannwhitneyu(x, y, method="asymptotic", use_continuity=True).pvalue
    assert lin["p_tempo"] == pytest.approx(ref)
    assert lin["delta_cliff"] == pytest.approx(E.cliff(x.to_numpy(), y.to_numpy())["delta"])


def test_comparacao_ingenua_existe_e_omnibus_por_servico(base_sintetica):
    r = E.analisar(base_sintetica, C.Parametros(min_celula=30))
    assert r["comparacao_ingenua"]["tempo"]["gl"] == 3
    assert r["comparacao_ingenua"]["proporcao"]["teste"] == "qui2"
    assert len(r["omnibus_por_servico"]) == 3  # 3 serviços com 4 canais cada


def test_sensibilidade_e_pressupostos(base_sintetica):
    r = E.analisar(base_sintetica, C.Parametros(min_celula=30))
    assert set(r["sensibilidade_horizonte"]["horizonte_dias"]) == {30, 180}
    assert "independencia" in r["pressupostos"]
