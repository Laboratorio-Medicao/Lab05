"""Testes do validador (issue #25): erros plantados em dados SINTÉTICOS."""

import pytest

import esquema as E
import gerar_dados_sinteticos as G
import validar_dados as V


@pytest.fixture()
def texto():
    dados = G.gerar(E.SEMENTE)
    return {t: dados[t].astype(str) for t in E.TABELAS_CSV}


def _regras_com_erro(tabelas, sintetico=True):
    return {(a.tabela, a.regra) for a in V.validar_tabelas(tabelas, sintetico)
            if a.nivel == "erro"}


def _linha_valida(t, filtro=None):
    s = t["sessoes"]
    validos = set(t["participantes"].query("valida == '1'")["participante"])
    m = s["participante"].isin(validos)
    if filtro is not None:
        m &= filtro(s)
    return s.index[m][0]


def test_dados_sinteticos_limpos_passam(texto):
    assert _regras_com_erro(texto) == set()


def test_pega_tempo_acima_do_teto(texto):
    i = _linha_valida(texto)
    texto["sessoes"].loc[i, "tempo_s"] = "301"
    assert ("sessoes", "tempo") in _regras_com_erro(texto)


def test_pega_teto_sem_motivo(texto):
    i = _linha_valida(texto, lambda s: s["motivo_fim"] == "teto")
    texto["sessoes"].loc[i, "tempo_s"] = "250.0"
    assert ("sessoes", "teto") in _regras_com_erro(texto)


def test_pega_ajuda_com_conclusao(texto):
    i = _linha_valida(texto, lambda s: s["motivo_fim"] == "concluida")
    texto["sessoes"].loc[i, "pediu_ajuda"] = "1"
    assert ("sessoes", "ajuda") in _regras_com_erro(texto)


def test_pega_tarefa_faltando(texto):
    i = _linha_valida(texto)
    texto["sessoes"] = texto["sessoes"].drop(index=i)
    assert ("sessoes", "completude") in _regras_com_erro(texto)


def test_pega_sequencia_incoerente(texto):
    p = texto["participantes"]
    i = p.index[(p["valida"] == "1") & (p["sequencia"] == "1")][0]
    p.loc[i, "sequencia"] = "3"  # celular-A vira computador-A/celular-B
    assert ("sessoes", "sequencia") in _regras_com_erro(texto)


def test_pega_sus_fora_do_dominio(texto):
    texto["sus"].loc[texto["sus"].index[0], "item_4"] = "6"
    assert ("sus", "dominio") in _regras_com_erro(texto)


def test_pega_seq_fora_do_dominio(texto):
    texto["sessoes"].loc[texto["sessoes"].index[0], "seq"] = "8"
    assert ("sessoes", "dominio") in _regras_com_erro(texto)


def test_pega_passo_fora_do_catalogo(texto):
    ps = texto["passos"]
    i = ps.index[ps["passo_id"] != E.PASSO_FORA][0]
    ps.loc[i, "passo_id"] = "p9"
    assert ("passos", "catalogo") in _regras_com_erro(texto)


def test_pega_soma_de_erros_diferente(texto):
    ps = texto["passos"]
    i = ps.index[ps["alcancado"] == "1"][0]
    ps.loc[i, "n_erros"] = str(int(ps.loc[i, "n_erros"]) + 1)
    assert ("passos", "soma_erros") in _regras_com_erro(texto)


def test_pega_coluna_proibida(texto):
    texto["participantes"]["nome_completo"] = "x"
    assert ("participantes", "dado_pessoal") in _regras_com_erro(texto)


def test_pega_email_em_texto_livre(texto):
    p = texto["participantes"]
    p.loc[p.index[0], "notas_moderador"] = "contato fulano@exemplo.com"
    assert ("participantes", "dado_pessoal") in _regras_com_erro(texto)


def test_pega_falha_tecnica_em_valido(texto):
    i = _linha_valida(texto, lambda s: s["motivo_fim"] == "abandono")
    texto["sessoes"].loc[i, "motivo_fim"] = "falha_tecnica"
    assert ("sessoes", "falha_tecnica") in _regras_com_erro(texto)


def test_pega_indeterminado_sem_motivo(texto):
    c = texto["catalogo_passos"]
    i = c.index[c["rotulo_wcag"] == "indeterminado"][0]
    c.loc[i, "motivo_indeterminado"] = ""
    assert ("catalogo_passos", "coerencia") in _regras_com_erro(texto)


def test_pega_mistura_de_origem(texto):
    texto["sus"].loc[texto["sus"].index[0], "origem"] = "real"
    assert ("*", "origem") in _regras_com_erro(texto)


def test_pega_origem_incoerente_com_nome_do_arquivo(texto):
    assert ("*", "origem") in _regras_com_erro(texto, sintetico=False)


def test_checksum_detecta_bruto_alterado(tmp_path):
    pasta = tmp_path / "sint"
    G.gravar(G.gerar(3), pasta)
    achados, sintetico = V.validar(pasta)
    assert sintetico and not [a for a in achados if a.nivel == "erro"]
    arq = pasta / "SINTETICO_sus.csv"
    arq.write_text(arq.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    achados, _ = V.validar(pasta)
    assert any(a.regra == "integridade" and a.nivel == "erro" for a in achados)


def test_relatorio_avisa_que_nao_e_verificado(tmp_path):
    pasta = tmp_path / "sint"
    G.gravar(G.gerar(3), pasta)
    achados, sintetico = V.validar(pasta)
    rel = V.formatar_relatorio(achados, pasta, sintetico)
    assert "Verificado" in rel and "SINTÉTICOS" in rel
