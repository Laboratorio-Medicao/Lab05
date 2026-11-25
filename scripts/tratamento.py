"""Leitura, anonimização e tratamento dos CSVs da PBH — LAB05.

Fluxo (cada passo corresponde a um item da FONTE_DA_VERDADE §8):

1. ``ler_csv``: detecta a codificação (UTF-8 com BOM ou cp1252), lê **somente as
   colunas da lista branca** (``config.COLUNAS_ORIGEM``). Logradouro, número,
   bairro, regional e coordenadas nunca chegam à memória nem a disco.
2. ``tratar``: padroniza texto, normaliza canais, converte datas (dois formatos
   convivem nos arquivos), pseudonimiza o ``Id Ticket``, remove duplicatas, calcula
   o tempo de encerramento e classifica cada registro em **encerrada**, **aberta**
   ou **inconsistente** (com o motivo). Solicitação aberta nunca recebe tempo 0.
3. ``gravar_base``: grava a base analítica anonimizada (``dados/processados/``,
   fora do git) e o relatório de qualidade.
"""

from __future__ import annotations

import gzip
import hashlib
import io
from pathlib import Path

import numpy as np
import pandas as pd

import config as C

ENCODINGS = ("utf-8-sig", "cp1252", "latin-1")
_AUSENTES_TEXTO = {"", "null", "nan", "none", "n/a", "na"}


class ErroDeDados(Exception):
    """Arquivo com estrutura inesperada (colunas obrigatórias ausentes etc.)."""


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------

def _renomear(cabecalhos) -> dict[str, str]:
    return {c: C.COLUNAS_ORIGEM[C.normalizar_cabecalho(c)]
            for c in cabecalhos if C.normalizar_cabecalho(c) in C.COLUNAS_ORIGEM}


def ler_csv(caminho: Path) -> tuple[pd.DataFrame, dict]:
    """Lê um CSV da PBH mantendo só as colunas da lista branca.

    Devolve ``(DataFrame com nomes internos, informações do arquivo)``. As
    informações incluem a codificação, a contagem de linhas e os **nomes** (nunca
    os valores) das colunas descartadas.
    """
    caminho = Path(caminho)
    ultimo_erro = None
    for enc in ENCODINGS:
        try:
            cabecalho = pd.read_csv(caminho, sep=";", dtype=str, encoding=enc, nrows=0)
            todas = list(cabecalho.columns)
            mapa = _renomear(todas)
            faltam = sorted(set(C.COLUNAS_ORIGEM.values()) - set(mapa.values()))
            if faltam:
                raise ErroDeDados(
                    f"{caminho.name}: colunas obrigatórias ausentes: {faltam}. "
                    f"Cabeçalhos encontrados: {todas}"
                )
            df = pd.read_csv(
                caminho, sep=";", dtype=str, encoding=enc, usecols=list(mapa),
                keep_default_na=False, na_values=[""],
            )
            break
        except UnicodeDecodeError as exc:
            ultimo_erro = exc
    else:
        raise ErroDeDados(f"{caminho.name}: codificação não reconhecida ({ultimo_erro})")
    df = df.rename(columns=mapa)[list(C.COLUNAS_ORIGEM.values())]
    descartadas = sorted(C.normalizar_cabecalho(c) for c in todas if c not in mapa)
    info = {
        "arquivo": caminho.name,
        "codificacao": "utf-8-sig" if enc == "utf-8-sig" else enc,
        "linhas": int(len(df)),
        "colunas_descartadas": descartadas,
    }
    return df, info


# ---------------------------------------------------------------------------
# Normalização
# ---------------------------------------------------------------------------

def limpar_texto(s: pd.Series) -> pd.Series:
    """Remove espaços nas pontas, colapsa repetidos e converte ausentes em NA."""
    s = s.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    return s.mask(s.str.lower().isin(_AUSENTES_TEXTO))


def _mapear_unicos(s: pd.Series, fn) -> pd.Series:
    """Aplica ``fn`` só aos valores distintos (rápido em colunas de baixa cardinalidade)."""
    valores = s.dropna().unique()
    tabela = {v: fn(v) for v in valores}
    return s.map(tabela)


def normalizar_canal(s: pd.Series) -> pd.Series:
    def um(v: str) -> str:
        return C.MAPA_CANAL.get(C.normalizar_rotulo(v), C.CANAL_NAO_MAPEADO)
    return _mapear_unicos(s, um).astype("string")


def parse_data(s: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Converte datas aceitando os DOIS formatos presentes nos arquivos da PBH.

    ``AAAA-MM-DD`` (2020–2022) e ``DD/MM/AAAA`` (2023). Os formatos são distintos
    por construção, então não há ambiguidade dia/mês. Qualquer outro padrão, ou
    data impossível (ex.: 31/02), vira NaT e é contada como inválida.

    Devolve ``(datas, invalida)``; ``invalida`` é True onde havia texto que não
    pôde ser convertido (ausente não é inválido).
    """
    s = s.astype("string").str.strip()
    iso = s.str.fullmatch(r"\d{4}-\d{2}-\d{2}").fillna(False).astype(bool)
    br = s.str.fullmatch(r"\d{2}/\d{2}/\d{4}").fillna(False).astype(bool)
    datas = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    if iso.any():
        datas[iso] = pd.to_datetime(s[iso], format="%Y-%m-%d", errors="coerce")
    if br.any():
        datas[br] = pd.to_datetime(s[br], format="%d/%m/%Y", errors="coerce")
    invalida = s.notna() & datas.isna()
    return datas, invalida


def hash_id(s: pd.Series) -> pd.Series:
    """Pseudonimiza o identificador do ticket (SHA-256, 16 primeiros hex)."""
    return pd.Series([hashlib.sha256(v.encode("utf-8")).hexdigest()[:16] for v in s.astype(str)],
                     index=s.index, dtype="string")


def _nome_exibicao(serv: pd.Series, chave: pd.Series) -> pd.Series:
    """Nome legível por chave: o mais frequente que não tenha "?" (caractere perdido)."""
    df = pd.DataFrame({"chave": chave, "nome": serv}).dropna()
    df["tem_interrogacao"] = df["nome"].str.contains("?", regex=False)
    cont = (df.groupby(["chave", "nome", "tem_interrogacao"], observed=True).size()
              .reset_index(name="n")
              .sort_values(["chave", "tem_interrogacao", "n", "nome"],
                           ascending=[True, True, False, True]))
    melhor = cont.drop_duplicates("chave").set_index("chave")["nome"]
    return chave.map(melhor)


# ---------------------------------------------------------------------------
# Tratamento
# ---------------------------------------------------------------------------

def tratar(brutos: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Gera a base analítica a partir dos registros lidos (colunas internas).

    ``brutos`` deve ter as colunas de ``config.COLUNAS_ORIGEM`` e ``arquivo_origem``,
    na ordem cronológica dos arquivos (em duplicata de ticket vale o mais recente).
    """
    df = brutos.copy()
    n_bruto = len(df)
    q: dict = {"linhas_brutas": int(n_bruto)}

    # --- texto e ausentes ---------------------------------------------------
    for col in ("id_ticket", "servico", "fase_atual", "situacao_atual",
                "canal_original", "orgao_normatizador"):
        df[col] = limpar_texto(df[col])
    q["ausentes_brutos"] = {c: int(df[c].isna().sum()) for c in
                            ("id_ticket", "servico", "fase_atual", "situacao_atual",
                             "canal_original", "orgao_normatizador")}
    q["ausentes_brutos"]["data_encerramento"] = int(
        brutos["data_encerramento"].isna().sum())
    q["ausentes_brutos"]["data_criacao"] = int(brutos["data_criacao"].isna().sum())

    # --- duplicatas por Id Ticket -------------------------------------------
    sem_id = df["id_ticket"].isna()
    q["registros_sem_id"] = int(sem_id.sum())
    df = df[~sem_id].copy()
    dup = df["id_ticket"].duplicated(keep=False)
    if dup.any():
        sub = df[dup]
        campos = ["data_criacao", "data_encerramento", "fase_atual", "canal_original"]
        conflitantes = int((sub.groupby("id_ticket")[campos].nunique(dropna=False) > 1)
                           .any(axis=1).sum())
    else:
        conflitantes = 0
    antes = len(df)
    df = df.drop_duplicates("id_ticket", keep="last")
    q["duplicatas"] = {
        "criterio": "Id Ticket idêntico; permanece o registro do arquivo mais recente",
        "removidas": int(antes - len(df)),
        "ids_com_conteudo_conflitante": conflitantes,
    }

    # --- canal e serviço ----------------------------------------------------
    df["canal"] = normalizar_canal(df["canal_original"])
    df["comparavel"] = df["canal"].isin(C.CANAIS_COMPARAVEIS)
    df["servico_chave"] = _mapear_unicos(df["servico"], C.chave_texto).astype("string")
    df["servico"] = _nome_exibicao(df["servico"], df["servico_chave"])
    df["fase_norm"] = _mapear_unicos(df["fase_atual"], C.normalizar_rotulo).astype("string")

    # --- datas --------------------------------------------------------------
    df["data_criacao"], cri_inv = parse_data(df["data_criacao"])
    df["data_encerramento"], enc_inv = parse_data(df["data_encerramento"])
    q["datas_invalidas"] = {"criacao": int(cri_inv.sum()), "encerramento": int(enc_inv.sum())}

    # corte de observação por arquivo = último encerramento registrado no arquivo
    # (proxy da data de extração; a PBH não publica essa data no CSV)
    corte = df.groupby("arquivo_origem")["data_encerramento"].transform("max")
    df["corte_observacao"] = corte
    df["seguimento_dias"] = (df["corte_observacao"] - df["data_criacao"]).dt.days

    # --- classificação ------------------------------------------------------
    inicio = pd.Timestamp(C.INICIO_PERIODO_VALIDO)
    cria_ok = df["data_criacao"].notna()
    fase = df["fase_norm"]
    e_encerrada = fase == C.FASE_ENCERRADA
    e_aberta = fase.isin(C.FASES_ABERTAS)
    tem_enc = df["data_encerramento"].notna()

    motivo = pd.Series(pd.NA, index=df.index, dtype="string")

    def marcar(cond, nome):
        nonlocal motivo
        motivo = motivo.mask(motivo.isna() & cond, nome)

    marcar(df["servico"].isna(), "servico_ausente")
    marcar(df["canal_original"].isna(), "canal_ausente")
    marcar(~cria_ok, "criacao_invalida")
    marcar(cria_ok & ((df["data_criacao"] < inicio)
                      | (df["seguimento_dias"].notna() & (df["seguimento_dias"] < 0))),
           "criacao_fora_do_periodo")
    marcar(~(e_encerrada | e_aberta), "fase_desconhecida")
    marcar(e_encerrada & ~tem_enc & enc_inv, "encerramento_invalido")
    marcar(e_encerrada & ~tem_enc, "encerrada_sem_data")
    marcar(e_aberta & (tem_enc | enc_inv), "aberta_com_data_encerramento")
    marcar(e_encerrada & tem_enc & cria_ok
           & (df["data_encerramento"] < df["data_criacao"]), "encerramento_anterior_a_criacao")

    df["motivo_inconsistencia"] = motivo
    df["status_registro"] = np.where(
        motivo.notna(), C.STATUS_INCONSISTENTE,
        np.where(e_encerrada, C.STATUS_ENCERRADA, C.STATUS_ABERTA))

    # tempo só existe para encerradas; aberta e inconsistente ficam NaN (nunca 0)
    tempo = (df["data_encerramento"] - df["data_criacao"]).dt.days
    df["tempo_dias"] = tempo.where(df["status_registro"] == C.STATUS_ENCERRADA)

    df["mes_criacao"] = df["data_criacao"].dt.strftime("%Y-%m")
    df["id_hash"] = hash_id(df["id_ticket"])
    df["data_encerramento"] = df["data_encerramento"].where(
        df["status_registro"] == C.STATUS_ENCERRADA)

    base = df[C.COLUNAS_BASE].reset_index(drop=True)
    garantir_anonimato(base)

    # --- relatório de qualidade --------------------------------------------
    q["linhas_base"] = int(len(base))
    q["status_registro"] = base["status_registro"].value_counts().to_dict()
    q["motivos_inconsistencia"] = (base["motivo_inconsistencia"].value_counts().to_dict())
    q["canais_originais"] = (base["canal_original"].value_counts(dropna=False)
                             .rename(index=lambda v: "<ausente>" if pd.isna(v) else v).to_dict())
    q["canais_normalizados"] = base["canal"].value_counts().to_dict()
    q["canais_nao_mapeados"] = sorted(
        base.loc[base["canal"] == C.CANAL_NAO_MAPEADO, "canal_original"].dropna().unique())
    q["servicos_distintos"] = int(base["servico_chave"].nunique())
    q["periodo_criacao"] = [str(base["data_criacao"].min().date()),
                            str(base["data_criacao"].max().date())]
    q["corte_observacao_por_arquivo"] = {
        k: str(v.date()) for k, v in
        df.groupby("arquivo_origem")["corte_observacao"].max().items() if pd.notna(v)}
    q["tempo_dias_encerradas"] = _resumo(base["tempo_dias"].dropna())
    return base, q


def _resumo(x: pd.Series) -> dict:
    if x.empty:
        return {}
    return {"n": int(x.size), "min": float(x.min()), "mediana": float(x.median()),
            "p99": float(x.quantile(0.99)), "max": float(x.max())}


def garantir_anonimato(base: pd.DataFrame) -> None:
    """Falha se alguma coluna da base lembrar endereço/identificação pessoal."""
    for col in base.columns:
        nome = col.lower()
        for trecho in C.TRECHOS_COLUNA_PROIBIDA:
            if trecho in nome:
                raise ErroDeDados(f"Coluna proibida na base analítica: {col!r} ({trecho})")
    extras = set(base.columns) - set(C.COLUNAS_BASE)
    if extras:
        raise ErroDeDados(f"Colunas fora do esquema da base analítica: {sorted(extras)}")


# ---------------------------------------------------------------------------
# Orquestração e persistência
# ---------------------------------------------------------------------------

def processar(caminhos: list[Path], log=print) -> tuple[pd.DataFrame, dict]:
    """Lê todos os CSVs, na ordem dada, e devolve ``(base, relatório de qualidade)``."""
    partes, infos = [], []
    for caminho in caminhos:
        log(f"  [lendo] {Path(caminho).name}")
        df, info = ler_csv(caminho)
        df.insert(0, "arquivo_origem", Path(caminho).name)
        partes.append(df)
        infos.append(info)
    brutos = pd.concat(partes, ignore_index=True)
    base, q = tratar(brutos)
    q["arquivos"] = infos
    q["colunas_descartadas_na_leitura"] = sorted({c for i in infos for c in i["colunas_descartadas"]})
    return base, q


def gravar_base(base: pd.DataFrame, caminho: Path) -> Path:
    """Grava a base em CSV gzip determinístico (mesmos bytes a cada execução)."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    saida = base.copy()
    for c in ("data_criacao", "data_encerramento"):
        saida[c] = saida[c].dt.strftime("%Y-%m-%d")
    # gzip sem nome de arquivo nem data no cabeçalho: mesmos bytes a cada execução
    with open(caminho, "wb") as bruto, gzip.GzipFile(
            filename="", mode="wb", fileobj=bruto, mtime=0) as gz:
        saida.to_csv(io.TextIOWrapper(gz, encoding="utf-8", newline=""), index=False,
                     lineterminator="\n")
    return caminho


def ler_base(caminho: Path) -> pd.DataFrame:
    """Lê a base analítica gravada por ``gravar_base``."""
    df = pd.read_csv(caminho, dtype={
        "id_hash": "string", "arquivo_origem": "category", "servico_chave": "string",
        "servico": "string", "canal": "category", "canal_original": "category",
        "mes_criacao": "string", "fase_atual": "category", "situacao_atual": "category",
        "orgao_normatizador": "category", "status_registro": "category",
        "motivo_inconsistencia": "category",
    }, parse_dates=["data_criacao", "data_encerramento"], low_memory=False)
    df["comparavel"] = df["comparavel"].astype(bool)
    garantir_anonimato(df)
    return df
