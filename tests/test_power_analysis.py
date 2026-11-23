"""Testes da simulação de poder v4 (scripts/power_analysis.py)."""

import sys
from pathlib import Path

import numpy as np
import pytest
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import power_analysis as pa  # noqa: E402


def _ep(p, R):
    return np.sqrt(p * (1 - p) / R)


def test_holm_valor_conhecido():
    p = np.array([0.01, 0.04, 0.03])
    np.testing.assert_allclose(pa.holm_ajustados(p)[0], [0.03, 0.06, 0.06])
    assert pa.holm_rejeicoes(p).tolist() == [[True, False, False]]
    # todos rejeitados quando cada p ordenado fica abaixo do seu limite
    assert pa.holm_rejeicoes(np.array([0.01, 0.02, 0.049])).tolist() == [[True, True, True]]


def test_holm_rejeicoes_coerentes_com_ajustados():
    rng = np.random.default_rng(1)
    p = rng.random((2000, 3)) * 0.1
    assert np.array_equal(pa.holm_rejeicoes(p), pa.holm_ajustados(p) <= pa.ALFA)


def test_wilcoxon_todas_dif_zero_da_p_1():
    assert pa.wilcoxon_pareado(np.zeros((3, 32), dtype=int)).tolist() == [1.0, 1.0, 1.0]


def test_wilcoxon_igual_ao_scipy():
    rng = np.random.default_rng(2)
    dif = rng.integers(-3, 4, size=(200, 32))
    dif[:, :10] = 0  # força zeros e empates
    nosso = pa.wilcoxon_pareado(dif)
    ref = [stats.wilcoxon(d, zero_method="wilcox", method="approx").pvalue for d in dif]
    np.testing.assert_allclose(nosso, ref, rtol=1e-10, atol=1e-12)


def test_t_pareado_igual_ao_scipy():
    rng = np.random.default_rng(3)
    x, y = rng.standard_normal((2, 50, 32))
    np.testing.assert_allclose(pa.t_pareado(x - y), stats.ttest_rel(x, y, axis=1).pvalue)


def test_oito_por_sequencia():
    seq = pa.alocar_sequencias(pa.CONTAGENS["n32"])
    assert seq.size == 32
    assert np.bincount(seq).tolist() == [8, 8, 8, 8]
    g, h, _ = pa._indicadores(seq)
    assert g.sum() == 0 and h.sum() == 0  # conjunto e período balanceados


@pytest.mark.parametrize("cenario", ["S0", "S1", "S2"])
def test_interceptos_mantem_conclusao_marginal(cenario):
    R = 6000
    sim = pa.simular(np.random.default_rng(4), R, pa.CONTAGENS["n32"], cenario, dp_u=1.0)
    tol = 4 * np.sqrt(0.9 * 0.1 / (R * 32 * 3)) + 0.004  # inclui ruído por replicação
    assert abs(sim["conclusao_marginal"]["computador"] - 0.90) < tol
    assert abs(sim["conclusao_marginal"]["celular"] - 0.75) < tol + 0.003


def test_dz_efetivo_analitico_bate_com_alvos():
    for cen, alvo in pa.DZ_EFETIVO_ALVO.items():
        assert pa.dz_efetivo_analitico(cen) == pytest.approx(alvo, abs=1e-12)


@pytest.mark.parametrize("cenario", ["S1", "S2"])
def test_dz_efetivo_analitico_proximo_do_empirico(cenario):
    sim = pa.simular(np.random.default_rng(5), 20000, pa.CONTAGENS["n32"], cenario, dp_u=1.0)
    for rq in ("RQ2", "RQ3"):
        assert sim["dz_empirico_agregado"][rq] == pytest.approx(
            pa.dz_efetivo_analitico(cenario), abs=0.015)


def test_poder_t_sem_ajuste_s0_igual_ao_analitico():
    R = 20000
    analitico = pa.poder_t_nao_central(0.6, 32)
    assert analitico == pytest.approx(0.908, abs=0.001)
    sim = pa.simular(np.random.default_rng(6), R, pa.CONTAGENS["n32"], "S0", dp_u=1.0)
    res = pa.resumir(sim["p"])
    for rq in ("RQ2", "RQ3"):
        assert abs(res["sem_ajuste"][rq] - analitico) < 4 * _ep(analitico, R)


def test_tipo_i_sob_h0_balanceado_s0():
    R = 20000
    sim = pa.simular(np.random.default_rng(7), R, pa.CONTAGENS["n32"], "S0", dp_u=1.0,
                     sob_h0=True)
    res = pa.resumir(sim["p"])
    lim = 4 * _ep(0.05, R)
    for rq in ("RQ2", "RQ3"):
        assert abs(res["sem_ajuste"][rq] - 0.05) < lim
    # Wilcoxon com aproximação normal em dados discretos: tolerância um pouco maior
    assert abs(res["sem_ajuste"]["RQ1"] - 0.05) < lim + 0.005
    assert res["pelo_menos_uma_rejeicao_holm"] <= 0.05 + lim


def test_mesma_semente_mesmo_resultado():
    a = pa.simular(np.random.default_rng(8), 500, pa.CONTAGENS["n24"], "S1", dp_u=1.0)
    b = pa.simular(np.random.default_rng(8), 500, pa.CONTAGENS["n24"], "S1", dp_u=1.0)
    assert np.array_equal(a["p"], b["p"])


def test_executar_rapido_e_reprodutivel():
    r1 = pa.executar(R=300, R_cal=1000)
    r2 = pa.executar(R=300, R_cal=1000)
    assert r1["calibracao"]["dp_u"] == r2["calibracao"]["dp_u"]
    assert r1["poder_n32"]["S1"]["com_holm"] == r2["poder_n32"]["S1"]["com_holm"]
    assert set(r1["comparacao_citado_reproduzido_poder"]) == {"S0", "S1", "S2"}
    assert "não é resultado" in r1["aviso"].lower() or "NÃO é resultado" in r1["aviso"]
