"""Testes da coleta (sem rede: usa file:// e arquivos sintéticos)."""

import time

import pytest

import coleta
import config as C
import sintetico as S


def _cliente():
    return coleta.Cliente(intervalo_s=0)


def test_listar_recursos_filtra_csv_e_confere_licenca(tmp_path):
    csvs = S.gerar_pasta(tmp_path / "origem")
    api = S.pacote_ckan(csvs, tmp_path / "pkg.json")
    meta = coleta.listar_recursos(_cliente(), api.as_uri())
    assert [r["arquivo"] for r in meta["recursos"]] == [
        "dadosabertos_bhdigital_2021.csv", "dadosabertos_bhdigital_2023_jan.csv"]
    assert meta["dataset"]["licenca"] == "cc-by"


def test_licenca_diferente_interrompe(tmp_path):
    csvs = S.gerar_pasta(tmp_path / "origem")
    api = S.pacote_ckan(csvs, tmp_path / "pkg.json", licenca="outra")
    with pytest.raises(coleta.ErroDeColeta, match="Licença"):
        coleta.listar_recursos(_cliente(), api.as_uri())


def test_download_confere_tamanho_e_reaproveita_cache(tmp_path):
    csvs = S.gerar_pasta(tmp_path / "origem")
    api = S.pacote_ckan(csvs, tmp_path / "pkg.json")
    destino = tmp_path / "cache"
    caminhos, man = coleta.coletar(destino, _cliente(), api.as_uri(), log=lambda *_: None)
    assert [p.name for p in caminhos] == [c.name for c in csvs]
    assert all(not r["do_cache"] for r in man["recursos"])
    assert all(len(r["sha256"]) == 64 for r in man["recursos"])
    _, man2 = coleta.coletar(destino, _cliente(), api.as_uri(), log=lambda *_: None)
    assert all(r["do_cache"] for r in man2["recursos"])


def test_tamanho_divergente_do_ckan_falha(tmp_path):
    csvs = S.gerar_pasta(tmp_path / "origem")
    api = S.pacote_ckan(csvs, tmp_path / "pkg.json", tamanho_errado=True)
    with pytest.raises(coleta.ErroDeColeta, match="declara"):
        coleta.coletar(tmp_path / "cache", _cliente(), api.as_uri(), log=lambda *_: None)


def test_recusa_pasta_de_brutos_dentro_do_repositorio():
    with pytest.raises(coleta.ErroDeColeta, match="dentro do repositório"):
        coleta.pasta_fora_do_repositorio(C.RAIZ / "dados" / "brutos")


def test_ordem_cronologica_dos_nomes():
    nomes = ["dadosabertos_bhdigital_2023_jun.csv", "dadosabertos_bhdigital_2021.csv",
             "dadosabertos_bhdigital_2020_mai-dez.csv", "dadosabertos_bhdigital_2023_jan.csv"]
    assert sorted(nomes, key=coleta.ordem_cronologica) == [
        "dadosabertos_bhdigital_2020_mai-dez.csv", "dadosabertos_bhdigital_2021.csv",
        "dadosabertos_bhdigital_2023_jan.csv", "dadosabertos_bhdigital_2023_jun.csv"]


def test_intervalo_minimo_entre_requisicoes(tmp_path):
    arq = tmp_path / "a.json"
    arq.write_text('{"ok": 1}')
    c = coleta.Cliente(intervalo_s=0.3)
    t0 = time.monotonic()
    c.json(arq.as_uri())
    c.json(arq.as_uri())
    assert time.monotonic() - t0 >= 0.3


def test_user_agent_identifica_o_projeto():
    assert "Lab05" in C.USER_AGENT and "Mozilla" not in C.USER_AGENT
    assert C.INTERVALO_MIN_REQUISICOES_S >= 1.0  # enunciado: no máximo 1 req/s
