# Metodologia — LAB05 (versão 3.0, 24/11/2026)

## 1. Problema

A Prefeitura de Belo Horizonte (PBH) atende o cidadão por vários canais: Portal de Serviços (plataforma SYDLE ONE), aplicativo PBH APP,
Central telefônica 156 e atendimento presencial (BH Resolve). **Para um mesmo serviço, o resultado da solicitação difere conforme o canal usado?**

## 2. Por que a metodologia mudou

A proposta S01 (arquivada em `docs/arquivo/s01-metodologia-participantes/`) previa um experimento com 32 participantes comparando celular × computador,
com sessões presenciais, cronometragem manual, SUS/SEQ e consentimento. Isso exigia recrutar, agendar e moderar dezenas de sessões, com sobrecarga
operacional incompatível com o grupo. A nova abordagem usa **dados abertos reais de operação** da PBH: sem participantes, sem sessões e sem coleta manual.
É o caminho "analisar dados de operação" do enunciado (§2b), que cita "dados abertos de atendimento de serviços digitais do governo".

O objeto continua sendo o ecossistema de atendimento da PBH (inclusive o Portal), então os critérios real / em operação / alto impacto
(`docs/evidencias/S01_criterios_do_software.md`) continuam válidos. **A mudança ainda não foi submetida ao professor** (pendência P15).

## 3. Pergunta de pesquisa e GQM

**Principal:** para um mesmo serviço, existem diferenças no tempo de encerramento e na proporção de solicitações encerradas conforme o canal?

**Objetivo (Basili):** analisar as solicitações registradas no BH Digital, com o propósito de comparar, com respeito ao tempo e à taxa de encerramento,
do ponto de vista da gestão do atendimento ao cidadão, no contexto dos dados abertos da PBH de maio/2020 a julho/2023.

| Pergunta | Métricas | Como é respondida |
|---|---|---|
| Q1. Quais canais têm menor tempo mediano de encerramento? | Mediana, Q1–Q3, P90 do tempo (dias), mediana de Kaplan–Meier | Tabela e gráficos por canal |
| Q2. A proporção encerrada difere entre canais? | % encerrada em ≤ 90 dias e até o corte, com IC de Wilson | Qui-quadrado r×2 (global); por serviço e par: qui-quadrado ou Fisher |
| Q3. As diferenças permanecem dentro do mesmo serviço? | OR de Mantel–Haenszel, delta de Cliff combinado, I², contagem de serviços | CMH, van Elteren, teste dos sinais entre serviços |
| Q4. Quais serviços diferem mais entre canais? | Maior \|delta\| e maior \|diferença de risco\| por serviço | Rankings com Holm |

Quantidade de solicitações por canal é descritiva (Q1 e Q2).

## 3.1 Planejamento do estudo

Esta subseção formaliza o que a §3 já pergunta: variáveis, objetos, hipóteses, design, instrumentação e operação. Ela define as hipóteses, não as responde; a resposta está em `docs/interpretacao_resultados.md`.

### Variáveis e objetos

| Elemento | Definição |
|---|---|
| Objeto (unidade de análise) | Solicitação registrada no BH Digital; sem sujeitos humanos |
| Variável independente (fator) | Canal de captação, 4 níveis: Portal de Serviços, PBH APP, Telefone 156, Presencial (BH Resolve) |
| Variáveis dependentes | (1) tempo de encerramento em dias (razão; só encerradas); (2) encerrada em ≤ 90 dias (nominal binária) |
| Variável de estratificação (controle) | Serviço (`servico_chave`) |
| Parâmetros fixos | Horizonte de 90 dias; mínimo de 30 registros elegíveis (proporção) ou 30 encerradas (tempo) por célula serviço × canal; α = 0,05 (decisão do grupo, P16 pendente) |
| Variáveis não controladas (confusão possível) | Urgência e perfil do solicitante, regional (existe na fonte, descartada na leitura por privacidade; dicionário §2), ano, mudanças de plataforma |

### Hipóteses

Todas as H1 são bicaudais: H1 é a negação de H0 (por exemplo, "OR de MH ≠ 1"), e nenhuma afirma um sentido. A convenção de sinal da §6 vale para ler os resultados (delta de Cliff > 0 = A mais lento; OR > 1 = A encerra mais em 90 dias).

| ID | Pergunta | H0 | H1 | Teste | Onde está o resultado |
|---|---|---|---|---|---|
| H-Q1 | Q1 | O tempo de encerramento (entre as encerradas) tem a mesma distribuição nos 4 canais (sem ajuste) | O tempo difere em pelo menos um canal | Kruskal–Wallis | `resultados.json` → `comparacao_ingenua.tempo.p` |
| H-Q2 | Q2 | A proporção encerrada em ≤ 90 d é igual nos 4 canais (sem ajuste) | A proporção difere em pelo menos um canal | Qui-quadrado r×2 | `resultados.json` → `comparacao_ingenua.proporcao.p` |
| H-Q3p | Q3 | Para cada par A × B, OR de Mantel–Haenszel = 1 entre serviços | OR de MH ≠ 1 | CMH | `pares_ajustados_por_servico.csv` → `p_cmh_holm` |
| H-Q3p-s | Q3 | P(serviço em que A encerra mais \| serviços sem empate) = 0,5 | P(serviço em que A encerra mais \| serviços sem empate) ≠ 0,5 | Teste dos sinais | `pares_ajustados_por_servico.csv` → `p_sinais_prop_holm` |
| H-Q3t | Q3 | Dentro dos serviços, os tempos de A e B (entre as encerradas) não diferem estocasticamente | Os tempos de A e B (entre as encerradas) diferem estocasticamente | van Elteren | `pares_ajustados_por_servico.csv` → `p_van_elteren_holm` |
| H-Q3t-s | Q3 | P(serviço em que A é mais lento \| serviços sem empate) = 0,5 | P(serviço em que A é mais lento \| serviços sem empate) ≠ 0,5 | Teste dos sinais | `pares_ajustados_por_servico.csv` → `p_sinais_tempo_holm` |
| H-S | Q3 | Para um dado serviço e par, a proporção não difere (qui-quadrado/Fisher) e, em teste separado, o tempo das encerradas não difere (Mann–Whitney) | Para esse serviço e par, difere | Qui-quadrado ou Fisher; Mann–Whitney | `pares_por_servico.csv` → `p_prop_holm`, `p_tempo_holm` |
| H-O | Q3 | Para um dado serviço com ≥ 3 canais, a proporção não difere entre os canais (qui-quadrado r×2) e, em teste separado, o tempo das encerradas não difere (Kruskal–Wallis) | Para esse serviço, difere | Qui-quadrado r×2; Kruskal–Wallis | `omnibus_por_servico.csv` → `p_prop_holm`, `p_tempo_holm` |

1. Q1 é descritiva; H-Q1 é só o teste global sem ajuste. Q4 é exploratória e não tem hipótese própria: usa os p da família H-S apenas para ordenar e filtrar.
2. **Regra de decisão:** rejeitar H0 com p (Holm) < 0,05 **e** só chamar a diferença de relevante quando a magnitude for pelo menos "pequena" (limiares da §6). Com n ≈ 10⁶, rejeitar H0 sozinho não diz nada. Magnitude por hipótese: H-S, delta de Cliff (`delta_magnitude`) e h de Cohen (`h_magnitude`); H-Q3t, delta combinado com a ressalva D14; H-Q3p, mediana da diferença de risco por serviço (`mediana_dif_risco_pp`), pois a §6 não fixa limiar para OR; H-Q1, H-Q2 e H-O, V de Cramér e ε², só descritivos (sem limiar fixado); testes dos sinais, só consistência, sem magnitude.
3. **Limitação:** as definições e os testes foram fixados antes dos resultados (FONTE §6), mas as hipóteses só foram escritas formalmente em 25/11/2026, **depois** de os resultados existirem. Não são pré-registradas, e essa limitação deve entrar nas ameaças de conclusão (§8, card #24).

### Design, instrumentação e operação

- **Design:** observacional retrospectivo, estratificado por serviço, sem atribuição de tratamento.
- **Instrumentação:** `scripts/pipeline.py` (coleta, tratamento, estatística, visualização), com testes em `tests/`.
- **Operação:** coleta única pela API do CKAN a 1 req/s, CSVs fora do repositório e colunas de endereço descartadas na leitura (ver §5).

## 4. Métricas e escalas

| Métrica | Definição | Escala | Estatística adequada |
|---|---|---|---|
| Tempo de encerramento | Dias entre criação e encerramento, **só de encerradas** | Razão (inteiro, dias) | Mediana, quartis, testes de postos |
| Encerrada em ≤ H dias | 1 se encerrada em até H = 90 dias | Nominal (binária) | Proporção, qui-quadrado/Fisher, CMH |
| Taxa de encerramento (corte) | Encerradas / elegíveis, até o corte de observação | Razão (%) | Descritiva |
| Solicitações por canal | Contagem | Razão | Descritiva |

Registros **abertos** não têm tempo (nunca 0) e **inconsistentes** são excluídos e contados por motivo. A definição de "elegível" e o
tratamento da censura estão em `scripts/estatistica.py` (cabeçalho do módulo) e abaixo.

## 5. Dados e tratamento

Pipeline único (`python scripts/pipeline.py`): baixa os 10 CSVs pela API do CKAN (1 req/s, user-agent identificado) para pasta temporária **fora do repositório**,
lê **apenas** as colunas da lista branca (descarta logradouro, número, bairro, regional e coordenadas na leitura), detecta codificação, converte os dois formatos de data,
normaliza canais, pseudonimiza o Id Ticket, remove duplicatas, classifica os registros, calcula o tempo, grava a base anonimizada e apaga os CSVs brutos. Detalhes em
`dados/dicionario_de_dados.md`.

## 6. Análise estatística

- **Coorte madura (decisão de desenho):** só entram solicitações com seguimento ≥ 90 dias até o corte de observação. Sem isso, as recentes pareceriam "abertas" por falta de tempo (censura à direita).
- **Mesmo serviço:** estratificação por serviço. Um serviço entra num par de canais só se as duas células têm ≥ 30 registros.
- **Proporções:** qui-quadrado sem correção; Fisher exato se 2×2 e esperado < 5 (pressuposto verificado em cada teste). Testes sem informação (todos encerrados nos dois grupos) ficam fora da família de Holm.
- **Tempos:** Mann–Whitney assintótico (com muitos empates o exato não vale); Kruskal–Wallis para ≥ 3 canais. Empates são frequentes (encerramento no mesmo dia); por isso a interpretação é de dominância estocástica (delta de Cliff), não de diferença de medianas.
- **Entre serviços:** Cochran–Mantel–Haenszel (OR combinado, IC de Robins–Breslow–Greenland, heterogeneidade por Q de Cochran e I²); van Elteren para tempos; teste dos sinais sobre o sentido da diferença em cada serviço.
- **Tamanho de efeito:** diferença de risco (IC de Newcombe), razão de chances, h de Cohen, delta de Cliff (IC de Cliff com erro-padrão de DeLong), épsilon² (Kruskal–Wallis), V de Cramér. Magnitudes: |delta| < 0,147 desprezível, < 0,33 pequena, < 0,474 média (Romano et al., 2006); |h| < 0,2 / 0,5 / 0,8 (Cohen).
- **Múltiplas comparações:** Holm por família (proporções por serviço-par, tempos por serviço-par, omnibus por serviço, pares ajustados).
- **Sensibilidade:** horizontes de 30 e 180 dias; mediana de Kaplan–Meier (abertas como censuradas).
- **Convenção de sinal:** para o par (A, B), delta de Cliff > 0 = A mais lento; OR > 1 = A encerra mais.
- Com n da ordem de 10⁵–10⁶ quase tudo tem p minúsculo: **a leitura é pelo tamanho do efeito e pela consistência entre serviços**, não pelo p. A conferência dos blocos estatísticos (contra scipy, força bruta, exemplos publicados e simulação de cobertura do IC) está em `tests/test_estatistica.py`.

## 7. Classificação em sete categorias (Aula 8)

| Categoria | Classificação | Justificativa |
|---|---|---|
| Natureza | Aplicada | Gestão de um serviço público em produção |
| Objetivos | Descritiva e exploratória (comparativa) | Descreve e compara desempenho; não testa mecanismo |
| Abordagem | Quantitativa | Métricas, testes e tamanho de efeito |
| Procedimentos | Análise documental de dados secundários de operação (estudo observacional retrospectivo) | Dados abertos já existentes, sem intervenção |
| Tempo | Longitudinal retrospectivo (mai/2020–jul/2023), comparação entre canais | Registros ao longo de ~3 anos |
| Controle | Sem controle experimental; ajuste estatístico por serviço | O canal não foi atribuído pelo pesquisador |
| Nível de evidência | Observacional: associação, não causa | Auto-seleção do canal e perfis diferentes de demanda |

Classificação sujeita a revisão na S03.

## 8. Ameaças à validade

| Tipo | Ameaça | Mitigação / tratamento |
|---|---|---|
| Conclusão | n enorme torna qualquer diferença "significativa" | Efeito, IC e consistência entre serviços; Holm |
| Conclusão | Independência não verificável (sem id do cidadão) | Declarada; não há como corrigir |
| Conclusão | Muitos empates nos tempos | Mann–Whitney com correção de empates; delta de Cliff; reportar proporção de empates |
| Interna | Perfil das solicitações difere entre canais; cidadão escolhe o canal | Estratificação por serviço; **não** elimina confusão residual (urgência, perfil do solicitante) |
| Interna | Censura à direita (abertas recentes) | Coorte madura de 90 dias; sensibilidade 30/180 dias; Kaplan–Meier |
| Interna | Mudanças na plataforma e nas regras ao longo de 2020–2023 | Não controlado; limitação |
| Construto | "Encerrada" é encerramento administrativo, não resolução (a situação "Serviço não realizado" também encerra) | Significado das situações não documentado: não se interpreta |
| Construto | Corte de observação é proxy (maior encerramento do arquivo) | Declarado |
| Construto | Resolução de 1 dia; "0 dia" é mesmo dia civil | Declarado |
| Externa | Só BH, só até jul/2023, só 164 de ~422 serviços têm ≥ 2 canais comparáveis | Não extrapolar para outros períodos, serviços ou cidades |
| Externa | Presencial e Telefone têm poucos serviços em comum com os demais (Telefone × Presencial: 2) | Resultados desses pares são frágeis |

## 9. Reproduzir

Ver `README.md`. Saídas em `resultados/` (resumo, tabelas, figuras, painel). Todos os números do resumo e do painel são gerados pelo código a partir dos dados.
