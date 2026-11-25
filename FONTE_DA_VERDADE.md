# FONTE DA VERDADE — LAB05

**Versão 3.3 · criada em 20/11/2026, atualizada em 25/11/2026** · Referência central e permanente do projeto LAB05.
Qualquer pessoa ou agente de IA deve ler este arquivo antes de tocar em qualquer artefato do LAB05.

> Convenção de leitura: este documento separa **exigido** (enunciado), **decidido** (professor), **planejado**, **executado** (artefato no repositório) e **resultado** (dado observado). **Mudança de direção (v3.0, 24/11/2026):** o projeto deixou de ser um experimento com participantes e passou a analisar **dados abertos reais de operação** da PBH. Os resultados do pipeline estão em `resultados/` e são gerados pelo código; nenhum número deste documento é digitado à mão sem apontar a fonte. A metodologia anterior está arquivada em [docs/arquivo/](./docs/arquivo/s01-metodologia-participantes/README.md) e **não vale mais**.

Fontes consultadas:

| Sigla | Arquivo | Papel |
|---|---|---|
| ENUNCIADO | [docs/enunciado/ENUNCIADO_LAB05.pdf](./docs/enunciado/ENUNCIADO_LAB05.pdf) | Requisitos do professor (impressão do Canvas em 20/11/2026) |
| METODOLOGIA | [docs/metodologia.md](./docs/metodologia.md) | Metodologia vigente (v3.0) |
| DICIONÁRIO | [dados/dicionario_de_dados.md](./dados/dicionario_de_dados.md) | Fonte dos dados, colunas, classificação, limitações |
| ARQUIVO | [docs/arquivo/](./docs/arquivo/s01-metodologia-participantes/) | Proposta e relatório S01 (histórico, descontinuados) |

---

## 1. Identificação do projeto

| Campo | Valor | Fonte |
|---|---|---|
| Laboratório | Laboratório 05 — Experimento em Software Real (LAB05), 20 pontos | ENUNCIADO |
| Curso / disciplina | Engenharia de Software — Laboratório de Experimentação de Software, 6º período, noite, Campus Lourdes (PUC Minas), 2026/2 | ENUNCIADO |
| Professor | Danilo Maia | ENUNCIADO |
| Software / objeto | Ecossistema de atendimento ao cidadão da Prefeitura de Belo Horizonte (PBH): Portal de Serviços (SYDLE ONE), PBH APP, Central 156 e atendimento presencial (BH Resolve) | METODOLOGIA |
| Estudo | Análise observacional retrospectiva de dados abertos de operação (CKAN da PBH, CC-BY), mai/2020 a jul/2023 | METODOLOGIA |
| Integrantes | **Não confirmados** (primeiros nomes: Marcos, Guilherme, Arthur); P14 | — |
| Sprint atual | S01 entregue com o desenho antigo; reorientação em 24/11/2026 (P15 pendente com o professor) | §19 |
| Link repositório / GitHub Projects | Repositório `Laboratorio-Medicao/Lab05`; link do Projects a preencher (P14) | — |

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

O objeto continua sendo o ecossistema de atendimento da PBH, agora observado pelos **resultados das solicitações** registradas no BH Digital, e não pela interação de participantes.

### 4.1 Os três critérios do enunciado (§2a)

Evidências em [docs/evidencias/S01_criterios_do_software.md](./docs/evidencias/S01_criterios_do_software.md) (ainda válidas): Portal sobre SYDLE ONE (real); Portal no ar desde maio/2020 (em operação); 1.492 serviços catalogados e 92% das demandas jan–set/2026 via Portal ou app, 496.956 solicitações jan–out/2023, BH com 2.315.560 habitantes (alto impacto; cada número com fonte e data no arquivo de evidências). Em adição, o próprio conjunto de dados mostra a escala: **1.480.736 solicitações únicas** entre 11/05/2020 e 31/07/2023 (`dados/qualidade_dados.json`).

### 4.2 Fonte dos dados (confirmada na API em 24/11/2026)

Resumo; detalhes no [DICIONÁRIO](./dados/dicionario_de_dados.md).

- Dataset CKAN "Solicitações dos cidadãos, por meio dos canais de atendimento da PBH", licença **CC-BY**, 10 CSVs de dados + dicionário PDF (atualizado em 25/07/2023).
- **Cobertura real: mai/2020 a jul/2023.** Não há 2024, 2025 nem 2026 (o pedido inicial supunha cobertura até 2026; foi **desmentido pela fonte**). O `metadata_modified` (10/06/2026) não corresponde a novos dados.
- Outro dataset do mesmo CKAN, "Solicitações de Serviço e Incidentes", vai até 2026, mas é de **chamados de TI (Prodabel)**, sem canal: descartado.
- Acesso automatizado: API do CKAN; o servidor bloqueia o user-agent padrão (HTTP 403) e aceita um identificado. O pipeline se identifica e respeita 1 req/s (enunciado §2).
- Colunas de endereço e localização (logradouro, número, bairro, regional, coordenadas) existem na fonte; **são descartadas na leitura** e nunca persistidas.

### 4.3 Limitações da fonte

Ver DICIONÁRIO §6: cobertura até jul/2023; canais "Integração entre Sistemas" e "Origem Interna" e as "situações" não documentados; travessão perdido ("?") na origem; resolução de dia; sem id do cidadão; corte de observação inferido. O robots.txt do Portal **não se aplica** ao CKAN e deixou de ser relevante: o pipeline não acessa o Portal.

---

## 5. Perguntas de pesquisa e GQM

**Principal:** para um mesmo serviço, existem diferenças no tempo de encerramento e na proporção de solicitações encerradas conforme o canal de atendimento?

| GQM | Pergunta | Métricas |
|---|---|---|
| Q1 | Quais canais têm menor tempo mediano de encerramento? | Mediana, Q1–Q3, P90 (dias); mediana de Kaplan–Meier |
| Q2 | A proporção de solicitações encerradas difere entre canais? | % encerrada em ≤ 90 dias e até o corte |
| Q3 | As diferenças permanecem dentro do mesmo serviço? | OR de Mantel–Haenszel; delta de Cliff combinado; I²; nº de serviços em cada sentido |
| Q4 | Quais serviços apresentam maior diferença entre canais? | Maior \|delta\| e maior \|dif. de risco\| por serviço |

Entidades e atributos: entidade = solicitação (processo/recurso de atendimento); atributos externos, medidas diretas (datas) e derivadas (tempo, taxa). Escalas e estatísticas permitidas: METODOLOGIA §4. Armadilha de medição (Goodhart/McNamara): "encerrada" pode ser encerramento administrativo; uma taxa alta não prova que o problema foi resolvido.

## 6. Definições e desenho da análise (fixadas antes de olhar os resultados)

Detalhe completo na [METODOLOGIA §6](./docs/metodologia.md) e no cabeçalho de `scripts/estatistica.py`. Pontos que não se pode mudar sem registro:

1. **Estados:** encerrada / aberta / inconsistente. **Aberta nunca recebe tempo 0.**
2. **Elegível:** não inconsistente, canal comparável (Portal, PBH APP, Telefone 156, Presencial), seguimento ≥ **90 dias** (coorte madura; decisão do grupo, **P16**).
3. **Tempo:** dias entre criação e encerramento, só de encerradas. **Taxa:** % encerrada em ≤ 90 dias (medida de proporção testada) e até o corte (descritiva).
4. **Mesmo serviço:** estratificação por serviço; célula serviço × canal precisa de ≥ 30 registros (**P16**).
5. **Testes:** qui-quadrado/Fisher, Mann–Whitney, Kruskal–Wallis, CMH, van Elteren, teste dos sinais; efeitos (diferença de risco, OR, h, delta de Cliff, ε², V); Holm por família; sensibilidade em 30 e 180 dias.
6. Com n ≥ 10⁵ o p-valor é quase sempre minúsculo: **interpretar por tamanho de efeito e consistência entre serviços**.

## 7. Sete categorias da pesquisa

Ver [METODOLOGIA §7](./docs/metodologia.md): aplicada; descritiva e exploratória (comparativa); quantitativa; análise documental de dados secundários (observacional retrospectivo); longitudinal retrospectivo; sem controle experimental (ajuste estatístico por serviço); evidência observacional (associação, não causa). **Preliminar**, a revisar na S03.

## 8. Coleta e tratamento (implementados)

`python scripts/pipeline.py`: coleta → tratamento → análise → gráficos. Passos e módulos no README e no DICIONÁRIO. Garantias verificadas por testes (`tests/`): colunas de endereço não chegam à memória, à base nem a nenhuma saída; ids pseudonimizados; datas nos dois formatos; duplicatas por Id; abertas sem tempo; recusa de pasta de CSV bruto dentro do repositório; user-agent identificado e intervalo ≥ 1 s. Execução real de 24/11/2026: ver §13.

## 9. Plano de análise e resultados

A análise é executada pelo código; os números vêm de `resultados/resumo.md`, `resultados/tabelas/` e `resultados/painel.html`. **Esta fonte não repete os números** para não divergirem do que o pipeline produz. A interpretação (S02, issue #25) está em [docs/interpretacao_resultados.md](./docs/interpretacao_resultados.md), versão 1.0 de 24/11/2026, **ainda sem revisão do grupo**. Conclusões:

- A maior parte da diferença global entre canais vem do **tipo de serviço** que cada canal atende. Dentro do mesmo serviço, o efeito típico é cerca de 10 vezes menor (interpretação §3.1).
- O Presencial parece encerrar muito menos, mas 88,7% de suas solicitações elegíveis são recurso à JARI, que permanece "em andamento". O OR de Mantel–Haenszel nos pares com Presencial é **dominado por esse serviço**; a mediana da diferença de risco por serviço fica perto de zero.
- O delta combinado de tempo nos pares com Presencial é **dominado pelo Tapa-Buraco** (peso n_A × n_B) e inverte de sinal com outra ponderação ou com a mediana por serviço: **resultado inconclusivo**, que não deve ser apresentado como achado (D14).
- Telefone 156: mais lento em ~3/4 dos serviços em comum (consistente), com magnitude **desprezível**; sem sentido consistente na proporção encerrada.
- Portal × PBH APP: o APP encerra um pouco mais e um pouco mais rápido de forma consistente, com magnitude desprezível. É o resultado mais robusto.
- Todas as afirmações são associação em dados observacionais.

## 10. Ameaças à validade

Ver [METODOLOGIA §8](./docs/metodologia.md) (conclusão, interna, construto, externa, com mitigação). Principais: confusão residual por perfil da demanda; encerramento administrativo ≠ resolução; censura à direita; independência não verificável; cobertura só até jul/2023; poucos serviços em comum entre alguns canais.

## 11. Impacto

**Nada foi calculado.** Princípio: nenhuma economia de tempo ou horas pode ser afirmada sem métrica compatível e fonte. Possível estimativa (S03): volume anual de solicitações por canal (da própria base) × diferença relativa de tempo, **apenas** para os serviços e canais com comparação válida, sempre com IC e com a ressalva de associação. Conversão em horas do cidadão: **P5** (pendente). Limites de generalização: BH, 2020–2023, serviços com ≥ 2 canais comparáveis.

## 12. Reaproveitamento dos laboratórios anteriores

| Lab | Conceito reaproveitado | Novo no LAB05 | Evidência |
|---|---|---|---|
| Lab01 | Coleta automatizada de dados via API | Cliente da API do CKAN com limite de 1 req/s | `scripts/coleta.py` (**conceito**; o código do Lab01 não está neste repositório) |
| Lab02 | Desenho de experimento | Substituído: estudo observacional, sem participantes | — |
| Lab03 | Métricas de operação (tempo até encerramento ≈ lead time/MTTR) | Aplicadas a solicitações de atendimento | `scripts/estatistica.py` (conceito) |
| Lab04 | Escolha do teste de hipótese, tamanho de efeito, dashboard | Testes não paramétricos e estratificados; painel HTML | `scripts/estatistica.py`, `scripts/visualizacao.py` (conceito; o código do Lab04 não está aqui). Simulação de poder/erro tipo I **não se aplica** (dados populacionais, n enorme) |

## 13. Estado atual do projeto

| Item | Situação | Evidência | Próxima ação |
|---|---|---|---|
| Reorientação para dados abertos | **Executado** (código, docs, testes); **não aprovado pelo professor** (P15) | `scripts/`, `docs/metodologia.md` | Levar ao professor |
| Validação da fonte | **Executado** em 24/11/2026 (cobertura, colunas, licença, API) | DICIONÁRIO §1 | Confirmar com a PBH se há dados > jul/2023 (P17) |
| Pipeline (coleta, tratamento, análise, gráficos) | **Verificado** em 25/11/2026 (reexecução do zero com download real, por agente de IA a pedido do Arthur; reproduzido com ressalvas): 10 CSVs e base com os mesmos SHA-256, 1.480.736 registros | `docs/evidencias/verificacao_pipeline.md`, `resultados/`, `dados/manifesto_coleta.json`, `dados/qualidade_dados.json` | Reexecução por um integrante (opcional, reforça a verificação, §2.3) |
| Testes automatizados | **57 testes passando** (dados sintéticos), 25/11/2026 | `tests/` | Rodar `python -m pytest` |
| Interpretação dos resultados | **Executado** (v1.0, 24/11/2026; sem revisão do grupo) | `docs/interpretacao_resultados.md` (issue #25) | Revisão por outro integrante; decidir D14 |
| Impacto, relatório | **Pendente** | — | #29 (impacto), #31 (documento final) |
| Revisão das 7 categorias (S03) | Pendente | METODOLOGIA §7 | S03 |
| Documento e apresentação (10 min) | Pendente | — | Entrega final |

"Verificado" (§2.3) exige conferência por segunda pessoa ou ferramenta, com registro: o pipeline foi reexecutado do zero em 25/11/2026 por um agente de IA (Claude Sonnet), a pedido do Arthur, e não por um integrante do grupo; ver `docs/evidencias/verificacao_pipeline.md`.

---

## 14. Registro das pendências

Preservadas as P1–P14 originais. **Não renumerar, agrupar nem remover.** Novas a partir da P15.

| ID | Descrição | Situação em 24/11/2026 |
|---|---|---|
| P1 | Tempo da tarefa abandonada antes de 300 s / pedido de ajuda (RQ2) | **Obsoleta** (metodologia anterior; sem tarefas com participantes) |
| P2 | Regra provisória de fechamento dos blocos | **Obsoleta** (idem) |
| P3 | Critério de exclusão por proporção de tarefas no teto de 300 s | **Obsoleta** (idem) |
| P4 | Teste inferencial da RQ4 (violações WCAG × erros) | **Obsoleta** (RQ4 descontinuada) |
| P5 | Conversão do impacto em horas | **Aberta** (grupo) |
| P6 | n mínimo abaixo de 32 | **Obsoleta** (não há amostra de participantes; hoje o critério é o mínimo por célula, P16) |
| P7 | Como foi obtido o HTML da página inicial | **Encerrada em 20/11/2026** (evidência em `docs/evidencias/`) |
| P8 | Leitura dos termos de uso do Portal | **Encerrada em 20/11/2026**. O pipeline atual não acessa o Portal |
| P9 | Habitantes de BH (IBGE) | **Encerrada em 20/11/2026** (2.315.560, Censo 2022) |
| P10 | Pedido via LAI (acessos ao Portal) | Enviado em 22/11/2026; protocolo a anexar. **Opcional** na nova metodologia (só contexto de impacto) |
| P11 | Comitê de ética | **Obsoleta** como pendência de participantes (sem participantes nem dados pessoais; colunas de endereço descartadas). Se o professor exigir manifestação, registrar aqui |
| P12 | Aceite de axe DevTools e Lighthouse frente ao robots.txt | **Obsoleta** (auditoria removida do escopo; arquivos em `docs/arquivo/`) |
| P13 | Datas de S02, S03 e entrega final | **Aberta** |
| P14 | Link do repositório/Projects; autoria | **Aberta** |
| **P15** | **Professor aprovar a mudança de metodologia** (dados abertos de operação no lugar de experimento com participantes). Não há registro de aprovação | **Aberta** (professor) |
| **P16** | **Professor validar decisões de desenho:** coorte madura de 90 dias, mínimo de 30 por célula, estratificação por serviço, não interpretar "situações" | **Aberta** (professor) |
| **P17** | Confirmar com a PBH (SUMOG) se existem dados posteriores a jul/2023, a data de extração dos CSVs e o significado de "Integração entre Sistemas", "Origem Interna" e das situações | **Aberta** (grupo) |

---

## 15. Cronograma e entregas

Nenhuma data de S02, S03 ou entrega final está confirmada (P13). Mapa do enunciado para o trabalho atual:

| Etapa | Esperado (ENUNCIADO) | Situação |
|---|---|---|
| S01 | Proposta, pergunta, caminhos, 1ª versão das 7 categorias, plano, coleta piloto | Entregue com o desenho antigo; a nova coleta (completa) já roda |
| S02 | Coleta completa, dados validados e versionados, análise (descritiva, testes, efeito), ameaças | **Código pronto e executado**; falta interpretar e conferir por segunda pessoa |
| S03 | Impacto, 7 categorias revisadas, conclusões e limitações, rascunhos | Pendente |
| Final | Documento e apresentação de 10 min | Pendente |

Papéis (sugestão do enunciado): A Planejamento e Método; B Instrumentação e Operação (`coleta`/`tratamento`); C Análise e Impacto (`estatistica`/`visualizacao`). Nomes não confirmados.

---

## 16. Estrutura dos artefatos

| Caminho | Finalidade |
|---|---|
| `README.md` | Entrada: como reproduzir, estrutura, regras, pendências |
| `FONTE_DA_VERDADE.md` | Este documento |
| `docs/metodologia.md` | Metodologia vigente (v3.0) |
| `docs/interpretacao_resultados.md` | Interpretação dos resultados (Q1–Q4, sensibilidade, limites), issue #25 |
| `docs/enunciado/` | Enunciado oficial (autoridade máxima) |
| `docs/evidencias/` | Critérios do software (S01) e instruções do pedido LAI |
| `docs/arquivo/s01-metodologia-participantes/` | Proposta, relatório e auditoria Lighthouse da metodologia **descontinuada** |
| `dados/dicionario_de_dados.md` | Fonte, colunas, classificação, limitações |
| `dados/manifesto_coleta.json`, `dados/qualidade_dados.json` | Saídas versionadas da coleta e do tratamento |
| `dados/processados/` | Base analítica anonimizada (**ignorada pelo git**, regenerável) |
| `scripts/` | `config`, `coleta`, `tratamento`, `estatistica`, `visualizacao`, `pipeline` |
| `tests/` | pytest com dados sintéticos (`tests/sintetico.py`) |
| `resultados/` | Resumo, tabelas, figuras, painel e JSON gerados pelo pipeline com dados reais |
| `.gitignore`, `.gitattributes` | Ignoram `.venv`, base processada e `dados/brutos/`; sem conversão de fim de linha em `dados/` |

**Removidos em 24/11/2026** (histórico no git, último commit com eles `bb06c60`): `docs/sessao/*` (roteiro, tarefas A/B, termo de consentimento, relatório do piloto), `dados/sinteticos/*`, dicionário antigo, `scripts/{analise,esquema,gerar_dados_sinteticos,validar_dados,power_analysis}.py`, `tests/test_{analise,validar_dados,power_analysis}.py`, `notebooks/analise_S02.py`, `resultados/results_v4.json`. Justificativa: dependiam de participantes, de SUS/SEQ, de tempo de tarefa humana ou de comparação celular × computador.

---

## 17. Regras para os próximos agentes de IA

1. Consultar esta fonte e o enunciado antes de modificar qualquer artefato.
2. Não alterar decisões metodológicas sem justificativa e registro (§19).
3. Não inventar resultados, referências, números, colunas ou significados que a PBH não documentou.
4. Não remover pendências sem evidência (§14); pendência obsoleta é marcada, não apagada.
5. Manter a distinção entre planejado, executado e resultado (§2.3).
6. **Nunca** versionar CSV bruto da PBH nem colunas de endereço/coordenadas; a base processada fica fora do git.
7. Respeitar 1 requisição por segundo e identificar o acesso. Não fazer teste de carga em sistema de terceiros. Não acessar o Portal de Serviços de forma automatizada.
8. Não apresentar associação como causa; não tratar "encerrada" como "resolvida"; não tratar mudança de metodologia como aprovada pelo professor.
9. Não generalizar além de BH, mai/2020–jul/2023 e dos serviços com ≥ 2 canais comparáveis.
10. Não escrever nomes completos, datas de S02/S03/final ou horas economizadas sem fonte.
11. Toda mudança em horizonte, mínimo por célula, definições ou testes: registrar na §19 no mesmo commit.

---

## 18. Divergências e inconsistências

| ID | Descrição | Tratamento |
|---|---|---|
| D1 | Poder simulado v3.2 ausente do repositório; reconstrução v4 divergente | **Encerrada por descontinuação** (24/11/2026): simulação de poder sem sentido na nova metodologia; arquivos removidos (histórico no git) |
| D2 | PDF da proposta, v2_pre_FINAL e original_S01 citados no relatório, ausentes | Mantida como registro histórico (relatório arquivado) |
| D3 | Limite de 1 req/s do enunciado ausente da proposta antiga | **Encerrada**: o novo pipeline implementa e testa o limite |
| D4, D5, D6, D7, D8, D9 | Piloto não executado; RQ4; autoavaliação do relatório; aceite não comprovado; autoria; títulos de notícias | Mantidas como histórico da proposta antiga; D8 (autoria) segue em P14; D9 segue válida para as citações do arquivo de evidências |
| D10 | Notebook `.py` percent e Holm à mão por falta de statsmodels | **Superada**: notebook removido; Holm e demais testes seguem implementados à mão/scipy em `scripts/estatistica.py`, conferidos por testes |
| D11 | O pedido inicial supunha dados de 2024, 2025 e 2026; a fonte termina em **jul/2023** | **Resolvida pela fonte**: escopo ajustado; P17 pergunta à PBH se há dados novos |
| D12 | Auditoria Lighthouse de 24/11/2026 gerada antes do aceite do professor (P12) | Arquivada, fora da análise |
| D13 | `metadata_modified` do dataset (10/06/2026) não corresponde à data dos arquivos (jul/ago 2023) | Registrada; não indica dados novos |
| D14 | O delta de Cliff combinado (`estratificado_por_par`) pondera cada serviço por n_A × n_B (encerradas). Nos pares com Presencial, o Tapa-Buraco (217 encerradas presenciais) recebe 44% a 68% do peso e define o sinal; com peso n_A·n_B/(n_A+n_B) ou pela mediana por serviço o sinal se inverte | **Aberta** (grupo): pipeline **não alterado**, porque o peso foi fixado antes dos resultados. Resultado tratado como inconclusivo em `docs/interpretacao_resultados.md` §4; decidir se a ponderação alternativa entra como sensibilidade (registrar na §19) |

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
| 2.3 | 22/11/2026 | Issue #17: RQ4 explicitada como hipótese de trabalho sem teste; gatilhos de reclassificação das 7 categorias; cabeçalho da proposta sem "@Someone" (primeiros nomes da issue #15) |
| 2.4 | 22/11/2026 | RQ4 passa a ter teste exploratório proposto (participante como unidade, Wilcoxon pareado, permutação de sinais como sensibilidade), a validar no P4; reverte a nota de 2.3 de "sem teste" |
| 2.5 | 23/11/2026 | Issue #20: reconstrução da simulação de poder **v4** (`scripts/power_analysis.py`, `tests/test_power_analysis.py`, `resultados/results_v4.json`, `requirements.txt`; `.gitignore` com `.claude/worktrees/`). Nova §6.5.1 com regra de calibração, tabela citado × reproduzido e erro tipo I (n = 24, 28, 32); D1 atualizada (segue aberta para o v3.2; 7 de 9 valores de poder e o FWER de n = 28 fora de 3 EP_MC); §9, §13 e §16 atualizadas; cabeçalho corrigido para a versão atual. Proposta e relatório não foram alterados |
| 2.6 | 23/11/2026 | Issue #25: dicionário de dados (proposta, a confirmar com o papel B), validador, análise, gerador de dados sintéticos, notebook `.py` percent, testes e `requirements.txt`. Tudo rodado **só com dados sintéticos**: **nenhum resultado**. P1 e P2 entram como parâmetros (opção provisória marcada PENDENTE, demais variantes como sensibilidade); teste da RQ4 desligável (P4). D10 registrada. Nenhuma pendência encerrada. Merge com a 2.5 (issue #20): `resultados/` passa a abrigar estimativas de simulação e saídas reais, nunca sintéticas; `requirements.txt` unificado |
| 3.0 | 24/11/2026 | **Mudança de metodologia** (registro obrigatório): o experimento com participantes (celular × computador, SUS/SEQ, sessões, auditoria Lighthouse) é substituído por análise de **dados abertos de operação** da PBH por canal de atendimento. Motivo: a coleta com participantes exige recrutamento e sessões em número inviável para o grupo. Nova pergunta: para um mesmo serviço, tempo e taxa de encerramento diferem por canal? Validada a fonte (CKAN, CC-BY): **cobertura mai/2020–jul/2023, sem 2024–2026** (D11). Implementados pipeline (`scripts/`), testes (55), dicionário, metodologia e resultados reais. Material antigo arquivado em `docs/arquivo/` ou removido (§16). P1–P4, P6, P11, P12 marcadas obsoletas; novas P15 (professor aprovar a mudança), P16 (validar decisões de desenho), P17 (consultar a PBH). D1, D3, D10 encerradas/superadas; D11–D13 abertas. **Nenhuma aprovação do professor foi registrada** |
| 3.1 | 24/11/2026 | Issue #25 (reescrita para a metodologia v3.0): criado `docs/interpretacao_resultados.md` com a resposta a Q1–Q4, sensibilidade e limites; §9 e §13 atualizadas. Registrada a D14 (dominância do Tapa-Buraco no delta combinado dos pares com Presencial). Pipeline, parâmetros e resultados **não** foram alterados. Nenhuma pendência encerrada. Issue #22 (32 sessões) fechada como obsoleta |
| 3.3 | 25/11/2026 | Issue #38: verificação do pipeline por reexecução do zero (venv novo, download real do CKAN, 57 testes), feita por um agente de IA a pedido do Arthur. CSVs e base com os mesmos SHA-256; diferenças só no manifesto (origem do download), fim de linha, a última casa decimal de 41 números de `resultados.json` e os bytes da figura 04 (renderização do matplotlib). Achados corrigidos: intervalo de 1 req/s (a resolução de 15,625 ms de `time.monotonic()` no Python 3.12/Windows deixava o intervalo real até ~16 ms abaixo do pedido; corrigido com relógio `perf_counter` e laço de reconferência, com teste novo) em `scripts/coleta.py` e testes portáveis (`encoding="utf-8"`); linha para Windows no README. Registrado em `docs/evidencias/verificacao_pipeline.md`; §13 atualizada. Pipeline, parâmetros e resultados **não** foram alterados. Nenhuma pendência encerrada |
