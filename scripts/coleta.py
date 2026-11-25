"""Coleta dos dados abertos da PBH (CKAN) — LAB05.

Obtém, pela API oficial do CKAN, a lista de arquivos CSV do conjunto
"Solicitações dos cidadãos, por meio dos canais de atendimento da PBH" e baixa
cada um para uma pasta **fora do repositório**: os CSVs brutos contêm logradouro,
número e coordenadas e não podem ser versionados (ver ``README.md``).

Boas práticas de acesso (enunciado do LAB05 §2): user-agent identificado,
no máximo 1 requisição por segundo, tamanho conferido com o declarado pelo CKAN.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

import config as C


class ErroDeColeta(Exception):
    """Falha ao obter dados da fonte (rede, formato inesperado, tamanho)."""


def pasta_fora_do_repositorio(pasta: Path) -> Path:
    """Garante que ``pasta`` não está dentro do repositório (CSV bruto tem endereços)."""
    pasta = Path(pasta).expanduser().resolve()
    raiz = C.RAIZ.resolve()
    if pasta == raiz or raiz in pasta.parents:
        raise ErroDeColeta(
            f"A pasta de dados brutos ({pasta}) está dentro do repositório. Os CSVs "
            "originais contêm endereço e coordenadas e não podem ser guardados aqui. "
            "Use uma pasta fora do repositório (ex.: ~/.cache/lab05 ou /tmp/lab05)."
        )
    return pasta


class Cliente:
    """Cliente HTTP mínimo (só biblioteca padrão) com intervalo entre requisições."""

    def __init__(self, intervalo_s: float = C.INTERVALO_MIN_REQUISICOES_S):
        self.intervalo_s = intervalo_s
        self._ultima = 0.0

    def _esperar(self) -> None:
        falta = self.intervalo_s - (time.monotonic() - self._ultima)
        if falta > 0:
            time.sleep(falta)
        self._ultima = time.monotonic()

    def _abrir(self, url: str):
        self._esperar()
        req = urllib.request.Request(url, headers={"User-Agent": C.USER_AGENT})
        return urllib.request.urlopen(req, timeout=C.TIMEOUT_S)  # noqa: S310 (https/file)

    def json(self, url: str) -> dict:
        ultimo = None
        for tentativa in range(1, C.TENTATIVAS + 1):
            try:
                with self._abrir(url) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                ultimo = exc
                time.sleep(min(2 * tentativa, 6))
        raise ErroDeColeta(f"Não foi possível ler {url}: {ultimo}")

    def baixar(self, url: str, destino: Path) -> None:
        ultimo = None
        for tentativa in range(1, C.TENTATIVAS + 1):
            parcial = destino.with_suffix(destino.suffix + ".parcial")
            try:
                with self._abrir(url) as resp, open(parcial, "wb") as saida:
                    shutil.copyfileobj(resp, saida, length=1 << 20)
                parcial.replace(destino)
                return
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                ultimo = exc
                parcial.unlink(missing_ok=True)
                time.sleep(min(2 * tentativa, 6))
        raise ErroDeColeta(f"Falha ao baixar {url}: {ultimo}")


def listar_recursos(cliente: Cliente, url_api: str = C.URL_API_DATASET) -> dict:
    """Lê os metadados do dataset e devolve ``{'dataset': {...}, 'recursos': [...]}``.

    Só entram os recursos CSV de dados (os dicionários em PDF são apenas citados).
    A ordem é cronológica pelo nome, para que, em caso de duplicata de ticket, o
    arquivo mais recente prevaleça.
    """
    resposta = cliente.json(url_api)
    if not resposta.get("success"):
        raise ErroDeColeta(f"A API do CKAN respondeu sem sucesso: {str(resposta)[:300]}")
    pacote = resposta["result"]
    licenca = pacote.get("license_id")
    if licenca != C.LICENCA_ESPERADA:
        raise ErroDeColeta(
            f"Licença do dataset mudou: esperado {C.LICENCA_ESPERADA!r}, obtido "
            f"{licenca!r}. Releia as condições de uso antes de continuar."
        )
    recursos = []
    for r in pacote.get("resources", []):
        if str(r.get("format", "")).upper() != "CSV":
            continue
        recursos.append({
            "id": r["id"],
            "nome": r.get("name"),
            "url": r["url"],
            "tamanho_declarado": r.get("size"),
            "ultima_modificacao": r.get("last_modified"),
            "arquivo": r["url"].rsplit("/", 1)[-1],
        })
    if not recursos:
        raise ErroDeColeta("Nenhum recurso CSV encontrado no dataset.")
    recursos.sort(key=lambda r: ordem_cronologica(r["arquivo"]))
    return {
        "dataset": {
            "id": C.DATASET_ID,
            "titulo": pacote.get("title"),
            "licenca": licenca,
            "url": C.URL_DATASET,
            "metadata_modified": pacote.get("metadata_modified"),
            "mantenedor": pacote.get("maintainer"),
            "periodicidade_declarada": "Mensal (descrição do dataset)",
        },
        "recursos": recursos,
    }


_MESES = {m: i for i, m in enumerate(
    ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"], 1)}


def ordem_cronologica(arquivo: str) -> tuple[int, int]:
    """Chave (ano, mês) a partir do nome do arquivo (``..._2023_jun.csv``, ``..._2021.csv``)."""
    partes = Path(arquivo).stem.lower().replace("-", "_").split("_")
    ano = next((int(p) for p in partes if p.isdigit() and len(p) == 4), 0)
    mes = next((_MESES[p] for p in partes if p in _MESES), 0)
    return ano, mes


def sha256_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def coletar(destino: Path, cliente: Cliente | None = None, url_api: str = C.URL_API_DATASET,
            log=print) -> tuple[list[Path], dict]:
    """Baixa os CSVs (reaproveitando o que já está em ``destino`` com o mesmo tamanho).

    Devolve a lista de caminhos (em ordem cronológica) e o manifesto da coleta.
    """
    destino = pasta_fora_do_repositorio(destino)
    destino.mkdir(parents=True, exist_ok=True)
    cliente = cliente or Cliente()
    meta = listar_recursos(cliente, url_api)
    caminhos: list[Path] = []
    entradas = []
    for r in meta["recursos"]:
        caminho = destino / r["arquivo"]
        esperado = r["tamanho_declarado"]
        reaproveitado = (caminho.exists() and esperado is not None
                         and caminho.stat().st_size == int(esperado))
        if reaproveitado:
            log(f"  [cache] {r['arquivo']}")
        else:
            log(f"  [baixando] {r['arquivo']} ({int(esperado or 0) / 1e6:.1f} MB)")
            cliente.baixar(r["url"], caminho)
        tamanho = caminho.stat().st_size
        if esperado is not None and tamanho != int(esperado):
            raise ErroDeColeta(
                f"{r['arquivo']}: {tamanho} bytes baixados, o CKAN declara {esperado}."
            )
        caminhos.append(caminho)
        entradas.append({**r, "bytes": tamanho, "sha256": sha256_arquivo(caminho),
                         "do_cache": reaproveitado})
    manifesto = {"dataset": meta["dataset"], "recursos": entradas}
    return caminhos, manifesto


def descrever_arquivos_locais(pasta: Path) -> tuple[list[Path], dict]:
    """Usa CSVs que já estão numa pasta local (``--entrada``), sem acessar a rede."""
    pasta = pasta_fora_do_repositorio(pasta)
    caminhos = sorted(pasta.glob("*.csv"), key=lambda p: (ordem_cronologica(p.name), p.name))
    if not caminhos:
        raise ErroDeColeta(f"Nenhum .csv encontrado em {pasta}.")
    entradas = [{"arquivo": p.name, "bytes": p.stat().st_size, "sha256": sha256_arquivo(p),
                 "origem": "pasta_local"} for p in caminhos]
    return caminhos, {"dataset": {"id": C.DATASET_ID, "url": C.URL_DATASET},
                      "recursos": entradas}
