# Dicionário de dados — LAB05 (canais de atendimento da PBH)

Atualizado em 24/11/2026. Descreve (1) a fonte, (2) o que o pipeline lê e descarta e (3) a base analítica.
O código que implementa este dicionário está em `scripts/config.py` e `scripts/tratamento.py`.

## 1. Fonte

| Item | Valor (conferido na API do CKAN em 24/11/2026) |
|---|---|
| Conjunto | Solicitações dos cidadãos, por meio dos canais de atendimento da PBH |
| Página | https://ckan.pbh.gov.br/dataset/solicitacoes-dos-cidadaos-por-meio-dos-canais-de-atendimento-da-pbh |
| API | `https://ckan.pbh.gov.br/api/3/action/package_show?id=solicitacoes-dos-cidadaos-por-meio-dos-canais-de-atendimento-da-pbh` |
| Licença | Creative Commons Attribution (`cc-by`): uso livre com citação da fonte |
| Mantenedor | SUMOG — Subsecretaria de Modernização da Gestão (PBH) |
| Periodicidade declarada | "Mensal" (descrição do dataset) |
| Cobertura real dos arquivos | **maio/2020 a julho/2023** (10 CSVs: 2020 mai–dez, 2021, 2022, 2023 jan a jul). **Não há 2024, 2025 nem 2026** |
| Dicionário oficial | PDF "SUMOG - Dicionário de dados - Solicitações BHDIGITAL", atualizado em 25/07/2023 (2 páginas) |
| Acesso automatizado | O CKAN devolve HTTP 403 ao user-agent padrão de bibliotecas; aceita um user-agent identificado. O pipeline se identifica e respeita 1 requisição/segundo |

O campo `metadata_modified` do dataset indica 10/06/2026, mas os arquivos de dados foram publicados em julho/agosto de 2023. O dataset
"Solicitações de Serviço e Incidentes" (mesmo CKAN, até o 3º trimestre de 2026) é outra coisa: chamados de TI atendidos pela Prodabel,
sem coluna de canal; **não** é usado.

## 2. Colunas do CSV original

Separador `;`. Codificação: UTF-8 com BOM (2023) ou cp1252 (2020–2022); o pipeline detecta. Datas: `AAAA-MM-DD` (2020–2022) e `DD/MM/AAAA` (2023),
apesar de o cabeçalho dizer `YYYY-MM-DD` em todos.

| Coluna original | Descrição (dicionário oficial da PBH) | Destino |
|---|---|---|
| Id Ticket | Identificador da solicitação | **Pseudonimizado** (`id_hash`) |
| Nome Servico | Nome do serviço solicitado | Mantida (`servico`, `servico_chave`) |
| Data de criação (YYYY-MM-DD) | Data em que a solicitação foi realizada | Mantida (`data_criacao`) |
| Data de encerramento (YYYY-MM-DD) | Data em que foi encerrada | Mantida (`data_encerramento`) |
| Fase Atual | "Novo, em andamento ou encerrada" | Mantida (`fase_atual`) |
| Situacao Atendimento Atual | Situação atual da tramitação | Mantida, **sem interpretar** (`situacao_atual`) |
| Canal Captacao | Canal usado pelo cidadão | Normalizada (`canal`, `canal_original`) |
| Orgao Normatizador | Órgão que normatiza o serviço | Mantida (`orgao_normatizador`) |
| Orgao Responsavel | Órgão responsável pela etapa atual | **Descartada na leitura** |
| Nome Logradouro | Logradouro do endereço do serviço | **Descartada na leitura (endereço)** |
| Numero Logradouro | Número do imóvel | **Descartada na leitura (endereço)** |
| Bairro | Bairro | **Descartada na leitura (localização)** |
| Regional | Regional administrativa | **Descartada na leitura (localização)** |
| Coordenadas | Latitude/longitude (Sirgas 2000) | **Descartada na leitura (localização)** |
| Ind Tp Pbh App | "Se o serviço está disponível no Aplicativo PBH APP" | Descartada: é atributo do serviço, **não** o canal usado |
| Nivel Acesso | Público, restrito ou sigiloso | Descartada (99,3% "Restrito"; sem uso na análise) |

A leitura usa **lista branca**: só as 8 colunas mantidas são carregadas. As demais nunca chegam à memória nem a disco.

## 3. Canais (`Canal Captacao` → `canal`)

| Valor original | `canal` | Comparável? | Fundamento |
|---|---|---|---|
| Portal | `portal_servicos` | Sim | Dicionário: "Portal de Serviços" |
| Portal Mobile | `pbh_app` | Sim | Dicionário: "Aplicativo PBH APP (Portal Mobile)" |
| Telefônico | `telefone_156` | Sim | Introdução do dicionário: "Central de Atendimento Telefônico - 156" |
| Presencial | `presencial` | Sim | Introdução: "Central de Atendimento Presencial BH Resolve" |
| Integração entre Sistemas | `integracao_sistemas` | **Não** | Aparece nos dados; **significado não documentado** |
| Origem Interna | `origem_interna` | **Não** | Idem |
| E-mail | `email` | **Não** | 8 registros; não documentado |
| outro valor | `nao_mapeado` | **Não** | Registrado no relatório de qualidade |

## 4. Base analítica (`dados/processados/solicitacoes_analiticas.csv.gz`)

Gerada pelo pipeline; **não versionada** (`.gitignore`), pois é reproduzível (~38 MB).

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_hash` | texto | 16 primeiros hex do SHA-256 do Id Ticket |
| `arquivo_origem` | texto | CSV de origem |
| `servico_chave` | texto | Nome do serviço sem acento/pontuação, minúsculo (chave de comparação "mesmo serviço") |
| `servico` | texto | Nome legível (prefere variante sem "?") |
| `canal`, `canal_original`, `comparavel` | texto, texto, bool | Ver §3 |
| `data_criacao`, `data_encerramento` | data | `data_encerramento` só existe para `encerrada` |
| `mes_criacao` | texto `AAAA-MM` | |
| `fase_atual`, `situacao_atual`, `orgao_normatizador` | texto | Como na fonte |
| `status_registro` | `encerrada` / `aberta` / `inconsistente` | Ver §5 |
| `motivo_inconsistencia` | texto | Ver §5; vazio se não inconsistente |
| `tempo_dias` | número | Dias entre criação e encerramento. **Vazio (nunca 0) para aberta e inconsistente** |
| `seguimento_dias` | inteiro | Dias entre a criação e o corte de observação do arquivo |

Arquivos versionados da coleta: `dados/manifesto_coleta.json` (URLs, tamanhos, SHA-256 dos CSVs, SHA-256 da base) e
`dados/qualidade_dados.json` (contagens de ausentes, datas inválidas, duplicatas, inconsistências, colunas descartadas).

## 5. Classificação dos registros

| Status | Regra |
|---|---|
| `encerrada` | Fase "Encerrado" **e** data de encerramento válida **e** ≥ data de criação |
| `aberta` | Fase "Novo" ou "Em andamento" **e** sem data de encerramento |
| `inconsistente` | Qualquer outro caso, com o primeiro motivo aplicável: `servico_ausente`, `canal_ausente`, `criacao_invalida`, `criacao_fora_do_periodo` (antes de 01/05/2020 ou após o corte), `fase_desconhecida`, `encerrada_sem_data`, `encerramento_invalido`, `aberta_com_data_encerramento`, `encerramento_anterior_a_criacao` |

- **Duplicatas:** mesmo Id Ticket; fica o registro do arquivo mais recente. Registros iguais exceto pelo Id **não** são duplicatas (a mesma demanda no mesmo dia é comum).
- **Corte de observação:** a PBH não publica a data de extração; usa-se como proxy a **maior data de encerramento de cada arquivo** (21/07/2023 a 04/08/2023). É uma inferência.
- **Ausentes:** data de encerramento ausente é esperada para solicitações abertas; para as demais colunas obrigatórias, o registro vira inconsistente.

## 6. Limitações conhecidas da fonte (não inventar o que a PBH não documentou)

1. Cobertura termina em jul/2023.
2. O significado de "Integração entre Sistemas" e "Origem Interna", e a regra de `Situacao Atendimento Atual`, não estão documentados. Não se classifica o encerramento em "resolvido" ou "negado".
3. O travessão "–" dos nomes de serviço aparece como "?" em todos os arquivos (perda na origem).
4. Datas só têm resolução de dia; "0 dia" significa encerrada no mesmo dia civil.
5. Não há identificador do cidadão: não se verifica independência entre solicitações.
6. A coluna `Ind Tp Pbh App` vem vazia em todo o arquivo de jul/2023 (não é usada).
7. O canal Presencial tem comportamento próprio de registro (86% das suas solicitações são recursos JARI, que permanecem "Em andamento"); por isso a comparação é feita dentro do mesmo serviço.
