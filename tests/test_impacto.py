"""Testes do módulo de estimativa de impacto (issue #29), só com dados sintéticos."""

import numpy as np
import pandas as pd
import pytest

import impacto as I


def _pares():
    return pd.DataFrame([
        dict(servico="S1", canal_a="portal_servicos", canal_b="telefone_156", n_a=200, n_b=100,
             taxa_a=0.9, taxa_b=0.8, mediana_a=3.0, mediana_b=10.0),
        dict(servico="S2", canal_a="portal_servicos", canal_b="telefone_156", n_a=600, n_b=300,
             taxa_a=0.5, taxa_b=0.5, mediana_a=2.0, mediana_b=3.0),
        dict(servico="S3", canal_a="portal_servicos", canal_b="presencial", n_a=100, n_b=100,
             taxa_a=0.9, taxa_b=0.1, mediana_a=1.0, mediana_b=9.0),
        dict(servico="S4", canal_a="portal_servicos", canal_b="telefone_156", n_a=100, n_b=40,
             taxa_a=1.0, taxa_b=0.5, mediana_a=np.nan, mediana_b=5.0)])


def test_anos_coorte():
    el = pd.DataFrame({"data_criacao": pd.to_datetime(["2020-01-01", "2020-12-31"])})
    assert I.anos_coorte(el) == pytest.approx(366 / 365.25)


def test_impacto_por_servico_exclui_presencial_e_calcula():
    s = I.impacto_por_servico(_pares(), anos=2.0).set_index("servico")
    assert "S3" not in s.index
    assert s.loc["S1", "vol_b_ano"] == 50
    assert s.loc["S1", "dif_mediana_dias"] == 7
    assert s.loc["S1", "dias_solicitacao_ano"] == 350
    assert s.loc["S1", "encerradas_90d_ano"] == pytest.approx(5.0)
    assert np.isnan(s.loc["S4", "dias_solicitacao_ano"])


def test_impacto_por_par_ponderado_e_ic():
    s = I.impacto_por_servico(_pares(), anos=2.0)
    par = I.impacto_por_par(s, semente=1).set_index(["canal_a", "canal_b"]).loc[("portal_servicos", "telefone_156")]
    assert par["servicos"] == 3
    assert par["dif_mediana_ponderada_dias"] == pytest.approx((50 * 7 + 150 * 1) / 200)
    assert par["dias_solicitacao_ano"] == pytest.approx(500)
    assert par["encerradas_90d_ano"] == pytest.approx(5.0 + 0 + 20 * 0.5)
    lo, hi = par["dias_solicitacao_ano_ic_lo"], par["dias_solicitacao_ano_ic_hi"]
    assert np.isfinite(lo) and np.isfinite(hi) and lo <= hi


def test_bootstrap_deterministico_e_um_servico():
    s = I.impacto_por_servico(_pares(), anos=2.0)
    assert I.impacto_por_par(s, semente=7).equals(I.impacto_por_par(s, semente=7))
    um = I.impacto_por_par(s[s.servico == "S1"], semente=7).iloc[0]
    assert um["dias_solicitacao_ano_ic_lo"] == um["dias_solicitacao_ano_ic_hi"] == 350


def test_dois_servicos_identicos_dao_ic_de_largura_zero():
    # o bootstrap reamostra serviços inteiros: com dois serviços idênticos, toda reamostra soma o mesmo
    p = _pares()
    dois = pd.concat([p[p.servico == "S1"], p[p.servico == "S1"].assign(servico="S1b")])
    s = I.impacto_por_servico(dois, anos=2.0)
    par = I.impacto_por_par(s, semente=3).iloc[0]
    for m in I.METRICAS:
        assert par[f"{m}_ic_lo"] == par[f"{m}_ic_hi"] == par[m]
    assert par["servicos"] == 2 and par["dias_solicitacao_ano"] == 700


def test_volume_anual_por_canal():
    el = pd.DataFrame({"data_criacao": pd.to_datetime(["2020-05-11", "2020-06-01", "2021-01-02"]),
                       "canal": ["pbh_app", "pbh_app", "pbh_app"]})
    v = I.volume_anual_por_canal(el).set_index("ano")
    assert v.loc[2020, "solicitacoes"] == 2 and v.loc[2020, "meses_cobertos"] == 2


def test_sentidos_opostos_de_tempo_e_taxa_ficam_explicitos():
    import visualizacao as V
    base = {"canal_a": "portal_servicos", "canal_b": "pbh_app", "servicos": 3}
    r = {"parametros": {"horizonte_dias": 90}, "coorte": {"inicio": "2020-01-01", "fim": "2020-12-31", "anos": 1.0}}
    r["impacto_por_par"] = pd.DataFrame([dict(base, dias_solicitacao_ano=-100.0, encerradas_90d_ano=5.0)])
    assert "sentidos opostos" in " ".join(V.sentidos_impacto(r))
    r["impacto_por_par"] = pd.DataFrame([dict(base, dias_solicitacao_ano=-100.0, encerradas_90d_ano=-5.0)])
    assert "sentidos opostos" not in " ".join(V.sentidos_impacto(r))
    assert "único par comparado" in " ".join(V.sentidos_impacto(r))
    r["impacto_por_par"] = pd.DataFrame([dict(base, dias_solicitacao_ano=-100.0, encerradas_90d_ano=-5.0),
                                         dict(base, canal_b="telefone_156", dias_solicitacao_ano=9.0,
                                              encerradas_90d_ano=2.0)])
    assert "nos 2 pares comparados" in " ".join(V.sentidos_impacto(r))


def test_sem_pares_nao_ha_frase_de_sentido_nem_de_exemplo():
    import visualizacao as V
    r = {"parametros": {"horizonte_dias": 90}, "coorte": {"inicio": "2020-01-01", "fim": "2020-12-31", "anos": 1.0},
         "impacto_por_par": pd.DataFrame(columns=I.COLUNAS_PAR)}
    assert V.sentidos_impacto(r) == []
    assert V._exemplo_sinal_impacto(r) == ""
    assert "neste resultado" not in V._texto_leitura_impacto(r)


def test_frase_do_sinal_vem_dos_dados_e_some_com_nan():
    import visualizacao as V
    base = {"canal_a": "portal_servicos", "canal_b": "telefone_156", "servicos": 3,
            "encerradas_90d_ano": 1.0}
    r = {"parametros": {"horizonte_dias": 90}, "coorte": {"inicio": "2020-01-01", "fim": "2020-12-31", "anos": 1.0}}
    r["impacto_por_par"] = pd.DataFrame([dict(base, dias_solicitacao_ano=50.0)])
    assert "Telefone 156 é mais lento que Portal de Serviços" in V._exemplo_sinal_impacto(r)
    r["impacto_por_par"] = pd.DataFrame([dict(base, dias_solicitacao_ano=np.nan)])
    assert V._exemplo_sinal_impacto(r) == ""