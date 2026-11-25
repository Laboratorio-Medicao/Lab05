"""Testes da leitura, anonimização e tratamento (dados sintéticos)."""

import gzip

import numpy as np
import pandas as pd
import pytest

import config as C
import sintetico as S
import tratamento as T


@pytest.fixture(scope="module")
def pasta(tmp_path_factory):
    p = tmp_path_factory.mktemp("csv")
    return p, S.gerar_pasta(p)


@pytest.fixture(scope="module")
def processado(pasta):
    _, caminhos = pasta
    return T.processar(caminhos, log=lambda *_: None)


# --- leitura ---------------------------------------------------------------

def test_le_as_duas_codificacoes_e_acentos(pasta):
    _, (a, b) = pasta
    da, ia = T.ler_csv(a)
    db, ib = T.ler_csv(b)
    assert ia["codificacao"] == "cp1252" and ib["codificacao"] == "utf-8-sig"
    assert list(da.columns) == list(C.COLUNAS_ORIGEM.values())
    assert "Telefônico" in set(da["canal_original"])  # acento preservado no cp1252
    assert "Telefônico" in set(db["canal_original"])  # e no UTF-8 com BOM
    # o travessão não cabe no latin-1/cp1252 do gerador? cabe no cp1252: confere ida e volta
    assert any("Serviço Alfa" in s for s in da["servico"])


def test_colunas_de_endereco_nao_chegam_a_memoria(pasta):
    _, (a, _) = pasta
    df, info = T.ler_csv(a)
    assert set(df.columns) == set(C.COLUNAS_ORIGEM.values())
    for sensivel in C.COLUNAS_SENSIVEIS_CONHECIDAS:
        assert sensivel in info["colunas_descartadas"]
    assert not df.astype(str).apply(lambda c: c.str.contains(S.MARCADOR_ENDERECO)).any().any()


def test_coluna_obrigatoria_ausente_gera_erro(tmp_path):
    (tmp_path / "x.csv").write_text("Id Ticket;Nome Servico\n1;a\n", encoding="utf-8")
    with pytest.raises(T.ErroDeDados, match="ausentes"):
        T.ler_csv(tmp_path / "x.csv")


# --- anonimização ----------------------------------------------------------

def test_base_nao_tem_coluna_nem_valor_sensivel(processado):
    base, _ = processado
    assert set(base.columns) == set(C.COLUNAS_BASE)
    for col in base.columns:
        assert not any(t in col.lower() for t in C.TRECHOS_COLUNA_PROIBIDA)
    texto = base.astype(str).apply(lambda c: c.str.contains(S.MARCADOR_ENDERECO))
    assert not texto.any().any()


def test_id_e_pseudonimizado(processado):
    base, _ = processado
    assert base["id_hash"].str.fullmatch("[0-9a-f]{16}").all()
    assert not base["id_hash"].str.startswith("a0000").any()
    assert base["id_hash"].is_unique


def test_garantir_anonimato_rejeita_coluna_proibida(processado):
    base, _ = processado
    ruim = base.assign(coordenadas="x")
    with pytest.raises(T.ErroDeDados):
        T.garantir_anonimato(ruim)


def test_base_gravada_nao_contem_endereco(processado, tmp_path):
    base, _ = processado
    caminho = T.gravar_base(base, tmp_path / "b.csv.gz")
    conteudo = gzip.open(caminho, "rt", encoding="utf-8").read()
    assert S.MARCADOR_ENDERECO not in conteudo and "-1.0, -1.0" not in conteudo
    # bytes determinísticos
    outro = T.gravar_base(base, tmp_path / "c.csv.gz")
    assert caminho.read_bytes() == outro.read_bytes()
    volta = T.ler_base(caminho)
    assert len(volta) == len(base) and volta["comparavel"].dtype == bool


# --- canais ----------------------------------------------------------------

def test_normaliza_canais():
    s = pd.Series(["Portal", " portal mobile ", "TELEFÔNICO", "Presencial",
                   "Integração entre Sistemas", "Origem Interna", "E-mail", "Fax", None],
                  dtype="string")
    r = T.normalizar_canal(T.limpar_texto(s)).tolist()
    assert r[:7] == ["portal_servicos", "pbh_app", "telefone_156", "presencial",
                     "integracao_sistemas", "origem_interna", "email"]
    assert r[7] == C.CANAL_NAO_MAPEADO and pd.isna(r[8])


def test_canais_comparaveis(processado):
    base, q = processado
    assert set(base.loc[base["comparavel"], "canal"]) <= set(C.CANAIS_COMPARAVEIS)
    assert (base.loc[base["canal"] == "integracao_sistemas", "comparavel"] == False).all()  # noqa: E712
    assert q["canais_nao_mapeados"] == []


# --- datas -----------------------------------------------------------------

def test_parse_dos_dois_formatos_sem_ambiguidade():
    s = pd.Series(["2023-02-03", "03/02/2023", "31/02/2023", "2023-13-01", "texto", None],
                  dtype="string")
    d, inv = T.parse_data(s)
    assert d[0] == pd.Timestamp("2023-02-03") and d[1] == pd.Timestamp("2023-02-03")
    assert d[2:5].isna().all() and pd.isna(d[5])
    assert inv.tolist() == [False, False, True, True, True, False]  # ausente não é inválido


def test_datas_invalidas_contadas(processado):
    _, q = processado
    assert q["datas_invalidas"]["criacao"] == 1


# --- tempo e classificação -------------------------------------------------

def test_tempo_de_encerramento_e_status(processado):
    base, _ = processado
    enc = base[base["status_registro"] == "encerrada"]
    calc = (enc["data_encerramento"] - enc["data_criacao"]).dt.days
    assert (enc["tempo_dias"] == calc).all() and (enc["tempo_dias"] >= 0).all()
    # aberta e inconsistente NUNCA recebem tempo (nem 0)
    nao_enc = base[base["status_registro"] != "encerrada"]
    assert nao_enc["tempo_dias"].isna().all()
    ab = base[base["status_registro"] == "aberta"]
    assert len(ab) > 0 and ab["data_encerramento"].isna().all()


def test_motivos_de_inconsistencia(processado):
    base, q = processado
    m = q["motivos_inconsistencia"]
    assert m["criacao_invalida"] == 1
    assert m["encerrada_sem_data"] == 1
    assert m["aberta_com_data_encerramento"] == 1
    assert m["encerramento_anterior_a_criacao"] == 1
    assert m["canal_ausente"] == 1
    assert m["fase_desconhecida"] == 1
    assert q["status_registro"]["inconsistente"] == 6
    inc = base[base["status_registro"] == "inconsistente"]
    assert inc["motivo_inconsistencia"].notna().all()


def test_valores_ausentes_registrados(processado):
    _, q = processado
    assert q["ausentes_brutos"]["data_encerramento"] > 0
    assert q["ausentes_brutos"]["fase_atual"] == 0


def test_duplicatas_por_id(processado):
    base, q = processado
    assert q["duplicatas"]["removidas"] == 1
    assert q["duplicatas"]["ids_com_conteudo_conflitante"] == 0
    assert base["id_hash"].is_unique
    assert q["linhas_brutas"] - q["duplicatas"]["removidas"] == q["linhas_base"]


def test_duplicata_conflitante_fica_com_o_arquivo_mais_recente():
    cols = {c: ["x"] for c in C.COLUNAS_ORIGEM.values()}
    d1 = pd.DataFrame({**cols, "id_ticket": ["i1"], "fase_atual": ["Em andamento"],
                       "data_criacao": ["2023-01-02"], "data_encerramento": [None],
                       "canal_original": ["Portal"], "servico": ["S"]})
    d1.insert(0, "arquivo_origem", "antigo.csv")
    d2 = d1.assign(fase_atual="Encerrado", data_encerramento="2023-01-05", arquivo_origem="novo.csv")
    base, q = T.tratar(pd.concat([d1, d2], ignore_index=True))
    assert len(base) == 1 and q["duplicatas"]["ids_com_conteudo_conflitante"] == 1
    assert base.loc[0, "status_registro"] == "encerrada" and base.loc[0, "tempo_dias"] == 3


def test_chave_de_servico_ignora_acento_pontuacao_e_interrogacao():
    k = C.chave_texto
    assert k("Árvore ? Poda de Árvore") == k("Arvore – Poda de arvore")
    assert k("  Tapa-Buraco ") == "tapa buraco"


def test_nome_de_exibicao_prefere_variante_sem_interrogacao():
    s = pd.Series(["Árvore ? Poda", "Árvore ? Poda", "Árvore – Poda"], dtype="string")
    chave = s.map(C.chave_texto).astype("string")
    assert T._nome_exibicao(s, chave).iloc[0] == "Árvore – Poda"


def test_seguimento_usa_corte_por_arquivo(processado):
    base, q = processado
    assert q["corte_observacao_por_arquivo"]["dadosabertos_bhdigital_2023_jan.csv"] == "2023-07-25"
    b = base[base["arquivo_origem"] == "dadosabertos_bhdigital_2023_jan.csv"]
    ok = b[b["data_criacao"].notna()]
    esperado = (pd.Timestamp("2023-07-25") - ok["data_criacao"]).dt.days
    assert (ok["seguimento_dias"] == esperado).all()
