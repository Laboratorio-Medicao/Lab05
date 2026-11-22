# FONTE DA VERDADE — LAB05

**Versão 2.1 · criada em 20/11/2026** · Referência central e permanente do projeto LAB05.
Qualquer pessoa ou agente de IA deve ler este arquivo antes de tocar em qualquer artefato do LAB05.

> Convenção de leitura: este documento separa sempre **exigido** (enunciado), **decidido** (professor), **planejado** (proposta), **executado** (evidência no repositório) e **resultado** (dado observado). Hoje existe apenas planejamento. **Não existe nenhum resultado empírico.**

Fontes consultadas (links relativos):

| Sigla | Arquivo | Papel |
|---|---|---|
| ENUNCIADO | [docs/enunciado/ENUNCIADO_LAB05.pdf](./docs/enunciado/ENUNCIADO_LAB05.pdf) | Requisitos do professor (impressão da página do Canvas em 20/11/2026, 7 páginas; arquivo renomeado, ver §19) |
| PROPOSTA | [docs/proposta/LAB05_S01_Proposta_FINAL.md](./docs/proposta/LAB05_S01_Proposta_FINAL.md) | Planejamento metodológico do grupo, revisado em 17/11/2026 (original de 16/11/2026) |
| RELATÓRIO | [docs/relatorios/RELATORIO_FECHAMENTO_LAB05.md](./docs/relatorios/RELATORIO_FECHAMENTO_LAB05.md) | Auditoria e fechamento da S01, de 17/11/2026 |

---

## 1. Identificação do projeto

| Campo | Valor | Fonte |
|---|---|---|
| Laboratório | Laboratório 05 — Experimento em Software Real (LAB05), 20 pontos | ENUNCIADO |
| Curso / disciplina | Engenharia de Software — Laboratório de Experimentação de Software, 6º período, noite, Campus Lourdes (PUC Minas, PLU), 2026/2 | ENUNCIADO |
| Professor | Danilo Maia | ENUNCIADO |
| Objetivo acadêmico | Planejar, executar e analisar um experimento sobre software real, em operação e de alto impacto; responder "o que o estudo mostrou?" e "o que isso significa para quem usa esse software?" | ENUNCIADO |
| Software estudado | Portal de Serviços da Prefeitura de Belo Horizonte (PBH), construído sobre a plataforma SYDLE ONE | PROPOSTA §1 |
| Estudo | Experimento intrassujeitos celular × computador (32 participantes analisáveis planejados) + auditoria WCAG complementar | PROPOSTA |
| Integrantes | **Não confirmados.** O cabeçalho da proposta traz apenas "@Someone"; papéis A, B e C existem, mas sem nomes. Conferência da autoria é a pendência P14 | PROPOSTA, P14 |
| Sprint atual | **S01 (Proposta) fechada com pendências externas** em 17/11/2026. Piloto e aceite do professor **não têm evidência de execução**; pedido LAI informado como enviado em 22/11/2026, sem protocolo arquivado (ver §13) | RELATÓRIO |
| Link repositório / GitHub Projects | A preencher (P14) | PROPOSTA §9 |

---

## 2. Fonte de autoridade e regras do projeto

### 2.1 Hierarquia (do mais ao menos autoritativo)

1. **ENUNCIADO** — o que o professor exige.
2. **Decisões documentadas do professor** — validações e orientações efetivamente recebidas. **Hoje não existe nenhum registro.** Todas as pendências do tipo "Professor" estão abertas.
3. **PROPOSTA** — planejamento adotado pelo grupo.
4. **RELATÓRIO** — histórico de auditoria, correções e pendências.
5. **Artefatos do repositório** — provam o que existe de fato.

### 2.2 Resolução de divergências

- Entre fontes de níveis diferentes, vale a de nível mais alto; a divergência é registrada na §18.
- Se o enunciado é omisso (não fixa n, número de hipóteses nem regra de descarte), vale a proposta, **marcada como decisão do grupo**, não como exigência.
- Se proposta e relatório divergem, a proposta é a fonte do texto metodológico; o relatório é a fonte do histórico. Registrar e corrigir a que estiver errada, **com justificativa**.
- Afirmação sem artefato correspondente no repositório é tratada como **não verificada**.

### 2.3 O que pode ser considerado comprovado

| Estado | Critério mínimo |
|---|---|
| Exigido | Está no ENUNCIADO |
| Aprovado pelo professor | Há registro documentado (mensagem, ata, comentário no Canvas) anexado ao repositório |
| Planejado | Está na PROPOSTA |
| Executado | Existe artefato no repositório (planilha, JSON, log, gravação anonimizada, script rodado) |
| Verificado | Executado **e** conferido por segunda pessoa/ferramenta, com registro |
| Resultado | Dado observado, produzido por coleta real |

Estimativas e premissas (inclusive o poder simulado) **não são resultados**.

### 2.4 Atualização desta fonte

- Toda decisão relevante, resposta do professor, resolução de pendência ou execução de etapa deve ser registrada aqui **no mesmo commit** que altera o artefato.
- Atualizar o cabeçalho (versão e data) e a §13/§14; manter histórico na §19.
- Pendência só muda para "Encerrada" com a evidência citada na linha.

---

## 3. O que o professor exige (ENUNCIADO)

### 3.1 Obrigatório vs. sugestão

O enunciado usa linguagem explícita. Exigências firmes (**OBRIGATÓRIO**) são poucas; boa parte é **SUGESTÃO**.

| Tema | Conteúdo | Natureza |
|---|---|---|
| Objetivo | Experimento sobre software real, em operação, de alto impacto; o grupo escolhe software, pergunta, tipo de estudo, métricas e formatos | **Obrigatório** |
| Critérios do software | Real; em operação; alto impacto, "com evidências (números e fontes)". O texto diz "o ideal é que atenda aos três" | Obrigatório (com evidências); "ideal" é a formulação do texto |
| Repositórios públicos do GitHub | **Proibidos** como objeto (minerar commits/issues/PRs, analisar código-fonte). Foco é o software em operação | **Obrigatório (restrição)** |
| Cada grupo, um software | Dois grupos não podem estudar o mesmo software | **Obrigatório (restrição)** |
| Ética | Sem teste de carga/estresse em sistema de terceiros; respeitar termos de uso e robots.txt; **no máximo 1 requisição por segundo**; sem dados pessoais; com participantes: consentimento e sem contas/dados reais deles | **Obrigatório (restrição)** |
| Caminhos de pesquisa | Rodar no ambiente do grupo; medir de fora; estudar com pessoas; analisar dados de operação; ouvir quem usa/mantém; avaliar qualidade do produto (ISO/IEC 25010, WCAG com axe/Lighthouse); outro caminho a combinar com o professor na S01. "Inspirações, não lista fechada"; combinar caminhos é **valorizado** | Sugestão |
| Experimento controlado | Não é obrigatório; quase-experimento, observacional, survey ou análise de dados de operação valem. O importante é **classificar corretamente** e discutir a força da evidência | Sugestão (classificação correta é exigida na prática) |
| Conceitos de Medição e Experimentação | Goodhart/Campbell/McNamara; GQM (template de Basili); entidades e atributos (produto/processo/recurso, interno/externo, direta/derivada); escalas e estatísticas permitidas; métricas de produto/processo/recurso (LOC, CK, Halstead, ISO 25010, MTBF/MTTR, DORA, SLI/SLO); 7 categorias; planejamento (hipóteses, variáveis, sujeitos, design, instrumentação, operação); ameaças (4 tipos); análise (descritiva, teste adequado, tamanho do efeito). "O grupo escolhe quais conceitos fazem sentido" | Sugestão (escolha do grupo), mas a avaliação é "como o grupo aplica o que aprendeu" |
| 7 categorias | Natureza, objetivos, abordagem, procedimentos, tempo, controle, nível de evidência, cada uma com justificativa (Aula 8) | Sugestão no texto; **exigência prática**: S01 pede "primeira versão" e S03 "revisadas e justificadas" |
| Ameaças à validade | Conclusão, interna, construto, externa, com mitigação | Sugestão; apresentação deve cobri-las (item 7 da lista) |
| Reaproveitamento Labs 01–04 | Lab01 coleta via API/Kanban; Lab02 desenho com tratamentos/participantes; Lab03 DORA; Lab04 escolha de teste, simulação de erro tipo I e poder, dashboard. Mostrar o que foi reaproveitado vs. novo | Sugestão |
| Impacto (mundo real) | Traduzir resultado para empresas/usuários; usar números públicos com fonte; deixar claro **o que não é possível afirmar** (validade externa) | Sugestão forte |
| Papéis do trio | A Planejamento e Método; B Instrumentação e Operação; C Análise e Impacto | Sugestão (o grupo pode adaptar) |
| Sprints | Conteúdo de cada sprint é sugestão; o grupo pode reorganizar | Sugestão |
| Documento e apresentação | **10 minutos**, ambos em formato livre. O professor pode pedir a qualquer integrante que explique qualquer parte | Obrigatório (duração, 10 min); formato livre |
| Pontuação / prazo | 20 pontos (4 × 5). Prazo "conforme cronograma da disciplina" (datas não constam do enunciado) | Obrigatório |
| Link repositório / GitHub Projects | Campo `<preencher>` no enunciado | Esperado |

### 3.2 Entregas por sprint (sugestão de conteúdo, 5 pontos cada)

| Sprint | Conteúdo sugerido |
|---|---|
| Lab05S01 | Proposta: software com evidências dos três critérios + pergunta de pesquisa + caminho(s) escolhido(s) + primeira versão das 7 categorias + plano de coleta e de análise + **coleta piloto** |
| Lab05S02 | Coleta completa + dados validados e versionados + análise (descritiva, testes e tamanho do efeito, quando couber) + ameaças à validade |
| Lab05S03 | Impacto para empresas/usuários + 7 categorias revisadas e justificadas + conclusões e limitações + rascunho do documento e da apresentação |
| Documento Final e Apresentação | Documento e apresentação de 10 minutos, formato livre |

### 3.3 Roteiro de conteúdo sugerido para documento/apresentação (ENUNCIADO §8)

(1) software, por que é real/operação/alto impacto, com números; (2) pergunta e caminho; (3) 7 categorias com justificativa; (4) conceitos da disciplina; (5) reaproveitado dos laboratórios; (6) resultados com análise adequada ao tipo e escala; (7) ameaças (4 tipos); (8) impacto e o que **não** é possível afirmar.

---

## 4. Contexto e objeto de estudo

**Portal de Serviços da Prefeitura de Belo Horizonte (PBH), sobre SYDLE ONE.** O objeto é o software em uso pelo cidadão, não código-fonte nem repositório (o que respeita a proibição de repositórios do GitHub).

### 4.1 Evidências (todas da PROPOSTA §1; acesso em 16/11/2026)

| Critério | Evidência | Fonte | Situação da evidência |
|---|---|---|---|
| Real | HTML da página inicial carrega pacotes `@sydle/pbh-components`, `@sydle/sydle-one-components`, `@sydle/service-desk-components`, com `org: "bhdigital"`. SYDLE ONE é vendida como plataforma de BPM, CRM e Service Desk | Página inicial do Portal; sydle.com/br | **Forma de obtenção do HTML não documentada (P7)** |
| Em operação | Portal no ar, lançado na plataforma atual em maio de 2020, com login único gov.br | PBH, 12/05/2020 | Citada; sem cópia arquivada no repositório |
| Alto impacto | 1.492 serviços catalogados, 1.118 solicitáveis pela internet; jan–set/2026, 92% das demandas à Prefeitura entraram por Portal ou app | PBH, 05/10/2026 | Citada |
| Alto impacto | 496.956 solicitações de serviço de jan–out/2023 (Portal + app + 156 + BH Resolve) | PBH, 27/12/2023 | Citada; soma de canais, não só Portal |
| Alto impacto | 2.315.560 habitantes (Censo 2022); BH eleita cidade mais digital do Brasil pelo 3º ano | IBGE Cidades; PBH, 18/08/2026 | **Número do IBGE a conferir no navegador (P9)** |

Nenhuma cópia das páginas-fonte está no repositório; a verificabilidade depende de reacesso às URLs.

### 4.2 Limitações

- **Acessos mensais ao Portal: desconhecidos.** Nenhuma página pública consultada informa. Pedido via LAI previsto (P10). **Não inventar esse número.**
- Os 496.956 de 2023 somam quatro canais e servem apenas de contexto de escala, não de cálculo de horas.
- O app BH SIM tem só 129 serviços (plano B Portal × app, descartado como principal por restringir tarefas comparáveis).

### 4.3 Restrição do robots.txt

O robots.txt do Portal contém `User-agent: *` e `Disallow: /`. Consequências adotadas: **sem crawler, sem varredura, sem coleta automatizada em larga escala**. A compatibilidade de axe DevTools e Lighthouse, acionados manualmente, com o robots.txt e com os termos de uso **não está comprovada nem refutada** (P8, P12). Ver também a divergência D3 (§18) sobre o limite de 1 requisição/segundo.

---

## 5. Perguntas de pesquisa e GQM

**Pergunta principal:** o cidadão consegue encontrar e iniciar um serviço no Portal com a mesma eficácia, eficiência e satisfação no celular e no computador?
**Complementar:** quais barreiras de acessibilidade (WCAG 2.2 AA) existem nas páginas dos serviços mais procurados, e elas coincidem com os pontos onde os participantes erram?

**Caminhos do enunciado combinados:** "estudar com pessoas" (principal) + "avaliar a qualidade do produto" (complementar).

**Objetivo GQM (Basili):** analisar o Portal de Serviços da PBH, com o propósito de avaliar, com respeito à usabilidade e à acessibilidade, do ponto de vista do cidadão, no contexto de usuários adultos realizando consultas sem login em celular e computador.

### 5.1 Perguntas e correspondência

| GQM | Pergunta | RQ | Papel |
|---|---|---|---|
| Q1 | O dispositivo altera a eficácia (nº de tarefas concluídas)? | RQ1 | Confirmatória |
| Q2 | O dispositivo altera o tempo nas tarefas (teto 300 s)? | RQ2 | Confirmatória |
| Q3 | O dispositivo altera a satisfação percebida? | RQ3 | Confirmatória |
| **Q4** | Quantas e quais violações WCAG existem nas páginas dos serviços da tarefa? | **nenhuma** | **Descritiva, sem hipótese** |
| **Q5** | As violações estão nos passos onde os participantes erram? | RQ4 | Exploratória, fora do Holm, descritiva |

### 5.2 Métricas

| Métrica | Q | Entidade | Atributo | Medida | Escala | Papel |
|---|---|---|---|---|---|---|
| Tarefa concluída (sim/não) | Q1 | Produto em uso | Eficácia (ext.) | Direta | Nominal | Insumo |
| **Tarefas concluídas por participante e dispositivo (0–3)** | Q1 | Produto em uso | Eficácia (ext.) | Derivada | Razão (contagem) | **Teste RQ1** |
| Taxa de conclusão (%) | Q1 | Produto em uso | Eficácia (ext.) | Derivada | Razão | Descritiva |
| Tempo na tarefa (s, teto 300 s) | Q2 | Processo (uso) | Eficiência (ext.) | Direta | Razão | Insumo |
| **Log-tempo médio por participante e dispositivo** | Q2 | Processo (uso) | Eficiência (ext.) | Derivada | Intervalar (log de razão) | **Teste RQ2** |
| Nº de erros por tarefa | Q2 | Processo (uso) | Eficiência (ext.) | Direta | Razão (contagem) | Descritiva |
| **Escore SUS (0–100)** | Q3 | Recurso (participante) sobre o produto | Satisfação (ext.) | Derivada | Intervalar (por convenção) | **Teste RQ3** |
| Item SUS (1–5) | Q3 | Recurso | Satisfação | Direta | Ordinal | Descritiva |
| SEQ pós-tarefa (1–7) | Q3 | Recurso | Dificuldade percebida | Direta | Ordinal | Descritiva |
| Nº de violações axe por página e severidade | Q4 | Produto | Acessibilidade (int.) | Direta | Razão; severidade ordinal | Descritiva |
| Nota Lighthouse de acessibilidade (0–100) | Q4 | Produto | Acessibilidade (int.) | Derivada | Ordinal (não intervalar) | Descritiva, complementar |
| LCP e CLS (Lighthouse mobile) | Q4 | Produto | Eficiência de desempenho | Direta | Razão | Descritiva |
| Taxa de erro por passo (erros ÷ pessoas que chegaram), por grupo: com violação / sem violação detectada / indeterminado | Q5 | Processo (uso) | Associação | Derivada | Razão | Exploratória descritiva |

**Entram em teste de hipótese apenas:** tarefas concluídas (RQ1), log-tempo médio (RQ2), SUS (RQ3).
**Só descritivos:** nº de erros por tarefa, item SUS, SEQ, SUS contra a referência de 68, taxa de conclusão em %, todas as métricas da Q4, e a taxa de erro por passo (RQ4).

**Armadilhas de medição (tema da disciplina):** a nota Lighthouse é "jogável" (Goodhart); página nota 100 pode ser inutilizável com leitor de tela. Por isso não é métrica principal; o desfecho principal é a conclusão da tarefa por pessoas (contra a Falácia de McNamara).

---

## 6. Hipóteses e desenho experimental

Todos os testes bicaudais, α = 0,05. **RQ1–RQ3 confirmatórias, família Holm de 3 testes. RQ4 exploratória, fora do Holm, descritiva, sem p-valor na versão atual.**

### 6.1 Hipóteses (definições da PROPOSTA §4, sem simplificação)

| RQ | H0 | H1 | Teste planejado |
|---|---|---|---|
| RQ1 | Não há diferença no número de tarefas concluídas entre celular e computador | Há diferença no número de tarefas concluídas entre celular e computador | Wilcoxon pareado sobre diferença celular − computador (`scipy.stats.wilcoxon`, `zero_method="wilcox"`). **Não** McNemar (tarefas de cada dispositivo vêm de conjuntos diferentes). Efeito: r de postos |
| RQ2 | A média, entre participantes, da diferença do log do tempo gasto (teto 300 s) (celular − computador) é zero, isto é, a razão das médias geométricas dos tempos (celular/computador) é 1 | A média da diferença do log do tempo é diferente de zero, isto é, a razão das médias geométricas é diferente de 1 | t pareado nas diferenças das médias do log. Efeito: d_z. O exponencial da diferença média estima a razão das médias geométricas **com teto**, não a razão das médias aritméticas |
| RQ3 | A diferença média de SUS (celular − computador) é zero | A diferença média de SUS é diferente de zero | t pareado. Efeito: d_z |
| RQ4 | A taxa de erro por passo é a mesma entre passos com violação WCAG e passos sem violação detectada por axe e pelo checklist manual (rótulos permutáveis em relação à taxa de erro) | A taxa de erro por passo é diferente entre os dois grupos | **Nenhum teste inferencial nem p-valor.** Teste de permutação só se a validade puder ser defendida (P4) |

Nota: o RQ2 mede "tempo gasto com teto de 300 s", que **não** é o tempo até concluir quando a tarefa falha.

### 6.2 Variáveis

| Tipo | Variável | Níveis |
|---|---|---|
| Independente | Dispositivo | Celular Android (Chrome) × computador (Chrome, tela ≥ 1366×768) |
| Dependentes | Tempo (teto 300 s), tarefas concluídas (0–3), erros, SEQ, SUS | — |
| Controladas | Rede, navegador, tarefas, roteiro, moderador | Mesma rede Wi-Fi, Chrome atual, roteiro lido igual, um moderador fixo |
| Bloqueio | Ordem do dispositivo e pareamento conjunto-dispositivo | Contrabalanceamento completo das 4 sequências |
| Covariáveis registradas | Idade (faixa), uso prévio do Portal, familiaridade digital, sequência | Questionário inicial, sem identificação |

### 6.3 Desenho

- **Intrassujeitos**, 1 fator de 2 níveis. Cada participante usa os dois dispositivos, com dois conjuntos de tarefas equivalentes (A e B).
- **4 sequências** (ordem do dispositivo × pareamento conjunto-dispositivo): celular-A/computador-B, celular-B/computador-A, computador-A/celular-B, computador-B/celular-A. É contrabalanceamento completo das quatro sequências, **não** quadrado latino.
- Ordem das 3 tarefas dentro do conjunto sorteada por participante.
- **Tarefas:** 3 por conjunto, só consulta, sem login, encerradas na tela anterior a qualquer formulário. **Candidatas (a validar no piloto, não definitivas):** poda de árvore; documentos para alvará; reparo de buraco na via; segunda via de guia municipal. Os conjuntos A e B ainda **não** estão definidos.
- **Cronômetro:** inicia quando o moderador termina a leitura e diz "pode começar"; para quando o participante chega à tela-alvo da tarefa e declara que terminou. Limite 300 s por tarefa.

### 6.4 Participantes, amostra e recrutamento

| Item | Valor |
|---|---|
| Meta | **32 analisáveis, 8 por sequência**. Adultos, por conveniência (colegas, familiares, funcionários da universidade); exclui quem trabalha no desenvolvimento do Portal |
| Agendamento | 36 a 38 (cobre 10%–15% de faltas; 32/0,90 ≈ 35,6; 32/0,85 ≈ 37,6). Percentuais são estimativas de planejamento, sem dados. Reservas incluídas nesse número |
| Piloto | 3 participantes, não repetem e não entram na análise final |
| Recrutamento total | 39 a 41 (36–38 + 3 do piloto) |
| Alocação | Blocos sorteados de 4 (um por sequência). 36 formam 9 blocos completos; 37 e 38 não formam blocos completos |
| n fixo | Fixado antes da coleta; sem parada antecipada por resultados |

**Regra operacional provisória de fechamento (NÃO aprovada pelo professor; P2):**
1. Falta ou sessão inválida (falha técnica, interrupção) é reposta na mesma sequência.
2. Análise primária usa os 8 primeiros analisáveis de cada sequência, por ordem de realização.
3. Excedentes de sequência completa são dispensados antes da sessão; se já ocorreu, dados arquivados e descritos, fora da análise primária.
4. Se terminar com sequências incompletas, analisam-se apenas os k blocos completos (k = menor n analisável entre as 4 sequências, k ≤ 8), com a perda de poder correspondente.

Não há n mínimo definido abaixo de 32 (P6).

### 6.5 Poder estatístico

Estimado por **simulação conjunta com Holm de 3** sobre RQ1–RQ3 (script `power_analysis.py` v3.2, semente 20261117, 20.000 simulações por célula, erro de simulação ≈ 0,004; d_z nominal = 0,6 em RQ2 e RQ3; conclusão marginal de 90% no computador e 75% no celular na RQ1). Valores para n = 32 (arquivo `results_v3_2.json`, **conforme citado**):

| Cenário | RQ1 | RQ2 | RQ3 |
|---|---|---|---|
| S0 idealizado | 0,778 | 0,883 | 0,875 |
| S1 realista | 0,671 | 0,821 | 0,818 |
| S2 adverso | 0,557 | 0,650 | 0,649 |

Em S1 o d_z efetivo de RQ2/RQ3 cai para 0,557; em S2, para 0,469.

**Limitações (obrigatório repetir ao citar poder):** (i) são estimativas condicionadas a premissas, não garantias; (ii) poder da RQ1 < 0,80 mesmo em S1; (iii) a simulação da RQ2 não representa a massa de tarefas no teto, as tarefas não concluídas nem a relação falha–tempo; (iv) a RQ4 não tem poder calculado como confirmatória; (v) parâmetros de S1 e S2 foram escolhidos pelo grupo sem dados de apoio; (vi) **o script e o JSON não estão no repositório** (D1, §18).

### 6.6 Tarefa não concluída, abandono e teto de 300 s

- A regra será definida **antes da coleta** e aplicada igualmente nos dois dispositivos; o moderador **só registra** evento e tempo, sem decidir durante a sessão.
- Pela proposta original: estourar 300 s = não concluída, tempo = 300 s; pedido de ajuda = não conclusão.
- 300 s **não** é tempo real de conclusão.
- **Indefinido (P1):** tempo da tarefa abandonada antes de 300 s e da encerrada por pedido de ajuda.
- **Sem** limite de validade nem critério de exclusão por proporção de tarefas no teto (P3); o relatório informa, por dispositivo, quantidade e proporção de tarefas que chegaram a 300 s.

---

## 7. As sete categorias da pesquisa (primeira versão — **preliminar**)

| Categoria | Classificação | Justificativa (resumo) |
|---|---|---|
| Natureza | Aplicada | Problema prático de serviço público em produção; não busca teoria nova |
| Objetivos | Explicativa (com parte descritiva) | Testa se o dispositivo causa diferença; a auditoria descreve barreiras |
| Abordagem | Mista, predominantemente quantitativa | Métricas e testes; comentários e notas do moderador analisados qualitativamente |
| Procedimentos | Experimento controlado + avaliação de produto | Manipula o dispositivo com contrabalanceamento; auditoria é inspeção sistemática contra a WCAG |
| Tempo | Transversal | Uma única sessão por participante; auditoria é retrato da versão do Portal no período |
| Controle | Laboratório (in vitro) sobre software real | Ambiente, rede, roteiro e tarefas fixados; software não controlado e pode mudar |
| Nível de evidência | Experimento único com amostra por conveniência | Controle interno alto, sem amostragem aleatória de BH: evidência causal local, generalização limitada |

**Classificação sujeita a revisão na S03** conforme a execução real (ex.: coleta desbalanceada ou com perdas relevantes → passa a quase-experimento).

---

## 8. Plano de coleta e instrumentação

### 8.1 Roteiro da sessão (~30 min)

1. Termo de consentimento; código P01, P02… (sem nome na base).
2. Questionário inicial: faixa etária, frequência de uso do Portal, familiaridade digital.
3. Primeiro dispositivo: 3 tarefas, cada uma seguida de SEQ (1–7).
4. SUS do primeiro dispositivo.
5. Segundo dispositivo: 3 tarefas do outro conjunto, cada uma seguida de SEQ.
6. SUS do segundo dispositivo + pergunta aberta "o que mais atrapalhou?".

### 8.2 Instrumentos

- **Planilha de observação padronizada:** início/fim por tarefa (cronômetro), conclusão, erros (clique em caminho errado, volta, busca refeita) e passo onde ocorreram. *Ainda não existe no repositório.*
- **Gravação de tela:** opcional, só com consentimento explícito, sem câmera nem áudio, apagada após codificação.
- **SUS e SEQ:** versão validada em português (fonte da versão a registrar).
- **Registro de versão:** data, hash dos pacotes `ui-package` carregados e versão do Portal em cada sessão.

### 8.3 Navegação manual × verificações automatizadas

| Atividade | Quem/como | Natureza |
|---|---|---|
| Uso do Portal nas tarefas | Participantes, manualmente, dispositivo e navegador padrão | Navegação manual |
| Auditoria | Integrante B aciona **axe DevTools** e **Lighthouse** (mobile e desktop) no Chrome, **manualmente, uma página por vez**, em 12–20 páginas selecionadas percorridas pelas tarefas; 3 execuções por página para desempenho; registra data, versão do Chrome e JSON exportado | Ferramentas executam verificações automatizadas **sobre a página aberta**; o Lighthouse recarrega a página a cada execução |
| Checklist WCAG complementar | Manual | Inspeção |

**Não há:** crawler, varredura de páginas, teste de carga ou coleta automatizada em larga escala. Este estudo **não deve ser descrito** como crawler ou varredura.

### 8.4 Rótulo WCAG para a RQ4

Atribuído, sempre que possível, ao **elemento** usado no passo (campo, botão, link, região), não à página inteira. "Sem violação" = "sem violação detectada por axe e checklist manual", nunca ausência comprovada. Passos cujo elemento não possa ser identificado formam a categoria **"indeterminado"** (quantidade e motivo reportados).

### 8.5 Ética, anonimização e versionamento

- Sem crawler; sem login; sem formulário enviado; sem conta ou dado real dos participantes; tarefa termina antes do login gov.br.
- Nenhum dado pessoal armazenado: só código do participante, faixas e respostas. Gravação apagada após codificação.
- Consentimento obrigatório. Necessidade de apreciação por comitê de ética: decisão do professor/instituição (P11).
- Se o professor discordar do uso de axe/Lighthouse, **a auditoria sai** e o estudo fica só com participantes (P12).
- Dados brutos (planilhas anonimizadas e JSON da auditoria) no repositório, com dicionário de dados e registro de data/versão do Portal.

### 8.6 Limitações da coleta

Moderador único (viés possível); cronometragem manual (conferência de amostra por segundo integrante); um aparelho/navegador específico; software de terceiros que pode mudar durante a coleta (janela de até 2 semanas planejada; P13 define a janela real); amostra por conveniência.

---

## 9. Plano de análise

Cada métrica recebe o teste permitido pela escala e pelo desenho pareado.

| Análise | Unidade | Descritiva | Inferência? | Teste | Efeito / IC |
|---|---|---|---|---|---|
| RQ1 conclusão | Participante | Média e distribuição por dispositivo | **Sim (Holm)** | Wilcoxon pareado | r de postos; IC 95% da diferença da taxa de conclusão por bootstrap de participantes |
| RQ2 tempo | Participante (média do log por dispositivo) | Mediana, IQR, boxplot; quantidade e proporção de tarefas no teto por dispositivo | **Sim (Holm)** | t pareado no log | d_z; exp(diferença média) = razão das médias geométricas (com teto), com IC. **Sensibilidade:** Wilcoxon pareado; análise só das concluídas (viés de seleção) |
| RQ3 SUS | Participante | Média e DP por dispositivo | **Sim (Holm)** | t pareado | d_z |
| RQ4 violações × erros | **Passo (página × dispositivo)** | Tamanho de cada grupo, contagens de erros, denominadores, taxas por passo, diferença observada, nº de indeterminados; tabela 2×2 (Fisher apenas descritivo) | **Não** | Nenhum, sem p-valor | Diferença observada entre médias das taxas (descritiva) |
| SEQ, SUS vs. 68 | — | Mediana/distribuição; média/DP com referência de 68 | Não | — | — |
| Auditoria (Q4) | Página | Totais, mediana por página, top 10 regras WCAG violadas | Não | — | — |

- **Holm** sobre RQ1–RQ3 (α = 0,05 na família de 3). Teste primário de cada RQ fixado **antes** da coleta, sem escolher teste pelo resultado de normalidade.
- **Controle de ordem:** verificar efeito de período e de conjunto (A × B) antes de interpretar o dispositivo. Com 8 por sequência o poder dessa checagem é baixo e **não calculado**; não encontrar efeito não prova que seja nulo.
- **Erro tipo I:** sequências desbalanceadas podem elevá-lo acima de 0,05 (simulações n = 24 e 28: 0,068 e 0,073 no cenário realista; **n = 32 não foi simulado**). Por isso a meta é o mesmo n por sequência.
- **RQ4 — por que sem p-valor:** permutabilidade dos rótulos não defensável: (i) rótulos detectados, não randomizados; (ii) complexidade, posição no fluxo e tipo de tarefa podem coincidir com violações; (iii) passos sequenciais (erro impede o seguinte); (iv) mesma página nos dois dispositivos; (v) denominadores diferentes. Os pontos (iii)–(v) não foram simulados. Um teste exploratório só entra se grupo e professor definirem critério e estratégia (P4). Um padrão observado indica associação nos passos observados, **não** causa e **não** se estende ao resto do Portal.
- **Ferramentas:** Python (pandas, scipy, statsmodels) em notebook versionado; gráficos/dashboard reaproveitando a base do Lab04.

---

## 10. Ameaças à validade (PROPOSTA §8)

| Tipo | Ameaça | Consequência | Mitigação planejada |
|---|---|---|---|
| Conclusão | Amostra de 32 deixa poder < 0,80 na RQ1 e, em cenários adversos, em RQ2/RQ3; múltiplos testes inflam erro tipo I | Falsos negativos; falsos positivos | Poder simulado antes da coleta; Holm; reportar efeito e IC; poder apresentado como condicional |
| Conclusão | Faltas e substituições desbalanceiam sequências | Erro tipo I > 0,05 | Blocos de 4; reposição na mesma sequência; análise só de blocos completos (regra provisória, P2) |
| Conclusão | Cronometragem manual imprecisa | Ruído no tempo | Regra fixa de início/fim; segundo integrante confere amostra das gravações |
| Conclusão | Tarefas no teto de 300 s sem tempo real; teto não simulado no poder | Estimativa de tempo enviesada; poder da RQ2 não comprovado | Relatar quantidade e proporção por dispositivo; sensibilidades; regra única antes da coleta (P1, P3) |
| Interna | Aprendizado: 2ª rodada mais rápida | Confunde dispositivo e ordem | 4 sequências; teste de efeito de período (poder baixo) |
| Interna | Portal muda durante a coleta | Condições diferentes entre sessões | Coleta em até 2 semanas; registrar data e hash dos pacotes |
| Interna | Moderador induz o participante | Viés de desempenho | Roteiro idêntico; moderador não ajuda nem decide; pedido de ajuda = não conclusão |
| Interna | RQ4: rótulos não randomizados, passos dependentes, mesma página em dois dispositivos, denominadores distintos, confusão por complexidade | Associação espúria ou mascarada | Rótulo no elemento; indeterminados reportados; análise descritiva sem p-valor; sem causalidade nem generalização |
| Construto | Tarefas sem login não representam o uso completo | Construto reduzido | Declarar o construto como "encontrar e iniciar" o serviço |
| Construto | Nota Lighthouse ≠ acessibilidade real; "sem violação" = "não detectada" | Falsa segurança | Contagem axe e erros de pessoas como principais; Lighthouse complementar |
| Externa | Amostra de estudantes e conhecidos, mais jovem e digital que a população de BH | Generalização limitada | Registrar perfil; não generalizar para idosos ou pessoas com deficiência; recrutar fora da turma |
| Externa | Um aparelho e um navegador | Resultado restrito | Declarar modelo e versão; vale para Android/Chrome em rede estável |
| Externa | Poucos serviços entre 1.118 solicitáveis | Não representa o catálogo | Serviços de alta demanda; não extrapolar |

---

## 11. Impacto para usuários e empresas

**Princípio:** nenhuma economia de tempo ou horas de cidadãos pode ser afirmada sem dados externos e métrica compatível. **Nada foi calculado.**

| Camada | Conteúdo | Situação |
|---|---|---|
| **Impacto relativo mensurável (resultado principal, S03)** | (i) razão das médias geométricas dos tempos (RQ2), com IC; (ii) diferença no nº de tarefas concluídas (RQ1); (iii) diferença de SUS (RQ3) | Planejado; depende da coleta |
| Estimativa secundária | Conversão em horas do cidadão | **Pendente (P5)**. Não se converte a razão das médias geométricas em segundos/horas (o total depende da média aritmética; o teto de 300 s não é tempo real) |
| Dados externos necessários | Solicitações mensais por serviço testado, fração de uso por celular, distribuição de tempos | **Grupo não os possui**; acessos mensais via LAI (P10) |
| Contexto de escala | 496.956 solicitações de 2023; 1.118 serviços online; 92% das demandas via Portal/app (jan–set/2026) | Só contextualiza; **não** serve para calcular horas |
| Limites de generalização | Só os serviços das tarefas testadas, Android/Chrome, rede estável, amostra por conveniência; sem idosos nem pessoas com deficiência; qualquer extrapolação mantém o IC | Obrigatório declarar |

Formato sugerido de entrega final: reunião simulada com o gestor do Portal (sugestão do grupo, não decisão).

---

## 12. Reaproveitamento dos laboratórios anteriores

| Lab | Reaproveitado (planejado) | Novo no LAB05 | Evidência no repositório |
|---|---|---|---|
| Lab01 | Kanban no GitHub Projects | Coleta manual por pessoas, sem API | Nenhuma (link do Projects ainda a preencher, P14) |
| Lab02 | Desenho com tratamentos e participantes; termo de consentimento | Contrabalanceamento intrassujeitos das 4 sequências | Nenhuma (termo não está no repositório) |
| Lab03 | Visão de métricas de operação (DORA) como contexto | Qualidade em uso (ISO/IEC 25010) e WCAG | Nenhuma |
| Lab04 | Escolha do teste, simulação de poder e de erro tipo I, dashboard | Testes pareados (Wilcoxon, t pareado), Holm, impacto relativo | Nenhuma (scripts e dashboard do Lab04 não estão neste repositório) |

A coluna "Reaproveitado" é **intenção declarada**; nada foi verificado como efetivamente reutilizado.

---

## 13. Estado atual do projeto

Legenda: **Verificado** · **Planejado** · **Em andamento** · **Pend. professor** · **Pend. grupo** · **Pend. documental**.

| Item | Situação | Evidência | Próxima ação |
|---|---|---|---|
| Texto da proposta S01 (versão FINAL de 17/11/2026) | Concluído (texto); **não** verificado por terceiros nem aprovado | `docs/proposta/LAB05_S01_Proposta_FINAL.md` | Submeter ao professor |
| Relatório de fechamento da S01 | Concluído (texto) | `docs/relatorios/RELATORIO_FECHAMENTO_LAB05.md` | — |
| PDF da proposta | Declarado no relatório; **ausente do repositório** | Nenhuma (D2) | Localizar/regerar e versionar, ou corrigir o relatório |
| Escolha do software e evidências dos 3 critérios | Planejado/documentado; evidências citadas, não arquivadas | PROPOSTA §1 | Resolver P7 e P9; arquivar capturas |
| Aceite do professor sobre a auditoria (P12) | Pend. professor | Nenhuma | Levar ao professor |
| Validação da regra de fechamento, tempo de abandono, teto (P1, P2, P3) | Pend. professor | Nenhuma | Levar ao professor |
| Ética / comitê (P11) | Pend. professor | Nenhuma | Consultar professor/instituição |
| Termos de uso (P8) | Pend. documental | Nenhuma | Ler e registrar |
| Pedido via LAI (P10) | Enviado em 22/11/2026 (informado pelo grupo) | Nenhuma ainda (sem protocolo/captura) | Arquivar protocolo e captura |
| Tarefas definitivas e conjuntos A/B | Planejado (candidatas) | PROPOSTA §4 | Definir e validar no piloto |
| Planilha de observação, roteiro final, termo de consentimento, formulários SUS/SEQ | Planejado; **inexistentes no repositório** | Nenhuma | Produzir (integrante B) |
| Script `power_analysis.py` e `results_v3_2.json` | Citados; **ausentes do repositório** | Nenhuma (D1) | Versionar no repositório |
| Piloto (3 participantes + auditoria de 3 páginas) | Planejado; **sem evidência de execução** | Nenhuma | Executar e registrar |
| Coleta principal (S02) | Planejado | — | Aguardar P1–P3, P13 |
| Auditoria completa axe/Lighthouse | Planejado; condicionado a P12 | — | Aguardar P12 |
| Análise estatística e notebook | Planejado | — | Após coleta |
| Estimativa de impacto relativo (S03) | Planejado | — | Após análise |
| Conversão em horas | Pend. grupo (P5) | — | Decidir se será feita |
| Teste inferencial na RQ4 | Pend. grupo e professor (P4) | — | Decidir |
| n mínimo (P6) | Pend. grupo | — | Decidir |
| Datas S02/S03/Final e janela de coleta (P13) | Pend. documental | — | Obter do cronograma da disciplina |
| Repositório e GitHub Projects (P14) | Pend. documental | — | Preencher |
| Conferência visual das páginas do PDF não vistas | Pend. (relatório §6) | RELATÓRIO | Conferir |
| Concordância do grupo com RQ4 descritiva e categoria "indeterminado" | Pend. grupo (adotadas "por instrução", sem votação registrada) | RELATÓRIO §6 | Registrar a decisão |

Nenhuma atividade de coleta, auditoria ou análise está marcada como concluída porque **não há artefato** que a comprove.

---

## 14. Registro das pendências P1–P14

Preservadas integralmente da PROPOSTA §10 e do RELATÓRIO §4. **Todas estão abertas em 20/11/2026.**

| ID | Descrição | Tipo | Responsável | Situação | Para encerrar |
|---|---|---|---|---|---|
| P1 | Tratamento do tempo da tarefa abandonada antes de 300 s e da encerrada por pedido de ajuda (RQ2); definir antes da coleta | Professor | Professor | **Aberta** | Resposta documentada do professor; regra registrada no protocolo e aqui |
| P2 | Validação da regra operacional provisória de fechamento dos blocos e da análise só de blocos completos | Professor | Professor | **Aberta** (regra provisória) | Aprovação documentada, ou regra substituta |
| P3 | Critério formal de validade/exclusão por proporção de tarefas no teto de 300 s (nenhum adotado) | Professor | Professor | **Aberta** | Decisão documentada (adotar critério ou confirmar que não haverá) |
| P4 | Teste inferencial na RQ4: critério de adequação dos grupos e denominadores, estatística, unidade de análise, verificação de permutabilidade | Grupo e Professor | Grupo, com validação do professor | **Aberta** (RQ4 hoje descritiva) | Especificação do teste + validação do professor, ou decisão registrada de manter só descritiva |
| P5 | Conversão do impacto em horas (secundária): métrica compatível e dados externos | Grupo | Grupo | **Aberta** | Métrica definida e dados externos com fonte (ou decisão de não converter) |
| P6 | n mínimo abaixo de 32 e como declarar o estudo nesse caso | Grupo | Grupo | **Aberta** | n mínimo e rótulo do estudo decididos e registrados |
| P7 | Como foram obtidos a leitura do HTML da página inicial e o tempo de resposta (HTTP 200 em 0,49 s). A frase do tempo de resposta foi **retirada** do texto | Documental | Grupo | **Encerrada em 20/11/2026** (HTML de https://servicos.pbh.gov.br, 18:57, Chrome 158.0.8127.36, via view-source Cmd+Option+U; trecho sem tokens em `docs/evidencias/capturas/`). Ressalva: o tempo de 0,49 s segue fora do texto | Registro feito: ver `docs/evidencias/S01_criterios_do_software.md` §2 |
| P8 | Leitura dos termos de uso do Portal e registro | Documental | Grupo | **Encerrada em 20/11/2026** (Termos de Uso em `https://servicos.pbh.gov.br/termos-de-uso+5df3bbb5ad0ab2006ceca0ad`, menu "O Portal"; sem menção a acesso automatizado, robôs ou ferramentas de auditoria; Política de Privacidade não lida; leitura feita por assistente no Chrome do coletor, com autorização, a informar ao professor na P12; reler antes da S02) | Registro em `docs/evidencias/S01_criterios_do_software.md` §4.2 |
| P9 | Conferência no navegador do nº de habitantes de BH no IBGE Cidades | Documental | Grupo | **Encerrada em 20/11/2026** (IBGE Cidades mostra 2.315.560 pessoas, Censo 2022; estimativa 2026: 2.415.451; captura em `docs/evidencias/capturas/`; conferência feita por assistente no Chrome do coletor, com autorização) | Registro em `docs/evidencias/S01_criterios_do_software.md` §3 |
| P10 | Envio do pedido via LAI ao canal de transparência da PBH e resposta | Documental | Grupo | **Enviada em 22/11/2026; protocolo a anexar depois** | Protocolo do envio e resposta arquivados |
| P11 | Necessidade de apreciação por comitê de ética | Professor | Professor ou instituição | **Aberta** | Decisão documentada |
| P12 | Validação do uso de axe DevTools e Lighthouse (manuais) frente ao robots.txt e à ética do enunciado | Professor | Professor | **Aberta** | Aceite/recusa documentada; se recusa, auditoria removida |
| P13 | Datas reais de S02, S03 e entrega final; janela de coleta | Documental | Grupo, conforme cronograma da disciplina | **Aberta** | Datas copiadas do cronograma oficial e registradas |
| P14 | Link do repositório e do GitHub Projects; conferência da autoria no cabeçalho | Documental | Grupo | **Aberta** | Links preenchidos; nomes dos integrantes confirmados |

**Não renumerar, agrupar nem remover.** Novas pendências devem receber P15 em diante.

---

## 15. Cronograma e entregas

**Nenhuma data de S02, S03 ou entrega final está confirmada** (P13). O enunciado diz apenas "conforme cronograma da disciplina". Datas conhecidas: proposta original 16/11/2026; versão FINAL e relatório 17/11/2026; impressão do enunciado 20/11/2026.

| Etapa | Esperado (ENUNCIADO) | Planejado no grupo (PROPOSTA §9) | Produzido | Falta |
|---|---|---|---|---|
| **S01** | Proposta com evidências dos 3 critérios, pergunta, caminhos, 1ª versão das 7 categorias, plano de coleta e análise, coleta piloto | Proposta; aceite do professor sobre auditoria; pedido LAI enviado; piloto com 3 participantes | Texto da proposta e relatório de fechamento | Aceite do professor; evidência de LAI; piloto; termo, planilha e instrumentos; resolver P7–P10 |
| **S02** | Coleta completa, dados validados e versionados, análise (descritiva, testes, efeito), ameaças | 32 sessões analisáveis (36–38 agendadas), auditoria completa, dados versionados, testes, ameaças atualizadas | — | Tudo |
| **S03** | Impacto, 7 categorias revisadas e justificadas, conclusões e limitações, rascunho do documento e da apresentação | Estimativa de impacto relativo com fontes; horas só como secundária (P5); categorias revisadas | — | Tudo |
| **Final** | Documento e apresentação de 10 min, formato livre | Documento + apresentação; sugestão: reunião simulada com o gestor do Portal | — | Tudo |

Papéis (sugestão do enunciado, adotada): **A** Planejamento e Método (critérios, LAI, GQM, hipóteses, categorias, ameaças); **B** Instrumentação e Operação (tarefas, roteiro, termo, planilha, sessões, auditoria, validação e anonimização); **C** Análise e Impacto (simulação de poder, notebook, gráficos, efeito, impacto relativo). Nomes: não confirmados.

---

## 16. Estrutura dos artefatos do projeto

**Convenção de pastas** (adotada em 20/11/2026): `docs/enunciado/`, `docs/proposta/`, `docs/relatorios/` para documentos; pastas futuras previstas: `scripts/` (análise e poder), `dados/` (coletas anonimizadas e JSON de auditoria), `instrumentos/` (termo, roteiro, planilha, formulários), `resultados/` (gráficos, dashboard). Só criar a pasta quando houver arquivo.

**Inventário verificado em 20/11/2026** (todo o conteúdo do repositório; `git status` limpo no início da sessão e sem commits listados):

| Caminho | Finalidade |
|---|---|
| `docs/enunciado/ENUNCIADO_LAB05.pdf` | Enunciado oficial (autoridade máxima) |
| `docs/proposta/LAB05_S01_Proposta_FINAL.md` | Proposta metodológica oficial (fonte oficial do planejamento) |
| `docs/relatorios/RELATORIO_FECHAMENTO_LAB05.md` | Auditoria e fechamento da S01 |
| `docs/evidencias/S01_criterios_do_software.md` | Registro de evidências dos 3 critérios (issue #16): matriz, roteiros de P7/P8, confirmação do IBGE, rascunho do pedido LAI |
| `docs/evidencias/P10_pedido_LAI_instrucoes.md` | Instruções e texto pronto do pedido LAI para quem vai enviar (Arthur); tabela de retorno do protocolo |
| `FONTE_DA_VERDADE.md` | Este documento (fica na raiz) |
| `README.md` | Porta de entrada do repositório: resumo, regras, tarefas por pessoa (P10 com Arthur), estrutura |

**Citados nos documentos, mas NÃO presentes no repositório** (não tratar como existentes):

| Artefato citado | Citado em |
|---|---|
| `LAB05_S01_Proposta_FINAL.pdf` | RELATÓRIO §2 |
| `LAB05_S01_Proposta_v2_pre_FINAL.md` | RELATÓRIO §2 |
| `original_S01.txt` | RELATÓRIO §2 |
| `power_analysis.py` (v3.2) | PROPOSTA §4 |
| `results_v3_2.json` | PROPOSTA §4, RELATÓRIO §5 |

**Inexistentes e ainda por produzir:** planilha de observação, termo de consentimento, formulários SUS/SEQ, roteiro final, dicionário de dados, dados coletados, JSON de auditoria, notebook de análise, gráficos/dashboard, documento e apresentação finais.

---

## 17. Regras para os próximos agentes de IA

1. Consultar esta fonte da verdade **antes** de modificar qualquer artefato do LAB05.
2. Consultar o enunciado oficial para verificar requisitos acadêmicos.
3. Não alterar decisões metodológicas sem justificativa e registro (§19).
4. Não inventar resultados, referências, números ou aprovações.
5. Não remover pendências sem evidência de resolução (§14).
6. Preservar a distinção entre planejamento, execução e resultado (§2.3).
7. Atualizar esta fonte quando decisões relevantes forem tomadas.
8. Manter consistência entre proposta, coleta, análise, relatório e apresentação.
9. **Não realizar testes de carga** em sistemas de terceiros; respeitar robots.txt, termos de uso e o limite de 1 requisição/segundo. Não executar crawler, nem automatizar acesso ao Portal sem aceite do professor (P12).
10. Não coletar dados pessoais dos participantes.
11. Não apresentar associação como causalidade (sobretudo RQ4).
12. Não generalizar além do desenho: serviços testados, Android/Chrome, amostra por conveniência.

Regras adicionais derivadas deste documento:

13. Citar poder estatístico sempre com suas limitações (§6.5) e nunca como resultado.
14. Não escrever nomes de integrantes, datas de S02/S03/final, número de acessos ao Portal ou horas economizadas sem fonte.
15. Não descrever a regra de fechamento, o teto de 300 s ou a RQ4 descritiva como aprovados pelo professor.
16. Não modificar a PROPOSTA e o RELATÓRIO como efeito colateral de outra tarefa; correções entram com registro na §19.

---

## 18. Divergências e inconsistências encontradas

| ID | Descrição | Fontes | Tratamento |
|---|---|---|---|
| D1 | A proposta e o relatório afirmam que o poder foi conferido em `results_v3_2.json` (gerado por `power_analysis.py` v3.2), mas **nenhum dos dois arquivos está no repositório**. Os 9 valores de poder são, neste repositório, **não reproduzíveis nem verificáveis** | PROPOSTA §4, RELATÓRIO §5 vs. repositório | Manter os valores como "conforme citado"; versionar script e JSON antes de usar na S02/S03 |
| D2 | O relatório lista `LAB05_S01_Proposta_FINAL.pdf`, `..._v2_pre_FINAL.md` e `original_S01.txt` como produzidos/preservados; nenhum está no repositório | RELATÓRIO §2 vs. repositório | Localizar e versionar, ou corrigir o relatório (com registro) |
| D3 | O enunciado limita medições de fora a **no máximo 1 requisição por segundo**. A proposta cita robots.txt e termos de uso, mas **não menciona o limite**. O Lighthouse recarrega a página em cada execução (12–20 páginas × 3 execuções × 2 modos, ou seja, até cerca de 120 carregamentos), e o enunciado exige respeito ao robots.txt (`Disallow: /`) | ENUNCIADO §2 vs. PROPOSTA §6 | Incluir o limite explícito de 1 req/s no protocolo de auditoria e levar a P12 ao professor. Não alterar a proposta sem registro |
| D4 | O enunciado pede "coleta piloto" na S01; a proposta a prevê, mas não há evidência de execução, e o relatório de fechamento não menciona o piloto como feito | ENUNCIADO §7, PROPOSTA §9, RELATÓRIO | Tratar como **não executado** até haver artefato |
| D5 | O relatório declara o texto "sem contradições internas relevantes" e a decisão de RQ4 descritiva/"indeterminado" foi adotada "por instrução, não por votação registrada" | RELATÓRIO §1, §6 | Registrar a concordância do grupo |
| D6 | O relatório diz que a proposta foi "finalizada com pendências externas" e "metodologicamente coerente" — é uma autoavaliação; não existe revisão independente nem do professor | RELATÓRIO §1 | Não citar como validação externa |
| D7 | A proposta (§9) lista o S01 como incluindo "aceite do professor sobre a auditoria" e "pedido LAI enviado" — nenhuma das duas é comprovada | PROPOSTA §9 | Tratar como planejadas |
| D8 | Autoria: cabeçalho traz apenas "@Someone"; enunciado exige papéis A/B/C (sugestão) sem nomes | PROPOSTA | P14 |
| D9 | A lista de fontes da proposta cita o título "amplia em mais de 500 serviços digitais"; o título real da notícia de 05/10/2026 é "... em mais de 500% serviços digitais". Além disso, os números de serviços variam por data (05/10/2026: 1.492/1.118; 18/08/2026: 1.489/903; 27/12/2023: 1.387/936) | PROPOSTA vs. fonte conferida em 20/11/2026 | **Título corrigido na proposta em 22/11/2026**; citar sempre com a data da fonte |

Não foi encontrada divergência de conteúdo entre a proposta e o relatório quanto a RQs, pendências, tamanhos de amostra ou valores de poder (conferidos nesta consolidação).

---

## 19. Histórico desta fonte

| Versão | Data | Alteração |
|---|---|---|
| 1.0 | 20/11/2026 | Criação, a partir de ENUNCIADO, PROPOSTA (rev. 17/11/2026) e RELATÓRIO (17/11/2026). Nenhum artefato foi alterado |
| 1.1 | 20/11/2026 | Reorganização em `docs/`; PDF do enunciado renomeado de `05 - Experimento Final ... 2026_2.pdf` para `ENUNCIADO_LAB05.pdf`; links e §16 atualizados. Conteúdo dos documentos movidos não foi alterado |
| 1.2 | 20/11/2026 | Issue #16: criado `docs/evidencias/S01_criterios_do_software.md`; nota na P9. Nenhuma pendência encerrada |
| 1.3 | 20/11/2026 | P7: HTML da página inicial registrado (trecho sem tokens). P7 segue aberta até confirmação do método |
| 1.4 | 20/11/2026 | P7 encerrada (método confirmado pelo coletor) |
| 1.5 | 20/11/2026 | P8: busca na web feita; nenhum termo específico do Portal localizado; leitura manual pendente. P8 segue aberta |
| 1.6 | 20/11/2026 | P8: captura do rodapé arquivada (sem link de termos na parte visível); menus ainda por conferir. P8 segue aberta |
| 1.7 | 20/11/2026 | P8 encerrada: Termos de Uso lidos no Portal (menu "O Portal"). Registrado que a leitura foi conduzida por ferramenta com autorização do coletor |
| 1.8 | 20/11/2026 | P9 encerrada: número do IBGE conferido no navegador |
| 1.9 | 20/11/2026 | P10: criado `docs/evidencias/P10_pedido_LAI_instrucoes.md` para o envio por Arthur. P10 segue aberta até haver protocolo |
| 2.0 | 20/11/2026 | Criado `README.md` com tarefas e responsáveis (P10: Arthur) |
| 2.1 | 20/11/2026 | Fontes do software conferidas no navegador (5 páginas); D9 registrada; evidências arquivadas |
| 2.2 | 22/11/2026 | P10: envio do LAI informado pelo grupo em 22/11/2026; protocolo e captura pendentes. Versão observada dos pacotes registrada (S01_criterios §2.1). Correção do título da D9 na proposta |
