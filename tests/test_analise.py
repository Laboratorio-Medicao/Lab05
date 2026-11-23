"""Testes da análise (issue #25). Todos os dados aqui são SINTÉTICOS."""

import math

import numpy as np
import pandas as pd
import pytest

import analise as A
import esquema as E
import gerar_dados_sinteticos as G


@pytest.fixture(scope="module")
def sinteticos():
    dados = G.gerar(E.SEMENTE)
    texto = {t: dados[t].astype(str) for t in E.TABELAS_CSV}
    return E.tipar(texto)


# --- estatísticas conferidas à mão -----------------------------------------

def test_holm_valor_conhecido():
    assert A.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_holm_teto_e_monotonia():
    assert A.holm([0.5, 0.6, 0.01]) == pytest.approx([1.0, 1.0, 0.03])


def test_d_z_a_mao():
    # média 2, DP (ddof=1) 1
    assert A.d_z([1, 2, 3]) == pytest.approx(2.0)


def test_wilcoxon_r_e_rank_biserial_a_mao():
    # dif = [1, 2, 3, -1, 0]: o zero sai (wilcox); |dif| = 1, 2, 3, 1
    # postos 1,5; 3; 4; 1,5 -> T+ = 8,5 e T- = 1,5; n_nz = 4
    # E[T] = 4·5/4 = 5; Var = 4·5·9/24 − (2³−2)/48 = 7,5 − 0,125 = 7,375
    # Z (pelo menor T) = (1,5 − 5)/√7,375; sinal positivo porque T+ > T-
    z = abs((1.5 - 5) / math.sqrt(7.375))
    r = A.wilcoxon_pareado([1, 2, 3, -1, 0])
    assert r["n_nz"] == 4 and r["n_zeros"] == 1
    assert r["T_mais"] == 8.5 and r["T_menos"] == 1.5
    assert r["z"] == pytest.approx(z)
    assert r["r"] == pytest.approx(z / 2)
    assert r["rank_biserial"] == pytest.approx((8.5 - 1.5) / 10)


def test_wilcoxon_sinal_negativo():
    r = A.wilcoxon_pareado([-1, -2, -3, 1])
    assert r["r"] < 0 and r["rank_biserial"] < 0


def test_wilcoxon_todas_nulas():
    r = A.wilcoxon_pareado([0, 0, 0])
    assert r["p"] == 1.0 and math.isnan(r["r"])


def test_escore_sus():
    assert A.escore_sus([3] * 10)[0] == 50.0
    assert A.escore_sus([5, 1] * 5)[0] == 100.0
    assert A.escore_sus([1, 5] * 5)[0] == 0.0
    # ímpares 4,4,4,4,4 -> 3 cada = 15; pares 2,2,2,2,2 -> 3 cada = 15; 30·2,5 = 75
    assert A.escore_sus([4, 2] * 5)[0] == 75.0


def test_permutacao_exata_valor_conhecido():
    # d = [1, 1, 1]: só os sinais todos + ou todos − atingem |média| = 1 -> 2/8
    r = A.permutacao_sinais([1.0, 1.0, 1.0])
    assert r["p"] == pytest.approx(0.25) and r["metodo"].startswith("exato")


def test_permutacao_exata_vs_sorteios():
    d = np.array([0.3, 0.1, -0.05, 0.2, 0.25, -0.1, 0.15, 0.05, 0.4, 0.0])
    exato = A.permutacao_sinais(d)
    mc = A.permutacao_sinais(d, n_sorteios=20_000, exato_ate=0)
    assert exato["metodo"].startswith("exato") and mc["metodo"].startswith("Monte")
    assert abs(exato["p"] - mc["p"]) < 0.01


def test_bootstrap_reprodutivel():
    x = np.arange(10.0)
    assert A.bootstrap_media(x) == A.bootstrap_media(x)
    lo, hi = A.bootstrap_media(x)
    assert lo < x.mean() < hi


# --- seleção da amostra (P2) -----------------------------------------------

def _participantes(contagens, piloto=0, invalidos=()):
    linhas, ordem = [], 0
    for seq, n in contagens.items():
        for i in range(n):
            ordem += 1
            linhas.append({"participante": f"P{ordem:02d}", "sequencia": seq, "bloco": i + 1,
                           "ordem_realizacao": ordem, "valida": True, "piloto": False})
    df = pd.DataFrame(linhas)
    df.loc[df["participante"].isin(invalidos), "valida"] = False
    return df


def test_p2_oito_primeiros():
    p = _participantes({1: 9, 2: 8, 3: 8, 4: 8})
    sel = A.selecionar_amostra(p, "p2_provisoria")
    assert sel["k"] == 8 and len(sel["ids"]) == 32
    assert "P09" not in sel["ids"]  # 9º da sequência 1, por ordem de realização
    assert sel["fora"]["P09"].startswith("excedente")


def test_p2_k_blocos_completos():
    p = _participantes({1: 8, 2: 6, 3: 8, 4: 7})
    sel = A.selecionar_amostra(p, "p2_provisoria")
    assert sel["k"] == 6 and len(sel["ids"]) == 24
    ok = p[p["participante"].isin(sel["ids"])]
    assert (ok.groupby("sequencia").size() == 6).all()


def test_p2_invalido_e_piloto_ficam_fora():
    p = _participantes({1: 9, 2: 8, 3: 8, 4: 8}, invalidos=("P02",))
    p.loc[p["participante"] == "P01", "piloto"] = True
    sel = A.selecionar_amostra(p, "p2_provisoria")
    assert sel["k"] == 7  # seq 1 ficou com 7 analisáveis
    assert sel["fora"]["P01"] == "piloto" and sel["fora"]["P02"] == "sessão inválida"


def test_p2_blocos_por_id():
    p = _participantes({1: 3, 2: 3, 3: 2, 4: 3})  # bloco 3 sem a sequência 3
    sel = A.selecionar_amostra(p, "blocos_completos_por_id")
    assert sel["k"] == 2 and len(sel["ids"]) == 8


# --- variantes de P1 --------------------------------------------------------

def _sessoes_p1():
    base = {"dispositivo": "celular", "concluida": False, "pediu_ajuda": False}
    return pd.DataFrame([
        {**base, "participante": "P01", "tarefa_id": "A1", "motivo_fim": "concluida",
         "tempo_s": 100.0, "concluida": True},
        {**base, "participante": "P01", "tarefa_id": "A2", "motivo_fim": "abandono", "tempo_s": 50.0},
        {**base, "participante": "P01", "tarefa_id": "A3", "motivo_fim": "ajuda", "tempo_s": 80.0,
         "pediu_ajuda": True},
    ])


def test_p1_variantes():
    s = _sessoes_p1()
    assert list(A.tempo_tratado(s, "teto_300")["tempo_s"]) == [100.0, 300.0, 300.0]
    assert list(A.tempo_tratado(s, "tempo_registrado")["tempo_s"]) == [100.0, 50.0, 80.0]
    assert list(A.tempo_tratado(s, "excluir_tarefa")["tempo_s"]) == [100.0]
    with pytest.raises(ValueError):
        A.tempo_tratado(s, "outra")


# --- RQ4: regra de exclusão -------------------------------------------------

def test_rq4_regra_de_exclusao():
    cat = pd.DataFrame([
        {"tarefa_id": "A1", "passo_id": "p1", "dispositivo": "celular", "rotulo_wcag": "sem_violacao_detectada"},
        {"tarefa_id": "A1", "passo_id": "p2", "dispositivo": "celular", "rotulo_wcag": "com_violacao"},
        {"tarefa_id": "A1", "passo_id": "p3", "dispositivo": "celular", "rotulo_wcag": "indeterminado"},
    ])

    def passo(p, pid, alc, n):
        return {"participante": p, "dispositivo": "celular", "tarefa_id": "A1",
                "passo_id": pid, "alcancado": alc, "n_erros": n}

    passos = pd.DataFrame([
        passo("P01", "p1", True, 0), passo("P01", "p2", True, 2), passo("P01", "p3", True, 5),
        passo("P02", "p1", True, 1), passo("P02", "p2", False, 0),       # sem passo com violação
        passo("P03", "p1", True, 0), passo("P03", "p2", True, 1),
        passo("P03", E.PASSO_FORA, True, 4),                              # fora do caminho: ignorado
    ])
    w = A.taxas_rq4(passos, cat, ["P01", "P02", "P03", "P04"])
    assert bool(w.loc["P01", "elegivel"]) and w.loc["P01", "d"] == pytest.approx(2.0)
    assert not w.loc["P02", "elegivel"]
    assert w.loc["P02", "motivo_exclusao"] == "nenhum passo com violação alcançado"
    assert w.loc["P04", "motivo_exclusao"] == "nenhum passo alcançado em nenhum dos grupos"
    assert w.loc["P03", "err_sem"] == 0 and w.loc["P03", "d"] == pytest.approx(1.0)
    # o indeterminado (5 erros de P01) não entra em nenhum grupo
    assert w.loc["P01", "err_com"] == 2 and w.loc["P01", "err_sem"] == 0


# --- efeito plantado e chave da RQ4 ----------------------------------------

def test_efeito_plantado_detectado(sinteticos):
    res = A.analisar(sinteticos, "sintetico")
    assert res["amostra"]["n"] == 32
    assert res["rq1"]["p_holm"] < 0.05 and res["rq1"]["primario"]["r"] < 0
    assert res["rq2"]["p_holm"] < 0.05 and res["rq2"]["razao_medias_geometricas"] > 1
    assert res["rq3"]["p_holm"] < 0.05 and res["rq3"]["primario"]["d_z"] < 0
    assert res["rq4"]["media_d_i"] > 0 and res["rq4"]["primario_exploratorio"]["p"] < 0.05
    assert res["aviso"] == A.AVISO_SINTETICO
    assert "PENDENTE" in res["parametros"]["p1"]["status"]
    assert "PENDENTE" in res["parametros"]["p2"]["status"]
    # sensibilidade "tempo registrado" se aproxima do efeito plantado (≈ 1,42) melhor que o teto
    sens = res["sensibilidades"]["p1"]["tempo_registrado"]["razao_medias_geometricas"]
    assert abs(sens - math.exp(G.EFEITOS_PLANTADOS["log_tempo_celular"])) < 0.25


def test_rq4_teste_desligavel(sinteticos):
    res = A.analisar(sinteticos, "sintetico", rq4_teste=False)
    assert "primario_exploratorio" not in res["rq4"]
    assert res["rq4"]["teste"].startswith("desligado")


def test_holm_so_tres_primarios(sinteticos):
    res = A.analisar(sinteticos, "sintetico")
    assert res["holm"]["familia"] == ["RQ1", "RQ2", "RQ3"]
    assert len(res["holm"]["p"]) == 3


# --- recusa de mistura e de destino ----------------------------------------

def test_recusa_mistura_origem(sinteticos):
    t = {k: v.copy() for k, v in sinteticos.items()}
    t["sus"].loc[t["sus"].index[0], "origem"] = "real"
    with pytest.raises(E.ErroDeDados):
        A.analisar(t, "sintetico")


def test_recusa_origem_incoerente_com_nome(sinteticos):
    with pytest.raises(E.ErroDeDados):
        A.analisar(sinteticos, "real")


def test_recusa_pasta_com_arquivos_das_duas_origens(tmp_path):
    (tmp_path / "SINTETICO_sessoes.csv").write_text("x\n")
    (tmp_path / "sessoes.csv").write_text("x\n")
    with pytest.raises(E.ErroDeDados):
        E.detectar_sintetico(tmp_path)


def test_sintetico_nunca_em_resultados(tmp_path):
    with pytest.raises(E.ErroDeDados):
        A.verificar_destino(tmp_path / "resultados", sintetico=True)
    with pytest.raises(E.ErroDeDados):
        G.gravar(G.gerar(1), tmp_path / "resultados" / "x")
    with pytest.raises(E.ErroDeDados):
        A.verificar_destino(tmp_path / "dados" / "sinteticos", sintetico=False)


def test_ponta_a_ponta_em_pasta_temporaria(tmp_path):
    G.gravar(G.gerar(7), tmp_path / "sint")
    tabelas, sintetico, origem = A.preparar(tmp_path / "sint")
    assert sintetico and origem == "sintetico"
    res = A.analisar(tabelas, origem)
    aud = A.analisar_auditoria(tmp_path / "sint", sintetico)
    escritos = A.gravar_saidas(res, aud, tmp_path / "saida", sintetico)
    assert all(f.name.startswith(E.PREFIXO_SINTETICO) for f in escritos)
    assert aud["top10_regras_wcag"] and "lighthouse" in aud


# --- leitor do axe ----------------------------------------------------------

def test_axe_formatos_aceitos():
    core = {"violations": [{"id": "label", "impact": "critical", "tags": ["wcag2a"],
                            "nodes": [{}, {}]}]}
    assert A.normalizar_axe(core) == [{"regra": "label", "impacto": "critical",
                                       "tags": ["wcag2a"], "n_nos": 2}]
    assert len(A.normalizar_axe([core, core])) == 2
    ext = {"allIssues": [{"ruleId": "label", "impact": "critical"},
                         {"ruleId": "label", "impact": "critical"}]}
    assert A.normalizar_axe(ext)[0]["n_nos"] == 2
    with pytest.raises(ValueError):
        A.normalizar_axe({"outra": 1})
