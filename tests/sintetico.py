"""Gerador de CSVs SINTÉTICOS com o esquema real da PBH (só para testes).

Nenhum dado real ou pessoal. Os campos de endereço levam marcadores óbvios
(``ENDERECO_FICTICIO_*``, coordenadas ``-1.0, -1.0``) para que os testes provem que
eles não chegam à base analítica nem a nenhuma saída.

Efeitos plantados: Telefone 156 mais lento; Presencial encerra bem menos;
PBH APP um pouco mais rápido que o Portal.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import numpy as np

MARCADOR_ENDERECO = "ENDERECO_FICTICIO"
CABECALHO = ["Id Ticket", "Nome Servico", "Data de criação (YYYY-MM-DD)",
             "Data de encerramento (YYYY-MM-DD)", "Fase Atual", "Situacao Atendimento Atual",
             "Canal Captacao", "Orgao Normatizador", "Orgao Responsavel", "Nome Logradouro",
             "Numero Logradouro", "Bairro", "Regional", "Coordenadas", "Ind Tp Pbh App",
             "Nivel Acesso"]
SERVICOS = ["Serviço Alfa – Teste", "Serviço Beta", "Serviço Gama (Fiscalização)"]
CANAIS = ["Portal", "Portal Mobile", "Telefônico", "Presencial"]
# (mediana de dias, prob. de encerrar) por canal
PERFIL = {"Portal": (4, 0.95), "Portal Mobile": (3, 0.95), "Telefônico": (20, 0.95),
          "Presencial": (6, 0.15)}


def _linha(i, serv, canal, criacao, enc, fase, situ, fmt, rotulo_pref="a"):
    def f(d):
        if d is None:
            return ""
        return d.strftime("%Y-%m-%d") if fmt == "iso" else d.strftime("%d/%m/%Y")
    return [f"{rotulo_pref}{i:023x}", serv, f(criacao), f(enc), fase, situ, canal,
            "PMBH / TESTE", "PMBH > TESTE", f"{MARCADOR_ENDERECO} RUA {i}", str(i % 500),
            f"{MARCADOR_ENDERECO}_BAIRRO", "CENTRO-SUL", "-1.0, -1.0", "Sim", "Restrito"]


def gerar_linhas(semente: int, n: int, inicio: date, dias_janela: int, fmt: str,
                 prefixo: str, corte: date) -> list[list[str]]:
    rng = np.random.default_rng(semente)
    linhas = []
    for i in range(n):
        serv = SERVICOS[i % len(SERVICOS)]
        canal = CANAIS[rng.integers(0, 4)]
        criacao = inicio + timedelta(days=int(rng.integers(0, dias_janela)))
        mediana, p_enc = PERFIL[canal]
        if rng.random() < p_enc:
            dias = int(rng.exponential(mediana / 0.69))
            enc = min(criacao + timedelta(days=dias), corte)
            linhas.append(_linha(i, serv, canal, criacao, enc, "Encerrado", "Serviço realizado",
                                 fmt, prefixo))
        else:
            fase = "Em andamento" if rng.random() < 0.8 else "Novo"
            linhas.append(_linha(i, serv, canal, criacao, None, fase, "Em andamento", fmt, prefixo))
    return linhas


def escrever_csv(caminho: Path, linhas, encoding: str) -> None:
    def esc(v):
        return f'"{v}"' if (";" in v or '"' in v) else v
    texto = ";".join(CABECALHO) + "\n" + "\n".join(";".join(esc(c) for c in l) for l in linhas) + "\n"
    caminho.write_bytes(texto.encode(encoding, errors="replace"))


def gerar_pasta(pasta: Path, n: int = 4000, com_casos_ruins: bool = True) -> list[Path]:
    """Cria dois CSVs (2021 em cp1252/ISO; jan/2023 em UTF-8 com BOM e DD/MM/AAAA)."""
    pasta.mkdir(parents=True, exist_ok=True)
    corte = date(2023, 7, 25)
    a = gerar_linhas(1, n, date(2021, 1, 1), 360, "iso", "a", corte)
    b = gerar_linhas(2, n, date(2023, 1, 1), 31, "br", "b", corte)
    if com_casos_ruins:
        # linha com data de corte para fixar o último encerramento do arquivo
        b.append(_linha(900001, SERVICOS[0], "Portal", date(2023, 7, 1), corte, "Encerrado",
                        "Serviço realizado", "br", "c"))
        casos = [
            # duplicata exata de Id Ticket (arquivo mais recente prevalece)
            b[0][:],
            # data de criação impossível
            _linha(900002, SERVICOS[1], "Portal", date(2023, 1, 5), None, "Em andamento", "x", "br", "c"),
            # encerrada sem data
            _linha(900003, SERVICOS[1], "Portal", date(2023, 1, 5), None, "Encerrado", "x", "br", "c"),
            # aberta com data de encerramento
            _linha(900004, SERVICOS[1], "Portal", date(2023, 1, 5), date(2023, 1, 9),
                   "Em andamento", "x", "br", "c"),
            # encerramento antes da criação
            _linha(900005, SERVICOS[1], "Portal", date(2023, 1, 9), date(2023, 1, 5),
                   "Encerrado", "x", "br", "c"),
            # canal ausente
            _linha(900006, SERVICOS[1], "", date(2023, 1, 5), date(2023, 1, 6), "Encerrado",
                   "x", "br", "c"),
            # canal sem significado documentado
            _linha(900007, SERVICOS[1], "Integração entre Sistemas", date(2023, 1, 5),
                   date(2023, 1, 5), "Encerrado", "x", "br", "c"),
            # fase desconhecida
            _linha(900008, SERVICOS[1], "Portal", date(2023, 1, 5), None, "Cancelado?", "x", "br", "c"),
        ]
        casos[1][2] = "31/02/2023"
        b.extend(casos)
    escrever_csv(pasta / "dadosabertos_bhdigital_2021.csv", a, "cp1252")
    escrever_csv(pasta / "dadosabertos_bhdigital_2023_jan.csv", b, "utf-8-sig")
    return [pasta / "dadosabertos_bhdigital_2021.csv", pasta / "dadosabertos_bhdigital_2023_jan.csv"]


def pacote_ckan(caminhos: list[Path], destino: Path, licenca: str = "cc-by",
                tamanho_errado: bool = False) -> Path:
    """Escreve um JSON no formato do ``package_show`` apontando para arquivos locais."""
    recursos = []
    for i, c in enumerate(caminhos):
        tam = c.stat().st_size + (7 if tamanho_errado else 0)
        recursos.append({"id": f"r{i}", "name": c.stem, "format": "CSV", "size": tam,
                         "url": c.as_uri(), "last_modified": "2023-07-25T00:00:00"})
    recursos.append({"id": "pdf", "name": "dicionario", "format": "PDF", "size": 1,
                     "url": "file:///nada.pdf"})
    pacote = {"success": True, "result": {"title": "Sintético", "license_id": licenca,
                                          "maintainer": "teste", "metadata_modified": "x",
                                          "resources": recursos}}
    destino.write_text(json.dumps(pacote), encoding="utf-8")
    return destino
