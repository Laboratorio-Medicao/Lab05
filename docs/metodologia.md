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

Revisada em 25/11/2026 (S03, issue #27), com base no que foi **executado** (pipeline, resultados e interpretação), e não mais só no planejado. A coluna "Muda?" compara com a classificação preliminar da S01/v3.0.

| Categoria | Classificação | Justificativa (baseada no executado) | Muda em relação à S01/preliminar? |
|---|---|---|---|
| Natureza | Aplicada | Gestão de um serviço público em produção (BH Digital, PBH). O resultado serve a quem usa e a quem gere o serviço (`docs/conclusoes_limitacoes.md`) | Não |
| Objetivos | Descritiva e exploratória-comparativa | Q1 e Q4 são descritivas (medianas, proporções, ranking de serviços). Q2 usa qui-quadrado r×2 (H-Q2); Q3 usa CMH, van Elteren e teste dos sinais (§3.1), mas só medem associação: nenhum teste busca o mecanismo causal (`docs/interpretacao_resultados.md` §1, §3) | Ajuste de redação: "comparativa" e o limite "sem mecanismo causal" ficam explícitos |
| Abordagem | Quantitativa | Todas as medidas são numéricas: tempo de encerramento, proporção encerrada em ≤ 90 dias, tamanhos de efeito (`resultados/tabelas/`) | Não |
| Procedimentos | Pesquisa documental com dados secundários de operação; estudo observacional retrospectivo (*ex post facto*) | Dados abertos da PBH já existentes (CKAN), coletados a 1 req/s e processados por `scripts/pipeline.py`; o pesquisador não interveio em nenhuma solicitação | Redação mais precisa: "análise documental" vira "pesquisa documental"; o procedimento é o mesmo |
| Tempo | Retrospectivo; coorte retrospectiva no nível da solicitação, com análise agregada no período (sem estudo de tendência temporal) | Cada solicitação é acompanhada da criação ao encerramento ou ao corte (seguimento ≥ 90 d, Kaplan–Meier), mas os 3 anos (mai/2020–jul/2023) são analisados juntos, sem o ano como estratificador (I4) | Sim: o "longitudinal" preliminar sugeria estudo de evolução no tempo, que não foi feito |
| Controle | Sem controle experimental; controle estatístico por estratificação por serviço | O canal não foi atribuído pelo pesquisador (autosseleção, I2). O serviço entra como estratificador (CMH, van Elteren, comparações dentro do serviço); urgência e perfil não estão nos dados, e a região existe na fonte, mas é descartada na leitura por privacidade (dicionário §2) | Não (redação mais precisa) |
| Nível de evidência | Observacional: associação, não causa | O efeito global some em grande parte ao controlar o serviço (V de Cramér de 0,46 para mediana 0,040; ε² de 0,077 para 0,006, `docs/interpretacao_resultados.md` §3.1). O caso do Presencial, em que 88,7% das solicitações elegíveis são recursos à JARI (I1), mostra que a confusão existe e é grande | Não; agora com a evidência de que a confusão ocorre |

### Por que não é um experimento

Apesar de o laboratório se chamar "Experimento Final", o estudo **não é um experimento**: o canal não foi atribuído aleatoriamente nem pelo pesquisador. O enunciado aceita estudo observacional e análise de dados de operação (FAQ, §10) e exige **classificar corretamente** e discutir a força da evidência; é isso que a tabela acima faz. Essa força é limitada pela autosseleção do canal (I2): o cidadão escolhe por onde pedir, então qualquer diferença residual pode vir de quem escolhe e não do canal. Por isso o texto fala em associação, nunca em efeito do canal. Combinar este caminho com outro, como um survey com usuários, é sugerido como trabalho futuro, porque o enunciado valoriza a combinação de caminhos (§2b).

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
