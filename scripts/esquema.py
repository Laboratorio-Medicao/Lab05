"""Esquema compartilhado dos dados do LAB05 (issue #25).

PROPOSTA do papel C, a confirmar com o papel B (Instrumentação e Operação).
A descrição completa está em ``dados/dicionario_de_dados.md``; este módulo é a
versão executável do mesmo dicionário e é usado por ``validar_dados.py``,
``analise.py`` e ``gerar_dados_sinteticos.py``.

Nada aqui contém dado coletado. Não existe nenhum resultado empírico.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Constantes do desenho (FONTE_DA_VERDADE §6)
# ---------------------------------------------------------------------------

DISPOSITIVOS = ("celular", "computador")
CONJUNTOS = ("A", "B")
TETO_S = 300.0
SEMENTE = 20261117
META_POR_SEQUENCIA = 8
N_TAREFAS_POR_DISPOSITIVO = 3

# Sequência -> dispositivo do 1º período e conjunto de cada dispositivo.
# 1 celular-A/computador-B; 2 celular-B/computador-A;
# 3 computador-A/celular-B; 4 computador-B/celular-A (FDV §6.3).
SEQUENCIAS = {
    1: {"primeiro": "celular", "celular": "A", "computador": "B"},
    2: {"primeiro": "celular", "celular": "B", "computador": "A"},
    3: {"primeiro": "computador", "celular": "B", "computador": "A"},
    4: {"primeiro": "computador", "celular": "A", "computador": "B"},
}

MOTIVOS_FIM = ("concluida", "teto", "abandono", "ajuda", "falha_tecnica")
ROTULOS_WCAG = ("com_violacao", "sem_violacao_detectada", "indeterminado")
PASSO_FORA = "fora_do_caminho"
ORIGENS = ("real", "sintetico")
PREFIXO_SINTETICO = "SINTETICO_"

FERRAMENTAS_AUDITORIA = ("axe", "lighthouse")
MODOS_AUDITORIA = ("mobile", "desktop")
TAGS_WCAG = ("wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa")
IMPACTOS_AXE = ("minor", "moderate", "serious", "critical")

# Colunas obrigatórias de cada tabela (ordem canônica).
COLUNAS = {
    "participantes": [
        "participante", "sequencia", "bloco", "ordem_realizacao", "data",
        "faixa_etaria", "uso_previo_portal", "familiaridade_digital",
        "valida", "motivo_invalida", "reposto_por", "piloto",
        "hash_ui_package", "versao_chrome", "versao_portal_obs",
        "o_que_mais_atrapalhou", "notas_moderador", "origem",
    ],
    "sessoes": [
        "participante", "dispositivo", "conjunto", "periodo", "tarefa_id",
        "ordem_tarefa", "concluida", "tempo_s", "motivo_fim", "pediu_ajuda",
        "erros", "seq", "origem",
    ],
    "sus": ["participante", "dispositivo"]
    + [f"item_{i}" for i in range(1, 11)] + ["origem"],
    "catalogo_passos": [
        "tarefa_id", "passo_id", "dispositivo", "pagina_url", "elemento",
        "rotulo_wcag", "regras_axe", "motivo_indeterminado", "origem",
    ],
    "passos": [
        "participante", "dispositivo", "tarefa_id", "passo_id", "alcancado",
        "n_erros", "origem",
    ],
}
COLUNAS_INDICE_AUDITORIA = [
    "arquivo", "pagina_url", "data", "versao_chrome", "ferramenta", "modo",
    "execucao", "origem",
]

# Trechos de nome de coluna que indicam dado pessoal (proibidos).
TRECHOS_COLUNA_PROIBIDA = (
    "nome", "email", "e_mail", "telefone", "fone", "cpf", "rg", "endereco",
    "contato", "whatsapp", "nascimento",
)

FAIXAS_ETARIAS = ("18-24", "25-34", "35-44", "45-59", "60+")
USO_PREVIO = ("nunca", "raramente", "as_vezes", "frequentemente")
FAMILIARIDADE = ("1", "2", "3", "4", "5")

TABELAS_CSV = tuple(COLUNAS)


class ErroDeDados(Exception):
    """Erro de estrutura ou de origem dos dados (ex.: mistura real × sintético)."""


def nome_arquivo(tabela: str, sintetico: bool) -> str:
    """Nome do arquivo CSV de uma tabela; sintéticos levam o prefixo SINTETICO_."""
    return f"{PREFIXO_SINTETICO}{tabela}.csv" if sintetico else f"{tabela}.csv"


def detectar_sintetico(pasta: Path) -> bool:
    """Diz se a pasta contém o conjunto sintético ou o real.

    Recusa pasta que tenha arquivos das duas origens ao mesmo tempo.
    """
    pasta = Path(pasta)
    tem_sint = any((pasta / nome_arquivo(t, True)).exists() for t in TABELAS_CSV)
    tem_real = any((pasta / nome_arquivo(t, False)).exists() for t in TABELAS_CSV)
    if tem_sint and tem_real:
        raise ErroDeDados(
            f"A pasta {pasta} mistura arquivos sintéticos (SINTETICO_*) e reais. "
            "Separe os conjuntos antes de validar ou analisar."
        )
    if not tem_sint and not tem_real:
        raise ErroDeDados(f"Nenhuma tabela do LAB05 encontrada em {pasta}.")
    return tem_sint


def carregar_tabelas(pasta: Path) -> tuple[dict[str, pd.DataFrame], bool]:
    """Lê as cinco tabelas como texto (sem conversão) e diz se são sintéticas.

    Ler como texto permite que o validador confira os domínios antes de
    qualquer conversão. Tabela ausente vira DataFrame vazio com as colunas
    canônicas (o validador acusa a ausência).
    """
    pasta = Path(pasta)
    sintetico = detectar_sintetico(pasta)
    tabelas = {}
    for t in TABELAS_CSV:
        arq = pasta / nome_arquivo(t, sintetico)
        if arq.exists():
            tabelas[t] = pd.read_csv(arq, dtype=str, keep_default_na=False)
        else:
            tabelas[t] = pd.DataFrame(columns=COLUNAS[t], dtype=str)
            tabelas[t].attrs["ausente"] = True
    return tabelas, sintetico


def pasta_auditoria(pasta: Path) -> Path:
    return Path(pasta) / "auditoria"


def carregar_indice_auditoria(pasta: Path, sintetico: bool) -> pd.DataFrame | None:
    """Lê ``auditoria/indice.csv`` (ou ``SINTETICO_indice.csv``); None se não houver."""
    nome = f"{PREFIXO_SINTETICO}indice.csv" if sintetico else "indice.csv"
    arq = pasta_auditoria(pasta) / nome
    if not arq.exists():
        return None
    return pd.read_csv(arq, dtype=str, keep_default_na=False)


def _bool01(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().map({"1": True, "0": False})


def tipar(tabelas: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Converte as tabelas lidas como texto para os tipos usados na análise.

    Pressupõe dados já validados por ``validar_dados.py``.
    """
    t = {k: v.copy() for k, v in tabelas.items()}
    p = t["participantes"]
    for c in ("sequencia", "bloco", "ordem_realizacao"):
        p[c] = pd.to_numeric(p[c]).astype(int)
    for c in ("valida", "piloto"):
        p[c] = _bool01(p[c])
    s = t["sessoes"]
    for c in ("periodo", "ordem_tarefa", "erros", "seq"):
        s[c] = pd.to_numeric(s[c]).astype(int)
    s["tempo_s"] = pd.to_numeric(s["tempo_s"]).astype(float)
    for c in ("concluida", "pediu_ajuda"):
        s[c] = _bool01(s[c])
    u = t["sus"]
    for i in range(1, 11):
        u[f"item_{i}"] = pd.to_numeric(u[f"item_{i}"]).astype(int)
    ps = t["passos"]
    ps["alcancado"] = _bool01(ps["alcancado"])
    ps["n_erros"] = pd.to_numeric(ps["n_erros"]).astype(int)
    return t


def origens_presentes(tabelas: dict[str, pd.DataFrame]) -> set[str]:
    """Conjunto de valores da coluna ``origem`` em todas as tabelas."""
    vals: set[str] = set()
    for df in tabelas.values():
        if "origem" in df.columns and len(df):
            vals |= set(df["origem"].astype(str).unique())
    return vals


def exigir_origem_unica(tabelas: dict[str, pd.DataFrame], sintetico: bool) -> str:
    """Recusa misturar origem real e sintética; devolve a origem única.

    Também exige que a origem bata com o nome dos arquivos (prefixo SINTETICO_).
    """
    vals = origens_presentes(tabelas)
    if len(vals) != 1:
        raise ErroDeDados(
            f"Coluna 'origem' com valores {sorted(vals)}: é proibido misturar "
            "dado real e sintético (ou deixar a origem em branco)."
        )
    origem = vals.pop()
    esperado = "sintetico" if sintetico else "real"
    if origem != esperado:
        raise ErroDeDados(
            f"Origem '{origem}' não bate com o nome dos arquivos (esperado "
            f"'{esperado}'). Arquivo sintético precisa do prefixo SINTETICO_."
        )
    return origem
