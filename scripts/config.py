"""Configuração e constantes do pipeline do LAB05 (dados abertos da PBH).

Tudo o que é decisão de projeto (fonte dos dados, mapa de canais, colunas que
podem entrar na memória, parâmetros da análise) fica aqui, em um só lugar, para
que a documentação (``dados/dicionario_de_dados.md`` e FONTE_DA_VERDADE) possa
ser conferida contra o código.

Nada aqui contém dado coletado.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Fonte dos dados (confirmada na API do CKAN em 24/11/2026)
# ---------------------------------------------------------------------------

CKAN_BASE = "https://ckan.pbh.gov.br"
DATASET_ID = "solicitacoes-dos-cidadaos-por-meio-dos-canais-de-atendimento-da-pbh"
URL_DATASET = f"{CKAN_BASE}/dataset/{DATASET_ID}"
URL_API_DATASET = f"{CKAN_BASE}/api/3/action/package_show?id={DATASET_ID}"
LICENCA_ESPERADA = "cc-by"

# O CKAN da PBH bloqueia (HTTP 403) o user-agent padrão de bibliotecas, mas aceita
# um user-agent que identifica quem acessa. Identificar-se é a prática correta.
USER_AGENT = (
    "Lab05-PUCMinas-pesquisa-academica "
    "(dados abertos; https://github.com/Laboratorio-Medicao/Lab05)"
)
# O enunciado do LAB05 (§2) limita medições em sistema de terceiros a 1 requisição
# por segundo. O download respeita esse intervalo mínimo entre requisições.
INTERVALO_MIN_REQUISICOES_S = 1.0
TIMEOUT_S = 300
TENTATIVAS = 3

# ---------------------------------------------------------------------------
# Colunas: LISTA BRANCA. Só estas colunas do CSV da PBH entram na memória.
# Todas as outras (logradouro, número, bairro, regional, coordenadas, órgão
# responsável, nível de acesso, indicador do app) são descartadas na leitura e
# nunca chegam a um DataFrame nem a disco.
# ---------------------------------------------------------------------------

COLUNAS_ORIGEM = {
    # cabeçalho normalizado (sem acento, minúsculo) -> nome interno
    "id ticket": "id_ticket",
    "nome servico": "servico",
    "data de criacao (yyyy-mm-dd)": "data_criacao",
    "data de encerramento (yyyy-mm-dd)": "data_encerramento",
    "fase atual": "fase_atual",
    "situacao atendimento atual": "situacao_atual",
    "canal captacao": "canal_original",
    "orgao normatizador": "orgao_normatizador",
}

# Cabeçalhos que sabemos conter endereço/localização (informação pessoal em
# potencial). Servem para registrar no manifesto QUAIS foram descartados e para o
# teste que garante que nenhum deles chega à base analítica.
COLUNAS_SENSIVEIS_CONHECIDAS = (
    "nome logradouro", "numero logradouro", "bairro", "regional", "coordenadas",
)
# Trechos que jamais podem aparecer em nome de coluna da base analítica.
TRECHOS_COLUNA_PROIBIDA = (
    "logradouro", "endereco", "coordenad", "latitude", "longitude", "bairro",
    "regional", "cpf", "email", "e_mail", "telefone", "fone", "rg_",
)

# Colunas da base analítica (ordem canônica).
COLUNAS_BASE = [
    "id_hash", "arquivo_origem", "servico_chave", "servico", "canal",
    "canal_original", "comparavel", "data_criacao", "data_encerramento",
    "mes_criacao", "fase_atual", "situacao_atual", "orgao_normatizador",
    "status_registro", "motivo_inconsistencia", "tempo_dias", "seguimento_dias",
]

# ---------------------------------------------------------------------------
# Canais
# ---------------------------------------------------------------------------

# Mapa do valor original de "Canal Captacao" (normalizado) para o canal do estudo.
# O dicionário de dados da PBH (SUMOG, 25/07/2023) descreve o campo como
# "Presencial, telefônico, Aplicativo PBH APP (Portal Mobile), Portal de Serviços,
# etc." e a introdução cita a Central 156 (telefônica) e a Central Presencial BH
# Resolve. "Integração entre Sistemas", "Origem Interna" e "E-mail" aparecem nos
# dados, mas NÃO têm significado documentado: ficam como canais não comparáveis.
MAPA_CANAL = {
    "portal": "portal_servicos",
    "portal mobile": "pbh_app",
    "telefonico": "telefone_156",
    "presencial": "presencial",
    "integracao entre sistemas": "integracao_sistemas",
    "origem interna": "origem_interna",
    "e-mail": "email",
    "email": "email",
}
CANAL_NAO_MAPEADO = "nao_mapeado"

CANAIS_COMPARAVEIS = ("portal_servicos", "pbh_app", "telefone_156", "presencial")
CANAIS_OUTROS = ("integracao_sistemas", "origem_interna", "email", CANAL_NAO_MAPEADO)

ROTULO_CANAL = {
    "portal_servicos": "Portal de Serviços",
    "pbh_app": "PBH APP",
    "telefone_156": "Telefone 156",
    "presencial": "Presencial (BH Resolve)",
    "integracao_sistemas": "Integração entre sistemas",
    "origem_interna": "Origem interna",
    "email": "E-mail",
    CANAL_NAO_MAPEADO: "Não mapeado",
}

# ---------------------------------------------------------------------------
# Estados do registro e fases
# ---------------------------------------------------------------------------

FASE_ENCERRADA = "encerrado"
FASES_ABERTAS = ("novo", "em andamento")

STATUS_ENCERRADA = "encerrada"
STATUS_ABERTA = "aberta"
STATUS_INCONSISTENTE = "inconsistente"

MOTIVOS_INCONSISTENCIA = (
    "criacao_invalida",
    "criacao_fora_do_periodo",
    "fase_desconhecida",
    "encerrada_sem_data",
    "encerramento_invalido",
    "aberta_com_data_encerramento",
    "encerramento_anterior_a_criacao",
    "servico_ausente",
    "canal_ausente",
)

# O Portal de Serviços na plataforma atual foi lançado em maio de 2020 (PBH,
# 12/05/2020) e o primeiro registro do dataset é de 11/05/2020. Datas de criação
# anteriores a esta são tratadas como inválidas.
INICIO_PERIODO_VALIDO = "2020-05-01"


# ---------------------------------------------------------------------------
# Parâmetros da análise (fixados ANTES de olhar os resultados)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Parametros:
    """Parâmetros da análise. Mudá-los é decisão metodológica: registrar na FDV §19."""

    # Coorte madura: só solicitações com pelo menos este seguimento (dias entre a
    # criação e o corte de observação do arquivo) entram na análise principal.
    # Sem isso, solicitações recentes pareceriam "abertas" só por falta de tempo.
    horizonte_dias: int = 90
    # Células (serviço × canal) com menos que isto não entram nos testes.
    min_celula: int = 30
    alfa: float = 0.05
    semente: int = 20261124
    # Horizontes alternativos, só para a análise de sensibilidade da proporção.
    horizontes_sensibilidade: tuple[int, ...] = (30, 180)
    # Quantos serviços mostrar nos rankings e nos gráficos.
    top_servicos: int = 15


# ---------------------------------------------------------------------------
# Normalização de texto
# ---------------------------------------------------------------------------

_RE_ESPACOS = re.compile(r"\s+")
_RE_NAO_ALNUM = re.compile(r"[^0-9a-z]+")


def sem_acento(texto: str) -> str:
    """Remove acentos (NFKD) e devolve minúsculas."""
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c)).lower()


def normalizar_cabecalho(nome: str) -> str:
    """Normaliza um cabeçalho de CSV: sem BOM, aspas, acento e espaços repetidos."""
    nome = nome.replace("﻿", "").strip().strip('"').strip()
    return _RE_ESPACOS.sub(" ", sem_acento(nome))


def normalizar_rotulo(texto: str) -> str:
    """Normaliza um rótulo categórico (canal, fase) para comparação."""
    return _RE_ESPACOS.sub(" ", sem_acento(texto.strip()))


def chave_texto(texto: str) -> str:
    """Chave de comparação de nomes de serviço.

    Remove acentos e tudo que não for letra ou dígito, o que torna a chave
    robusta a variações de pontuação e de caixa. Observação (verificada em todos
    os 10 arquivos): o travessão "–" dos nomes aparece como "?" na própria fonte,
    inclusive nos arquivos UTF-8 de 2023; é perda de caractere da origem, não de
    leitura. A chave ignora esse "?" e o nome de exibição escolhe, quando existir,
    uma variante sem "?".
    """
    return _RE_NAO_ALNUM.sub(" ", sem_acento(texto)).strip()
