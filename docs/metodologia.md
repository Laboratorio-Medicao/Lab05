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
- **Sensibilidade:** horizontes de 30 e 180 dias; mediana de Kaplan–Meier (abertas como censuradas); delta combinado com peso n_A·n_B/(n_A+n_B) e mediana por serviço. O resultado de tempo do par é tratado como inconclusivo quando os sinais discordam (acrescentada em 25/11/2026, depois de ver os resultados; D14, #39).
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

As ameaças foram revistas com os resultados reais em 25/11/2026. Os IDs (C = conclusão, I = interna, K = construto, E = externa) são estáveis e serão citados nas limitações e no rascunho do documento final. A coluna "O que resta" diz o que continua em aberto depois da mitigação: nenhuma ameaça é tratada como resolvida.

| ID | Tipo | Ameaça | Evidência | Mitigação aplicada | O que resta |
|---|---|---|---|---|---|
| C1 | Conclusão | Com n da ordem de 10⁶ nos testes agregados, qualquer diferença sai "significativa" | p < 0,0001 em 11 dos 12 testes estratificados por par (CMH e van Elteren, `resultados/resumo.md`); por serviço, com n menor, só 30 de 286 (proporção) e 59 de 286 (tempo) ficam abaixo de 0,05 após Holm (`pares_por_servico.csv`) | Leitura pelo tamanho do efeito (delta de Cliff, h de Cohen, V, ε²), pelo IC e pela contagem de serviços; Holm por família | O p quase não discrimina. Magnitudes "desprezível" e "pequena" podem ser estatisticamente claras e irrelevantes na prática |
| C2 | Conclusão | Um serviço domina o efeito combinado: o Tapa-Buraco no delta de tempo dos pares com Presencial (44% a 68% do peso, D14) e a JARI no OR de Mantel–Haenszel desses pares | Interpretação §4 (com peso alternativo e com a mediana por serviço o sinal se inverte) e §3.3 (OR de 14 a 19 dominado pela JARI, I² = 0,99) | Delta combinado dos pares com Presencial tratado como inconclusivo; mediana por serviço e teste dos sinais sempre ao lado do número combinado; sensibilidade de ponderação (#39) para o delta de tempo | O OR de MH **não** tem sensibilidade equivalente: a sensibilidade de ponderação do #39 cobre só o delta de tempo. O OR desses pares segue dominado pela JARI e instável (de 7,6 a 23,2 entre os horizontes de 30 e 180 dias, interpretação §6). Os pares com Presencial não sustentam conclusão |
| C3 | Conclusão | Heterogeneidade alta entre serviços: um número combinado resume mal | I² de 0,89 a 0,99 em todos os pares (`pares_ajustados_por_servico.csv`; interpretação §7) | Mediana por serviço, contagem de serviços (teste dos sinais) e rankings por serviço junto de todo valor combinado | O efeito varia de serviço para serviço; o valor combinado não representa nenhum serviço em particular |
| C4 | Conclusão | Independência entre solicitações não verificável (a base não tem id do cidadão) | `resultados/resultados.json`, bloco `pressupostos` | Declarada; nenhum procedimento disponível com esses dados | ICs e p podem estar otimistas se o mesmo cidadão gera vários pedidos. Não há como medir |
| C5 | Conclusão | Muitos empates nos tempos (encerramento no mesmo dia) | Proporção de empates: mediana 0,027, máxima 0,44 (interpretação §7) | Mann–Whitney assintótico e delta de Cliff (dominância estocástica) em vez de diferença de medianas | Nos serviços com muitos empates, o teste e o IC são menos precisos |
| C6 | Conclusão | Hipóteses formalizadas depois dos resultados, sem pré-registro | Metodologia §3.1 (#37); FONTE §6 (definições e testes fixados antes dos resultados) | Testes, horizonte e peso fixados antes da análise (FONTE §6); regra de decisão com magnitude mínima (§3.1) | As hipóteses H0/H1 foram escritas com os resultados já conhecidos; o rigor de confirmação é menor que o de um estudo pré-registrado |
| C7 | Conclusão | Holm corrige dentro de cada família de testes, não entre famílias | Metodologia §6 (Holm por família) | Nenhuma correção entre famílias; as conclusões não se apoiam em p isolado (C1), mas em magnitude e consistência entre serviços | Não há controle do erro entre as famílias; a quantidade total de testes aumenta o risco de falso positivo |
| I1 | Interna | Confusão pelo tipo de serviço: cada canal recebe uma mistura diferente de demandas | Efeito cerca de 10 vezes menor dentro do serviço (V de Cramér de 0,46 para mediana 0,040; ε² de 0,077 para 0,006); 88,7% do Presencial elegível é JARI (interpretação §2 e §3.1) | Estratificação por serviço (CMH, van Elteren, comparação dentro do serviço) | O serviço é só uma das fontes de confusão: a estratificação corrige a mistura de serviços, não a de perfis dentro do serviço |
| I2 | Interna | Autosseleção do canal pelo cidadão; confusão residual dentro do serviço (urgência, perfil do solicitante, região) | Metodologia §7 (sem controle experimental; o canal não foi atribuído pelo pesquisador) | Estratificação por serviço; linguagem de associação, não de causa | Urgência e perfil do solicitante não existem na fonte; a localização (Regional, Bairro) existe, mas é descartada na leitura por privacidade (dicionário §2) e não pode ser usada como estratificador; qualquer diferença residual pode vir desses fatores |
| I3 | Interna | Censura à direita: pedidos recentes ainda abertos parecem não encerrados | Metodologia §6; `resultados/tabelas/sensibilidade_horizonte.csv` (sentido de todos os pares estável em 30, 90 e 180 dias) | Coorte madura de 90 dias; sensibilidade em 30 e 180 dias; mediana de Kaplan–Meier | Os pedidos da coorte imatura ficam fora da análise principal. O corte de observação é inferido (K3) e o OR de MH varia com o horizonte (C2) |
| I4 | Interna | Mudanças de plataforma, de regras e de demanda (inclusive a pandemia) ao longo de 2020–2023 | Metodologia §8 (versão anterior): não controlado | Nenhuma; o ano não entra como estratificador | Um canal pode ter mudado de comportamento ao longo do período, e o resultado médio esconde isso |
| K1 | Construto | "Encerrada" é encerramento administrativo, não resolução (Goodhart/McNamara); "Serviço não realizado" também encerra | Metodologia §8 (versão anterior); dicionário §6, item 2 (a regra de `Situacao Atendimento Atual` não é documentada) | Não se interpreta a situação; o texto fala em "encerrada", nunca em "resolvida" | Um canal que "encerra mais rápido" pode só fechar o pedido mais cedo. Os dados não separam os dois casos |
| K2 | Construto | Significado das situações e dos canais "Integração entre Sistemas" e "Origem Interna" não documentado pela PBH | Dicionário §6, item 2 | Situações mantidas sem interpretação; canais não documentados fora da análise principal (E4) | Não se sabe o que esses canais representam na base; a situação de encerramento não distingue resolução de negativa (K1) |
| K3 | Construto | O corte de observação é um proxy (maior data de encerramento de cada arquivo) | Dicionário §5 (21/07/2023 a 04/08/2023; "é uma inferência") | Declarado; usado só para definir a coorte madura e o seguimento | Se o corte real for outro, o seguimento de cada pedido muda e a fronteira da coorte madura se desloca |
| K4 | Construto | Resolução de 1 dia: "0 dia" é encerrada no mesmo dia civil | Metodologia §8 (versão anterior); dicionário §6, item 4 | Declarado; empates tratados pelo delta de Cliff (C5) | Diferenças menores que um dia não existem nos dados; a medida é grosseira para serviços rápidos |
| K5 | Construto | Normalização do nome do serviço (`servico_chave`) e travessão perdido ("?") na fonte podem juntar ou separar serviços, afetando o "mesmo serviço" | Dicionário §4 e §6.3 | Chave sem acento/pontuação, minúscula | Variantes de nome não verificadas manualmente |
| E1 | Externa | Só Belo Horizonte, de mai/2020 a jul/2023 (inclui a pandemia) | Dicionário §1 (cobertura real dos arquivos) | Declarado; o texto não extrapola para outros períodos nem cidades | Não vale para outros municípios nem para depois de jul/2023; P17 (consulta à PBH) segue aberta |
| E2 | Externa | Só 164 dos 422 serviços com solicitações elegíveis têm ≥ 2 canais com ≥ 30 registros (61 têm um só canal; 197 têm ≥ 2 canais, mas menos de 2 células com ≥ 30). A base tem 460 serviços (`dados/qualidade_dados.json`); os 38 restantes não têm nenhuma solicitação elegível (só em canais não comparáveis ou só na coorte imatura) | `resultados/tabelas/servico_x_canal.csv`; os 164 somam 998.775 de 1.042.926 elegíveis (95,8%) | Declarado; a comparação é feita só onde há dado | O resultado não vale para os 258 serviços fora da comparação, embora eles somem só 4,2% das solicitações elegíveis |
| E3 | Externa | Poucos serviços em comum com o Presencial (20 e 15) e só 2 no par 156 × Presencial | `resultados/tabelas/pares_ajustados_por_servico.csv` (`servicos_prop`) | Par 156 × Presencial marcado como "não interpretar" (interpretação §3.2) | As conclusões sobre o Presencial se apoiam em poucos serviços e não generalizam |
| E4 | Externa | Canais "Integração entre Sistemas", "Origem Interna" e "E-mail" fora da análise: 298.570 registros (20,2% da base) | `funil_elegibilidade.csv` | Declarado | O resultado não vale para as solicitações desses canais |

**Resumo.** As ameaças mais sérias são I1 (a maior parte da diferença global vem do serviço), C2 (os pares com Presencial não sustentam conclusão), K1 (encerrada não é resolvida) e E1 (só BH, 2020–2023). Nenhuma foi eliminada: a tabela mostra o que foi feito e o que continua em aberto.

## 9. Reproduzir

Ver `README.md`. Saídas em `resultados/` (resumo, tabelas, figuras, painel). Todos os números do resumo e do painel são gerados pelo código a partir dos dados.
