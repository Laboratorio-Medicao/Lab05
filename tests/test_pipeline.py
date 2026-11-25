"""Teste de ponta a ponta (CSV sintético → base → análise → gráficos), sem rede."""

import argparse
import gzip
import json

import pytest

import config as C
import pipeline as P
import sintetico as S


def _args(tmp_path, pasta_entrada, **kw):
    base = dict(cache_dir=None, entrada=str(pasta_entrada), base=None, horizonte_dias=90,
                min_celula=30, dados_dir=str(tmp_path / "dados"), saida=str(tmp_path / "res"))
    base.update(kw)
    return argparse.Namespace(**base)


@pytest.fixture(scope="module")
def execucao(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("e2e")
    S.gerar_pasta(tmp / "entrada", n=6000)
    saida = P.executar(_args(tmp, tmp / "entrada"), log=lambda *_: None)
    return tmp, saida


def test_gera_todas_as_saidas(execucao):
    tmp, saida = execucao
    esperados = [
        "dados/processados/solicitacoes_analiticas.csv.gz", "dados/manifesto_coleta.json",
        "dados/qualidade_dados.json", "res/resultados.json", "res/resumo.md", "res/painel.html",
        "res/tabelas/metricas_por_canal.csv", "res/tabelas/pares_ajustados_por_servico.csv",
        "res/tabelas/pares_por_servico.csv", "res/tabelas/funil_elegibilidade.csv",
    ]
    for rel in esperados:
        assert (tmp / rel).exists(), rel
    assert len(saida["figuras"]) == 6
    assert all(f.stat().st_size > 5000 for f in saida["figuras"])  # PNG não vazio


def test_nenhuma_saida_contem_endereco(execucao):
    tmp, _ = execucao
    for arq in list((tmp / "dados").rglob("*")) + list((tmp / "res").rglob("*")):
        if not arq.is_file() or arq.suffix == ".png":
            continue
        bruto = arq.read_bytes()
        texto = gzip.decompress(bruto).decode() if arq.suffix == ".gz" else bruto.decode("utf-8")
        assert S.MARCADOR_ENDERECO not in texto, arq
        assert "-1.0, -1.0" not in texto, arq


def test_manifesto_e_qualidade(execucao):
    tmp, _ = execucao
    man = json.loads((tmp / "dados/manifesto_coleta.json").read_text(encoding="utf-8"))
    assert len(man["recursos"]) == 2 and len(man["sha256_base_analitica"]) == 64
    q = json.loads((tmp / "dados/qualidade_dados.json").read_text(encoding="utf-8"))
    assert "nome logradouro" in q["colunas_descartadas_na_leitura"]
    assert q["status_registro"]["inconsistente"] == 6


def test_resumo_so_tem_numeros_calculados(execucao):
    tmp, saida = execucao
    texto = (tmp / "res/resumo.md").read_text(encoding="utf-8")
    pc = saida["resultado"]["por_canal"].set_index("canal")
    assert f"{int(pc.loc['portal_servicos', 'solicitacoes']):,}".replace(",", ".") in texto
    assert "Portal de Serviços × Telefone 156" in texto
    html = (tmp / "res/painel.html").read_text(encoding="utf-8")
    assert "<img" in html and "associação, não causa" in html


def test_so_analise_a_partir_da_base_reproduz_os_resultados(execucao, tmp_path):
    tmp, saida = execucao
    base = tmp / "dados/processados/solicitacoes_analiticas.csv.gz"
    args = _args(tmp_path, tmp / "entrada", entrada=None, base=str(base),
                 dados_dir=str(tmp / "dados"), saida=str(tmp_path / "res2"))
    outra = P.executar(args, log=lambda *_: None)
    a = saida["resultado"]["por_canal"].reset_index(drop=True)
    b = outra["resultado"]["por_canal"].reset_index(drop=True)
    assert a.equals(b)
    assert (tmp / "res/tabelas/metricas_por_canal.csv").read_text(encoding="utf-8") == \
        (tmp_path / "res2/tabelas/metricas_por_canal.csv").read_text(encoding="utf-8")


def test_recusa_entrada_dentro_do_repositorio(tmp_path):
    with pytest.raises(Exception, match="dentro do repositório"):
        P.executar(_args(tmp_path, C.RAIZ / "dados"), log=lambda *_: None)


def test_cli_retorna_erro_amigavel(tmp_path, capsys):
    rc = P.main(["--entrada", str(C.RAIZ / "dados"), "--saida", str(tmp_path)])
    assert rc == 1 and "ERRO" in capsys.readouterr().err
