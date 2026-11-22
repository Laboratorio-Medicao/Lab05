---
title: "LAB05 S01 — Proposta: Usabilidade e acessibilidade do Portal de Serviços da PBH"
subtitle: "Versão revisada em 17/11/2026 (original de 16/11/2026) · @Someone"
---

Propomos um experimento intrassujeitos com 32 participantes analisáveis, comparando celular × computador no Portal de Serviços da PBH, junto com uma auditoria de acessibilidade WCAG complementar. Os participantes navegam manualmente pelo Portal. A auditoria usa as ferramentas axe DevTools e Lighthouse, acionadas manualmente por um integrante em páginas selecionadas. Não há crawler nem varredura automatizada em larga escala, porque o robots.txt do Portal contém `Disallow: /`.

Itens que dependem do professor, do grupo ou de evidência documental estão identificados como P1 a P14 na seção 10. Nenhum deles deve ser lido como aprovado ou comprovado.

# 1. Software escolhido

O objeto é o Portal de Serviços da Prefeitura de Belo Horizonte, construído sobre a plataforma comercial SYDLE ONE. O foco é o software em uso pelo cidadão, não código-fonte nem repositório.

| Critério | Evidência | Fonte (acesso em 16/11/2026) |
|---|---|---|
| Real | O HTML da página inicial carrega os pacotes @sydle/pbh-components, @sydle/sydle-one-components e @sydle/service-desk-components, com org: "bhdigital" (forma de obtenção a documentar, P7). SYDLE ONE é vendida como plataforma de BPM, CRM e Service Desk. | Página inicial do Portal; sydle.com/br |
| Em operação | Portal no ar, lançado na plataforma atual em maio de 2020, com login único gov.br. | PBH, 12/05/2020 |
| Alto impacto | 1.492 serviços catalogados, 1.118 solicitáveis pela internet. De janeiro a setembro de 2026, 92% das demandas à Prefeitura entraram pelo Portal ou pelo app. | PBH, 05/10/2026 |
| Alto impacto | 496.956 solicitações de serviço de janeiro a outubro de 2023, somando Portal, app, 156 e BH Resolve. | PBH, 27/12/2023 |
| Alto impacto | Belo Horizonte tem 2.315.560 habitantes (Censo 2022; número a conferir, P9). BH foi eleita cidade mais digital do Brasil pelo terceiro ano. | IBGE Cidades; PBH, 18/08/2026 |

Em aberto: número de acessos mensais ao Portal. Nenhuma página pública consultada o informa; o pedido será feito via Lei de Acesso à Informação ao canal de transparência da PBH (P10).

Restrição que molda o estudo: o robots.txt do Portal contém `User-agent: *` e `Disallow: /`. Por isso o grupo não usa crawler nem coleta automatizada em larga escala. A compatibilidade das ferramentas de auditoria, acionadas manualmente, com o robots.txt e com os termos de uso não está comprovada nem refutada e depende de validação (P8 e P12).

# 2. Pergunta de pesquisa e caminhos

Pergunta principal: o cidadão consegue encontrar e iniciar um serviço no Portal de Serviços da PBH com a mesma eficácia, eficiência e satisfação no celular e no computador?

Pergunta complementar: quais barreiras de acessibilidade (WCAG 2.2, nível AA) existem nas páginas dos serviços mais procurados, e elas coincidem com os pontos onde os participantes erram?

O estudo combina dois caminhos do enunciado:

1. Estudar com pessoas (principal): experimento com participantes executando tarefas reais de consulta no Portal, comparando celular × computador.
2. Avaliar a qualidade do produto (complementar): auditoria de acessibilidade e desempenho com axe DevTools e Lighthouse, acionadas manualmente por um integrante, no próprio navegador, em páginas selecionadas. As ferramentas executam verificações automatizadas sobre a página aberta; não há varredura de páginas.

A combinação dá duas fontes de evidência: a auditoria aponta onde o produto viola o padrão, e o experimento mostra se isso atrapalha quem usa.

Por que celular × computador: o tratamento é controlável pelo grupo, não exige conta nem dado real e responde a uma decisão prática da PBH (onde investir em usabilidade). A alternativa Portal × app BH SIM fica como plano B, porque o app oferece só 129 serviços e restringe as tarefas comparáveis.

# 3. GQM

Objetivo (template de Basili): analisar o Portal de Serviços da PBH, com o propósito de avaliar, com respeito à usabilidade e à acessibilidade, do ponto de vista do cidadão, no contexto de usuários adultos realizando consultas sem login em celular e computador.

Perguntas:

- Q1. O dispositivo altera a eficácia, isto é, o número de tarefas concluídas?
- Q2. O dispositivo altera o tempo gasto nas tarefas (com teto de 300 s)?
- Q3. O dispositivo altera a satisfação percebida?
- Q4. Quantas e quais violações WCAG existem nas páginas dos serviços da tarefa? (descritiva, sem hipótese)
- Q5. As violações encontradas estão nos passos onde os participantes erram? (exploratória)

Correspondência com as questões de pesquisa: Q1 ↔ RQ1; Q2 ↔ RQ2; Q3 ↔ RQ3; Q5 ↔ RQ4 (exploratória, fora do Holm). A Q4 não corresponde a nenhuma RQ nem a hipótese: é análise descritiva de acessibilidade. Entram nos testes das RQs apenas a contagem de tarefas concluídas (RQ1), o log-tempo médio (RQ2) e o escore SUS (RQ3). São apenas descritivos, sem teste de hipótese: o nº de erros por tarefa, o item SUS, o SEQ, o SUS contra a referência de 68 pontos, a taxa de conclusão em % e todas as métricas da Q4. Os erros por passo alimentam a RQ4, exploratória e descritiva.

| Métrica | Pergunta | Entidade (tipo) | Atributo | Medida | Escala |
|---|---|---|---|---|---|
| Tarefa concluída (sim/não) | Q1 | Produto em uso | Eficácia (externo) | Direta | Nominal |
| Tarefas concluídas por participante e dispositivo (0 a 3) | Q1 | Produto em uso | Eficácia (externo) | Derivada | Razão (contagem) |
| Taxa de conclusão (%) | Q1 | Produto em uso | Eficácia (externo) | Derivada | Razão |
| Tempo na tarefa (s), com teto de 300 s | Q2 | Processo (uso) | Eficiência (externo) | Direta | Razão |
| Log-tempo médio por participante e dispositivo | Q2 | Processo (uso) | Eficiência (externo) | Derivada | Intervalar (log de uma razão) |
| Nº de erros por tarefa | Q2 | Processo (uso) | Eficiência (externo) | Direta | Razão (contagem) |
| Escore SUS (0–100) | Q3 | Recurso (participante) sobre o produto | Satisfação (externo) | Derivada | Intervalar (tratada como tal por convenção) |
| Item SUS (1–5) | Q3 | Recurso (participante) | Satisfação | Direta | Ordinal |
| SEQ pós-tarefa (1–7) | Q3 | Recurso (participante) | Dificuldade percebida | Direta | Ordinal |
| Nº de violações axe por página, por severidade | Q4 | Produto | Acessibilidade (interno) | Direta | Razão; severidade ordinal |
| Nota de acessibilidade Lighthouse (0–100) | Q4 | Produto | Acessibilidade (interno) | Derivada | Ordinal (não é intervalar) |
| LCP e CLS no Lighthouse mobile | Q4 | Produto | Eficiência de desempenho | Direta | Razão |
| Taxa de erro por passo (erros registrados ÷ pessoas que chegaram ao passo), por grupo de passos: com violação WCAG, sem violação detectada (por axe e pelo checklist manual) e indeterminado | Q5 | Processo (uso) | Associação | Derivada | Razão (erros por pessoa) |

Armadilhas de medição: a nota Lighthouse é fácil de "jogar" (Goodhart): página nota 100 ainda pode ser inutilizável com leitor de tela. Por isso ela não é métrica principal; o desfecho principal é a conclusão da tarefa por pessoas (contra a Falácia de McNamara, que mede só o que é fácil de contar).

# 4. Hipóteses e desenho experimental

São quatro questões de pesquisa, cada uma com um único par H0/H1 (bicaudais, α = 0,05). RQ1, RQ2 e RQ3 são confirmatórias e formam a família da correção de Holm (3 testes). A RQ4 é exploratória, fica fora da correção e é conduzida de forma descritiva, sem p-valor (seção 7).

| RQ | Pergunta | H0 | H1 | Status e teste |
|---|---|---|---|---|
| RQ1 | O dispositivo altera a eficácia, isto é, o número de tarefas concluídas por participante (0 a 3)? | Não há diferença no número de tarefas concluídas entre celular e computador | Há diferença no número de tarefas concluídas entre celular e computador | Confirmatória (Holm de 3); Wilcoxon pareado |
| RQ2 | O dispositivo altera a eficiência, isto é, o tempo gasto nas tarefas, com teto de 300 s (que não é o tempo até concluir quando a tarefa falha)? | A média, entre participantes, da diferença do log do tempo gasto, com teto de 300 s (celular − computador), é zero, isto é, a razão das médias geométricas dos tempos gastos (celular/computador) é 1 | A média da diferença do log do tempo gasto é diferente de zero, isto é, a razão das médias geométricas dos tempos gastos é diferente de 1 | Confirmatória (Holm de 3); t pareado no log |
| RQ3 | O dispositivo altera a satisfação percebida, medida pelo SUS? | A diferença média de SUS (celular − computador) é zero | A diferença média de SUS é diferente de zero | Confirmatória (Holm de 3); t pareado |
| RQ4 | A ocorrência de erro está associada ao fato de o passo da tarefa ter violação WCAG? | A taxa de erro por passo é a mesma entre passos com violação WCAG e passos sem violação detectada por axe e pelo checklist manual (os rótulos "com" e "sem" violação são permutáveis em relação à taxa de erro) | A taxa de erro por passo é diferente entre passos com violação WCAG e passos sem violação detectada por axe e pelo checklist manual | Exploratória, fora do Holm; análise descritiva, sem p-valor. Um teste de permutação só será considerado se a validade puder ser defendida (P4) |

Fora das RQs, sem hipótese: a descrição das violações WCAG e do desempenho das páginas das tarefas (Q4 do GQM), o SEQ e o SUS contra a referência de 68 pontos, todos apenas descritivos.

A RQ4 é exploratória: seu resultado não é apresentado como evidência confirmatória nem como evidência causal.

Variáveis:

| Tipo | Variável | Níveis ou valores |
|---|---|---|
| Independente (fator) | Dispositivo | Celular Android (Chrome) × computador (Chrome, tela 1366×768 ou maior) |
| Dependentes | Tempo (teto de 300 s), tarefas concluídas (0 a 3), erros, SEQ, SUS | Ver GQM |
| Controladas | Rede, navegador, tarefas, roteiro, moderador | Mesma rede Wi-Fi, Chrome atual, roteiro lido igual para todos, um moderador fixo |
| Bloqueio | Ordem do dispositivo e pareamento conjunto-dispositivo | Contrabalanceamento completo das quatro sequências |
| Covariáveis registradas | Idade (faixa), uso prévio do Portal, familiaridade digital, sequência | Questionário inicial, sem identificação |

Design: intrassujeitos com um fator de dois níveis (dispositivo), contrabalanceado em 4 sequências que cruzam a ordem do dispositivo com o pareamento conjunto-dispositivo: celular-A/computador-B, celular-B/computador-A, computador-A/celular-B, computador-B/celular-A. É contrabalanceamento completo das quatro sequências, não quadrado latino. Cada participante usa os dois dispositivos, com dois conjuntos de tarefas equivalentes (A e B). A ordem das 3 tarefas dentro do conjunto é sorteada por participante.

Participantes, sequências e recrutamento:

- **Meta:** 32 participantes analisáveis, 8 por sequência. Adultos, recrutados por conveniência entre colegas, familiares e funcionários da universidade, excluídos os que trabalham no desenvolvimento do Portal.
- **Agendamento:** 36 a 38 pessoas, o que cobre 10% a 15% de faltas (32/0,90 ≈ 35,6; 32/0,85 ≈ 37,6). Esses percentuais são estimativas de planejamento, sem dados. Eventuais reservas estão incluídas nesse número e não se somam a ele.
- **Piloto:** 3 participantes, que não repetem e não entram na análise final.
- **Recrutamento:** 39 a 41 pessoas, isto é, os 36 a 38 agendados mais as 3 do piloto.
- **Alocação:** as pessoas agendadas são alocadas às sequências em blocos sorteados de 4 (um por sequência). 36 agendados formam 9 blocos completos; 37 e 38 não formam blocos completos.
- **n fixo:** o n é fixado antes da coleta, sem parada antecipada por causa de resultados.
- **Regra operacional provisória de fechamento, a validar pelo professor (P2):**
  1. Uma falta ou sessão inválida (falha técnica, interrupção) é reposta na mesma sequência.
  2. A análise primária usa os 8 primeiros participantes analisáveis de cada sequência, na ordem de realização das sessões.
  3. Excedentes de uma sequência já completa são dispensados antes da sessão; se a sessão já ocorreu, os dados ficam arquivados e são descritos, mas fora da análise primária.
  4. Se a coleta terminar com sequências incompletas, analisam-se apenas os k blocos completos, em que k é o menor número de participantes analisáveis entre as quatro sequências (k ≤ 8), com a perda de poder correspondente.
- **Aviso:** essa regra não foi aprovada pelo professor nem confirmada como compatível com o enunciado. Não há n mínimo definido abaixo da meta (P6).

Poder estatístico: o poder foi estimado por simulação conjunta com Holm de 3 sobre RQ1, RQ2 e RQ3 (script `power_analysis.py`, versão 3.2, semente 20261117, 20.000 simulações por célula, erro de simulação de cerca de 0,004), com efeito nominal d_z = 0,6 em RQ2 e RQ3 e conclusão marginal de 90% no computador e 75% no celular na RQ1. Valores para n = 32 (arquivo `results_v3_2.json`):

| Cenário de premissas | RQ1 | RQ2 | RQ3 |
|---|---|---|---|
| S0, idealizado (sem diferença de conjunto, período ou sequência) | 0,778 | 0,883 | 0,875 |
| S1, realista | 0,671 | 0,821 | 0,818 |
| S2, adverso | 0,557 | 0,650 | 0,649 |

Os parâmetros de S1 e S2 (diferença de dificuldade entre conjuntos, efeito de período, variação entre tarefas, ruído de sequência e correlação entre as RQs) foram escolhidos pelo grupo sem dados de apoio e estão no script. No cenário realista, o d_z efetivo de RQ2 e RQ3 cai para 0,557 e, no adverso, para 0,469. Limitações: (i) os valores são estimativas condicionadas às premissas da simulação, não garantias; (ii) o poder da RQ1 fica abaixo de 0,80 mesmo no cenário realista; (iii) a simulação da RQ2 não representa a massa de tarefas no teto de 300 s, as tarefas não concluídas nem a relação entre falha e tempo, e não comprova o poder real nessas condições; (iv) a RQ4 não tem poder calculado como confirmatória.

Tarefas: 3 por conjunto, todas de consulta e sem login, encerradas na tela anterior a qualquer formulário. Candidatas a validar no piloto: descobrir como pedir poda de árvore; descobrir os documentos para um alvará; descobrir como solicitar reparo de buraco na via; descobrir onde emitir a segunda via de uma guia municipal. O cronômetro inicia quando o moderador termina a leitura e diz "pode começar" e para quando o participante chega à tela-alvo definida para a tarefa e declara que terminou. Limite de 5 minutos (300 s) por tarefa.

Tarefas não concluídas: a regra será definida antes da coleta e aplicada igualmente nos dois dispositivos, sem decisão do moderador durante a sessão (o moderador só registra o evento e o tempo transcorrido). Pela proposta original, a tarefa que estoura o limite conta como não concluída, com tempo igual a 300 s, e o pedido de ajuda conta como não conclusão. O tempo de 300 s não é tempo real de conclusão. O tratamento do tempo da tarefa abandonada antes de 300 s e da encerrada por pedido de ajuda não está definido (P1). Não há limite de validade nem critério de exclusão por proporção de tarefas no teto; o relatório informa, por dispositivo, a quantidade e a proporção de tarefas que chegaram a 300 s (P3).

# 5. As 7 categorias da pesquisa (primeira versão)

| Categoria | Classificação | Justificativa |
|---|---|---|
| Natureza | Aplicada | Responde a um problema prático de um serviço público em produção, não busca teoria nova. |
| Objetivos | Explicativa (com parte descritiva) | Testa se o dispositivo causa diferença no desempenho; a auditoria descreve as barreiras. |
| Abordagem | Mista, predominantemente quantitativa | Métricas numéricas e testes estatísticos; comentários dos participantes e notas do moderador são analisados qualitativamente. |
| Procedimentos | Experimento controlado + avaliação de produto | O grupo manipula o dispositivo e contrabalanceia a ordem; a auditoria é uma inspeção sistemática contra a WCAG. |
| Tempo | Transversal | Cada participante é medido em uma única sessão; a auditoria é um retrato da versão do Portal no período da coleta. |
| Controle | Laboratório (in vitro) sobre software real | Ambiente, rede, roteiro e tarefas são fixados pelo grupo; o software não é controlado e pode mudar durante a coleta. |
| Nível de evidência | Experimento único com amostra por conveniência | Controle interno alto (contrabalanceamento, unidade de análise por participante), mas sem amostragem aleatória da população de BH: evidência causal local, generalização limitada. |

A classificação será revisada na S03 conforme o que de fato for executado (por exemplo, se a coleta terminar desbalanceada ou com perdas relevantes, o estudo passa a quase-experimento).

# 6. Coleta, instrumentação e ética

Roteiro da sessão com participante (cerca de 30 minutos):

1. Leitura e assinatura do termo de consentimento; participante recebe um código (P01, P02…), sem nome na base.
2. Questionário inicial: faixa etária, frequência de uso do Portal, autoavaliação de familiaridade digital.
3. Primeiro dispositivo: 3 tarefas, cada uma seguida do SEQ (1–7).
4. SUS do primeiro dispositivo.
5. Segundo dispositivo: 3 tarefas do outro conjunto, cada uma seguida do SEQ.
6. SUS do segundo dispositivo e pergunta aberta: "o que mais atrapalhou?".

Instrumentos:

- Planilha de observação padronizada: início e fim de cada tarefa (cronômetro), conclusão, erros (clique em caminho errado, volta, busca refeita) e passo onde ocorreram.
- Gravação de tela opcional, só com consentimento explícito, sem câmera nem áudio, apagada após a codificação.
- Formulário SUS e SEQ em versão validada em português.
- Auditoria: extensão axe DevTools e Lighthouse (modo mobile e desktop) no Chrome, acionadas manualmente pelo integrante B nas páginas que as tarefas percorrem (estimativa de 12 a 20 páginas), 3 execuções por página para o desempenho, registrando data, versão do Chrome e resultado em JSON exportado. Os resultados do axe e do Lighthouse são gerados automaticamente pelas ferramentas na página aberta, e o checklist WCAG complementar é manual.

Natureza das medições:

- **Participantes:** navegam manualmente pelo Portal, em dispositivos e navegador padrão.
- **Auditoria:** um integrante aciona axe DevTools e Lighthouse manualmente, uma página por vez, em páginas selecionadas. As ferramentas realizam verificações automatizadas na página aberta, e o Lighthouse carrega a página durante cada execução.
- **Não há:** crawler, varredura de páginas, teste de carga ou coleta automatizada em larga escala.
- **Pendente:** o enunciado pede respeito aos termos de uso e ao robots.txt. A compatibilidade das ferramentas de auditoria com o robots.txt e com os termos de uso não foi estabelecida (P8, P12).

Rótulo WCAG para a RQ4: o rótulo é atribuído, sempre que tecnicamente possível, no nível do elemento usado no passo da tarefa (campo, botão, link ou região com que a pessoa interage), e não à página inteira. Uma violação em outra parte da página não torna o passo "com violação". "Sem violação" significa sempre "sem violação detectada por axe e pelo checklist manual", e não ausência comprovada de violação. Passos em que o elemento correspondente não puder ser identificado formam uma categoria própria, "indeterminado": não são classificados como com nem como sem violação, e a quantidade e o motivo são reportados.

Regras de ética:

- Nenhum crawler nem coleta automatizada em larga escala contra o Portal, em respeito ao robots.txt (`Disallow: /`). A navegação é manual e as ferramentas de auditoria são acionadas manualmente em páginas selecionadas.
- Nenhum login, nenhum formulário enviado, nenhuma conta ou dado real dos participantes. A tarefa termina antes do login gov.br.
- Nenhum dado pessoal armazenado: só o código do participante, faixas e respostas.
- A validação do professor sobre o uso das ferramentas de auditoria é mantida como pendência (P12). Se o professor discordar, a auditoria sai e o estudo fica só com participantes.
- A necessidade de apreciação por comitê de ética é decisão do professor ou da instituição (P11).

Versionamento: dados brutos (planilhas anonimizadas e JSON da auditoria) no repositório do grupo, com dicionário de dados e registro de data e versão do Portal observada em cada sessão.

# 7. Plano de análise

Cada métrica recebe o teste permitido pela sua escala e pelo desenho pareado. A unidade de análise das RQ1 a RQ3 é o participante.

| Hipótese | Dado | Descritiva | Teste | Tamanho do efeito |
|---|---|---|---|---|
| RQ1 conclusão | Contagem de tarefas concluídas (0 a 3) por participante e dispositivo | Média e distribuição por dispositivo; IC 95% da diferença na taxa de conclusão por bootstrap de participantes | Wilcoxon pareado sobre a diferença celular − computador (`scipy.stats.wilcoxon`, `zero_method="wilcox"`). Não se usa McNemar, porque as tarefas de cada dispositivo pertencem a conjuntos diferentes | r de postos |
| RQ2 tempo | Média, por participante e dispositivo, do log do tempo gasto (teto de 300 s) | Mediana, IQR, boxplot por dispositivo; quantidade e proporção de tarefas no teto por dispositivo | t pareado na diferença das médias do log; o exponencial da diferença média estima a razão das médias geométricas dos tempos (com teto), não a razão das médias aritméticas. Sensibilidade: Wilcoxon pareado e análise só das tarefas concluídas (esta tem viés de seleção) | d_z |
| RQ3 SUS | Intervalar, pareado | Média e DP por dispositivo | t pareado | d_z |
| RQ4 violações × erros | Taxa de erro por passo, por grupo: com violação, sem violação detectada e indeterminado | Tamanho de cada grupo, contagens de erros, pessoas expostas (denominadores), taxas por passo e diferença observada entre os grupos; tabela 2×2 (Fisher exato apenas descritivo) | Nenhum teste inferencial e nenhum p-valor (ver abaixo) | Diferença observada entre as médias das taxas (descritiva) |
| SEQ e SUS contra 68 | Ordinal; intervalar | Mediana e distribuição por nível; média e DP, com a referência de 68 pontos | Nenhum (só descritivos) | — |
| Auditoria | Contagens por página e severidade | Totais, mediana por página, top 10 regras WCAG violadas | Descritiva apenas | — |

Correção para múltiplos testes: Holm sobre RQ1, RQ2 e RQ3 (α = 0,05 na família de 3). A RQ4 fica fora da correção. O teste primário de cada RQ é fixado antes da coleta, sem escolher o teste olhando o resultado de normalidade.

RQ4, análise exploratória descritiva: a unidade de análise é o passo da tarefa (página × dispositivo). A taxa de erro de um passo é o número de erros registrados dividido pelas pessoas que chegaram a ele. Não se calcula p-valor nesta versão. Um teste de permutação dos rótulos entre passos só tem validade defensável sob a hipótese de permutabilidade dos rótulos em relação às taxas de erro, e essa hipótese não pode ser sustentada com os materiais atuais: (i) os rótulos WCAG são detectados, não randomizados; (ii) a complexidade da página, a posição no fluxo e o tipo de tarefa podem coincidir com a presença de violações; (iii) os passos de uma tarefa são sequenciais, de modo que um erro pode impedir o passo seguinte; (iv) a mesma página é observada nos dois dispositivos, o que correlaciona passos; (v) os passos têm denominadores diferentes, conforme o número de pessoas que os alcançou. Os pontos (iii) a (v) não foram simulados. Existirem permutações em número suficiente é uma condição matemática, não uma garantia de validade. Se o grupo e o professor definirem um critério de adequação e uma estratégia que respeite essas dependências, um teste exploratório poderá ser considerado (P4); até lá, o relatório da RQ4 apresenta apenas: o tamanho de cada grupo de passos, as contagens de erros, os denominadores, as taxas por passo, a diferença observada e a quantidade de passos indeterminados. Um padrão observado indica associação nos passos observados; não indica causa e não se estende às demais páginas do Portal.

Controle de ordem: verificar efeito de período e de conjunto de tarefas (A × B) antes de interpretar o efeito do dispositivo. Com 8 participantes por sequência essa checagem tem poder baixo, não calculado; não encontrar diferença não prova que o efeito de ordem seja nulo. Erro tipo I: as três hipóteses confirmatórias são corrigidas por Holm. Sequências desbalanceadas podem elevar o erro tipo I acima de 0,05 (em simulações com n = 24 e 28 o erro familiar chegou a 0,068 e 0,073 no cenário realista; n = 32 não foi simulado); por isso a meta é o mesmo número por sequência.

Estimativa de impacto (S03): o resultado principal é o impacto relativo, composto por (i) a razão das médias geométricas dos tempos gastos (RQ2), com intervalo de confiança, (ii) a diferença no número de tarefas concluídas (RQ1) e (iii) a diferença de SUS (RQ3). A razão das médias geométricas não é convertida diretamente em segundos nem em horas: o tempo total depende da média aritmética, que em geral difere da geométrica, e o teto de 300 s não é tempo real de conclusão. A conversão em horas do cidadão é uma análise secundária, hoje pendente: exige uma métrica compatível (ainda não definida) e entradas externas (solicitações mensais por serviço, fração de uso por celular e distribuição de tempos) que o grupo não tem (P5). Os números públicos já coletados, como as 496.956 solicitações de 2023, servem apenas para contextualizar a escala e não para calcular horas. Qualquer extrapolação mantém o intervalo de confiança e não vai além dos serviços das tarefas testadas.

Ferramentas: Python (pandas, scipy, statsmodels) em notebook versionado; gráficos e dashboard reaproveitando a base do Lab04.

# 8. Ameaças à validade (preliminar)

| Tipo | Ameaça | Mitigação |
|---|---|---|
| Conclusão | Amostra de 32 deixa o poder abaixo de 0,80 na RQ1 e, em cenários adversos, também em RQ2 e RQ3; vários testes inflam o erro tipo I | Poder simulado antes da coleta; Holm sobre RQ1 a RQ3; relatar tamanho do efeito e IC, não só p-valor; apresentar o poder como condicionado às premissas |
| Conclusão | Faltas e substituições desbalanceiam as sequências, o que pode elevar o erro tipo I acima de 0,05 | Blocos de 4, reposição na mesma sequência; análise só de blocos completos se terminar desbalanceado (regra provisória, P2) |
| Conclusão | Medição de tempo manual imprecisa | Cronômetro com regra fixa de início e fim; segundo integrante confere uma amostra das gravações |
| Conclusão | Tarefas no teto de 300 s não têm tempo real de conclusão; o teto não foi simulado no poder | Relatar quantidade e proporção por dispositivo; análises de sensibilidade; regra única definida antes da coleta |
| Interna | Aprendizado: a segunda rodada fica mais rápida | Contrabalanceamento completo das quatro sequências; testar efeito de período (poder baixo) |
| Interna | O Portal muda durante a coleta (nova versão, instabilidade) | Concentrar a coleta em até duas semanas; registrar data e hash dos pacotes ui-package carregados em cada sessão |
| Interna | Moderador induz o participante | Roteiro lido igual; moderador não ajuda e não decide casos durante a sessão; pedido de ajuda conta como não conclusão |
| Interna | RQ4: rótulos WCAG não randomizados, passos sequenciais e dependentes, mesma página nos dois dispositivos, denominadores diferentes, complexidade e posição no fluxo associadas a violações | Rótulo no elemento do passo; passos indeterminados reportados; análise descritiva sem p-valor; sem causalidade nem generalização |
| Construto | Tarefas sem login não representam o uso completo (envio do pedido) | Declarar que o construto é "encontrar e iniciar" o serviço, não concluí-lo |
| Construto | Nota Lighthouse não equivale a acessibilidade real; "sem violação" significa "sem violação detectada" | Usar contagem de violações axe e erros de pessoas como medidas principais; Lighthouse só complementar |
| Externa | Amostra de estudantes e conhecidos, mais jovem e digital que a população de BH | Registrar perfil; não generalizar para idosos ou pessoas com deficiência; recrutar fora da turma quando possível |
| Externa | Um aparelho e um navegador específicos | Declarar modelo e versão; resultado vale para Android/Chrome em rede estável |
| Externa | Poucos serviços testados entre 1.118 solicitáveis | Escolher serviços de alta demanda; não extrapolar para o catálogo inteiro |

# 9. Piloto, reaproveitamento e organização

Coleta piloto (entrega da S01): 3 participantes, cada um nos dois dispositivos, mais a auditoria de 3 páginas. Objetivos: confirmar que as tarefas têm dificuldade parecida entre os conjuntos A e B, que nenhuma exige login, que cabem em 30 minutos e que a planilha captura tudo. Dados do piloto não entram na análise final.

Reaproveitamento dos laboratórios anteriores:

| Lab | O que reaproveitamos | O que é novo |
|---|---|---|
| Lab01 | Kanban no GitHub Projects para as sprints | Coleta manual por pessoas, sem API |
| Lab02 | Desenho com tratamentos e participantes, termo de consentimento | Contrabalanceamento intrassujeitos das quatro sequências |
| Lab03 | Visão de métricas de operação (DORA) como contexto | Métricas de qualidade em uso (ISO/IEC 25010) e WCAG |
| Lab04 | Escolha do teste, simulação de poder e de erro tipo I, dashboard | Testes pareados (Wilcoxon, t pareado), correção de Holm e análise de impacto relativo |

Papéis no trio:

| Integrante | Papel | Responsabilidades |
|---|---|---|
| A | Planejamento e Método | Critérios do software, pedido via LAI, GQM, hipóteses, 7 categorias, ameaças |
| B | Instrumentação e Operação | Tarefas, roteiro, termo, planilha, sessões, auditoria, validação e anonimização dos dados |
| C | Análise e Impacto | Simulação de poder, notebook de análise, gráficos, tamanho do efeito, estimativa de impacto relativo |

Sprints (as datas reais de S02, S03 e da entrega final seguem o cronograma da disciplina, P13):

| Sprint | Entrega |
|---|---|
| S01 | Esta proposta, aceite do professor sobre a auditoria, pedido via LAI enviado, piloto com 3 participantes |
| S02 | 32 sessões analisáveis (36 a 38 agendadas), auditoria completa, dados validados e versionados, análise descritiva e testes, ameaças atualizadas |
| S03 | Estimativa de impacto relativo com fontes (conversão em horas só como análise secundária, P5), 7 categorias revisadas, conclusões e limites, rascunho do documento e da apresentação |
| Final | Documento e apresentação de 10 minutos (sugestão: reunião simulada com o gestor do Portal na PBH) |

Link do repositório e do GitHub Projects: a preencher (P14).

# 10. Pendências

Tipos: **Professor** (validação externa), **Grupo** (decisão dos integrantes), **Documental** (evidência ou fonte ainda não obtida).

| ID | Pendência | Tipo | Responsável |
|---|---|---|---|
| P1 | Tratamento do tempo da tarefa abandonada antes de 300 s e da encerrada por pedido de ajuda (RQ2); deve ser definido antes da coleta | Professor | Professor |
| P2 | Validação da regra operacional provisória de fechamento dos blocos (seção 4) e da análise só de blocos completos | Professor | Professor |
| P3 | Qualquer critério formal de validade ou exclusão por proporção de tarefas no teto de 300 s (nenhum foi adotado) | Professor | Professor |
| P4 | Teste inferencial na RQ4: critério de adequação dos grupos e dos denominadores, estatística, unidade de análise e verificação da permutabilidade | Grupo e Professor | Grupo, com validação do professor |
| P5 | Conversão do impacto em horas (análise secundária): métrica compatível e dados externos de solicitações mensais, uso por celular e distribuição de tempos | Grupo | Grupo |
| P6 | n mínimo abaixo da meta de 32 e como declarar o estudo nesse caso | Grupo | Grupo |
| P7 | Como foram obtidos a leitura do HTML da página inicial e o tempo de resposta do original (HTTP 200 em 0,49 s). A frase do tempo de resposta foi retirada do texto até haver evidência de uma medição compatível com a navegação manual | Documental | Grupo |
| P8 | Leitura dos termos de uso do Portal e registro dessa leitura | Documental | Grupo |
| P9 | Conferência no navegador do número de habitantes de BH no IBGE Cidades | Documental | Grupo |
| P10 | Envio do pedido via LAI ao canal de transparência da PBH e resposta | Documental | Grupo |
| P11 | Necessidade de apreciação por comitê de ética (decisão do professor ou da instituição) | Professor | Professor ou instituição |
| P12 | Validação do uso de axe DevTools e Lighthouse, acionados manualmente, frente ao robots.txt e aos cuidados de ética do enunciado | Professor | Professor |
| P13 | Datas reais de S02, S03 e da entrega final, e janela de coleta | Documental | Grupo, conforme o cronograma da disciplina |
| P14 | Link do repositório e do GitHub Projects; conferência da autoria no cabeçalho | Documental | Grupo |

# Fontes

Acessadas em 16/11/2026.

- Portal de Serviços da PBH e seu robots.txt
- PBH: em uma década, PBH amplia em mais de 500% serviços digitais (05/10/2026) [título conforme a notícia; corrigido em 22/11/2026, ver FONTE_DA_VERDADE D9]
- PBH: Belo Horizonte é eleita cidade mais digital do Brasil pelo terceiro ano (18/08/2026)
- PBH: área de modernização destaca principais resultados (27/12/2023)
- PBH: Prefeitura lança novo Portal de Serviços (12/05/2020)
- SYDLE ONE
- IBGE Cidades: Belo Horizonte (número a conferir no navegador, P9)
