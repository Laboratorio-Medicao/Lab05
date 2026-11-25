# Estimativa de impacto — LAB05 (issue #29)

**Versão 1.0 · 25/11/2026** · Papel C (Análise e Impacto) · Metodologia v3.0

> Estudo **observacional**: tudo aqui é **associação, não causa**. O que se estima é um **contrafactual hipotético** ("se os pedidos do canal B tivessem o desempenho do canal A no mesmo serviço"), não o efeito de mudar de canal.
> Nenhum número foi digitado à mão sem fonte: cada um aponta para um arquivo em `resultados/tabelas/`, gerado por `python scripts/pipeline.py` com os dados reais (execução de 25/11/2026). Código: `scripts/impacto.py`.
> A mudança de metodologia e as decisões de desenho (90 dias, ≥ 30 por célula, estratificação por serviço) **ainda não foram aprovadas pelo professor** (P15, P16). Sem revisão do grupo.

## 1. A pergunta (enunciado §5)

O enunciado pede que o resultado seja traduzido para quem usa o atendimento da PBH. A pergunta aqui é: **quanto tempo de espera, por ano, está associado à diferença de desempenho entre canais, quando se compara o mesmo serviço?**

A resposta honesta é curta: nos pares com conclusão sustentada, a diferença **por pedido** é pequena (poucos dias na mediana), e os totais anuais só parecem grandes porque são multiplicados por um volume de dezenas a centenas de milhares de pedidos por ano. Esses totais são uma **escala de grandeza**, não uma economia que alguém vá obter.

## 2. Volume anual por canal

Fonte: `resultados/tabelas/volume_anual_por_canal.csv` (solicitações **elegíveis**: coorte madura, canais comparáveis, sem registros inconsistentes; `meses_cobertos` = meses com criação naquele ano e canal).

| Ano | Portal de Serviços | PBH APP | Telefone 156 | Presencial | Meses cobertos |
|---|---:|---:|---:|---:|---|
| 2020 | 42.538 | 17.917 | 13.537 | 12 | Portal e APP: 8; 156: 7; Presencial: 3 (**parcial**) |
| 2021 | 166.562 | 104.478 | 41.060 | 21.641 | 12 |
| 2022 | 230.079 | 152.793 | 43.467 | 21.326 | 12 |
| 2023 | 110.395 | 54.014 | 16.029 | 7.078 | 4 (**parcial**) |

- Só 2021 e 2022 são anos completos. 2020 e 2023 são parciais: **não comparar** com os anos cheios.
- O volume usado nas estimativas **não** é o de um ano específico: é o número de solicitações elegíveis do serviço dividido pela duração da coorte, de 2020-05-11 a 2023-04-26, ou 2,96 anos (`resultados.json`, `coorte`). Isso trata cada ano como igual, o que não vale (o volume cresceu de 2020 a 2022).
- A coorte termina em abril/2023 e não em jul/2023 porque só entram solicitações com ao menos 90 dias de seguimento.

## 3. Impacto por par de canais

Fonte: `resultados/tabelas/impacto_por_par.csv`. IC de 95% por bootstrap percentil (2.000 reamostras de **serviços**, com reposição; semente fixa). Só entram os serviços com célula válida (≥ 30 registros) nos dois canais.

Convenção: A = primeiro canal do par; B = segundo. O impacto é calculado sobre os pedidos de B. A "diferença de mediana ponderada" é Σ (volume de B × diferença de mediana) / Σ volume de B, com a diferença de mediana = mediana de B − mediana de A em cada serviço, e só entram os serviços com as duas medianas.

| Par (A × B) | Serviços | Pedidos de B por ano | Diferença de mediana ponderada (dias) | Dias de espera por ano (B − A) | Encerradas em ≤ 90 d a mais por ano |
|---|---:|---:|---:|---:|---:|
| Portal × PBH APP | 159 | 110.551 | −1,69 [−3,37; −0,32] | −186.607 [−421.157; −25.214] | −760 [−1.647; −8] |
| Portal × Telefone 156 | 45 | 38.470 | +2,31 [0,84; 4,50] | +88.973 [34.911; 158.072] | +348 [18; 735] |
| PBH APP × Telefone 156 | 45 | 38.470 | +2,69 [1,02; 5,38] | +103.616 [38.194; 186.419] | +336 [−154; 829] |

### 3.1 Como ler o sinal (as duas medidas têm sinais próprios)

**Tempo** (colunas "diferença de mediana" e "dias de espera por ano"): positivo = B **mais lento** que A no mesmo serviço; negativo = B **mais rápido**.

**Taxa** (coluna "encerradas em ≤ 90 d a mais por ano"): positivo = B **encerra menos** que A em até 90 dias (seriam encerradas mais solicitações de B se tivesse o desempenho de A); negativo = B **encerra mais** que A.

- **Portal × PBH APP.** B = APP. O tempo é negativo (−1,69 dia na mediana ponderada, IC de −3,37 a −0,32): o **APP é um pouco mais rápido** que o Portal no mesmo serviço. A taxa também é negativa (−760 por ano, IC de −1.647 a −8): o **APP também encerra um pouco mais** em 90 dias. Nos dois casos o IC não inclui zero e o sentido é o mesmo (APP melhor). **Não é "impacto negativo"**: o sinal negativo quer dizer que B (APP) está em melhor situação.
- **Portal × Telefone 156 e APP × Telefone 156.** B = 156. O tempo é positivo nos dois pares: o **156 é mais lento** no mesmo serviço (cerca de 2 a 3 dias na mediana ponderada). A taxa é positiva nos dois (o 156 encerra menos em 90 dias), mas só no par com o Portal o IC exclui zero (+348, de 18 a 735). **No par APP × 156 o IC da taxa inclui zero (−154 a 829): não se afirma diferença na taxa**, só no tempo.
- **Tempo e taxa apontam no mesmo sentido nos três pares** (nas estimativas pontuais). Isso foi conferido nos dados, e o pipeline imprime um aviso explícito (painel e resumo) se, em outra execução, os sentidos forem opostos. Mesmo assim, as duas medidas têm ICs próprios e devem ser lidas separadamente: uma não confirma a outra.
- **Dentro de um mesmo serviço os sentidos podem divergir.** No Tapa-Buraco (Portal × APP), o tempo favorece o APP (−2 dias de mediana) e a taxa favorece levemente o Portal (+0,33 ponto percentual). É um exemplo de por que não se junta tempo e taxa numa conclusão só (`impacto_por_servico_par.csv`).

### 3.2 O que os números dizem e o que não dizem

- A diferença por pedido é **pequena** (poucos dias na mediana). Isso é coerente com `docs/interpretacao_resultados.md` §3.3: o delta de Cliff entre canais, dentro do serviço, é desprezível. Os totais anuais crescem porque são `volume de B × diferença de mediana`.
- **Dias de espera por ano** não é "total de dias de espera": é o volume anual de B multiplicado pela **diferença de medianas** do serviço, somada entre serviços. Medianas não se somam como médias; o número serve como **ordem de grandeza** e para comparar pares, não como contagem de dias vividos pelos cidadãos.
- **Concentração.** O resultado é puxado por poucos serviços grandes (`impacto_por_servico_par.csv`). No Portal × APP, o Tapa-Buraco responde por −90.314 dos −186.607 dias por ano (48%); sem ele, o total seria −96.293. No Portal × 156, Poluição Sonora – Fiscalização responde por +24.406 de +88.973 (27%); no APP × 156, Denúncias sobre Rede de Esgotos e Resíduos Sólidos responde por +25.562 de +103.616 (25%). O IC por bootstrap de serviços captura parte dessa instabilidade, e por isso é largo.
- O IC **não** cobre a incerteza de ordem causal (confusão por perfil do pedido dentro do serviço, escolha do canal pelo cidadão) nem a variação entre anos, nem o erro amostral das medianas dentro de cada serviço (o bootstrap reamostra serviços inteiros; o IC mede a heterogeneidade entre serviços).
- Em Portal × APP, 10 dos 159 serviços não têm mediana em algum dos canais (poucas encerradas) e ficam fora das medidas de tempo, mas entram na de taxa (`impacto_por_servico_par.csv`, linhas com `dias_solicitacao_ano` vazio).

## 4. Exemplos por serviço (5 maiores |dias de espera por ano|)

Fonte: `resultados/tabelas/impacto_por_servico_par.csv`, ordenado por |`dias_solicitacao_ano`|. O "?" em "Árvore ? Poda" é o travessão perdido na própria fonte da PBH (ver `config.chave_texto`).

| Serviço | Par (A × B) | Pedidos de B por ano | Dif. de mediana (dias) | Dif. de taxa (A − B, p.p.) | Dias de espera por ano | Encerradas a mais por ano |
|---|---|---:|---:|---:|---:|---:|
| Tapa-Buraco | Portal × APP | 45.157 | −2,0 | +0,33 | −90.314 | +148 |
| Árvore ? Poda de Árvore em Passeios, Praças, Etc | Portal × APP | 3.781 | −11,0 | −3,96 | −41.594 | −150 |
| Denúncias sobre Rede de Esgotos e Resíduos Sólidos em Estabelecimentos Comerciais ou Residências | APP × 156 | 1.549 | +16,5 | +3,78 | +25.562 | +59 |
| Poluição Sonora - Fiscalização | APP × 156 | 3.051 | +8,0 | +2,77 | +24.406 | +84 |
| Poluição Sonora - Fiscalização | Portal × 156 | 3.051 | +8,0 | +3,12 | +24.406 | +95 |

- As duas últimas linhas são o **mesmo serviço** com o 156 como B; o valor é o mesmo (24.406) porque Portal e APP têm a mesma mediana nesse serviço (11 dias) e o 156 tem 19 (`pares_por_servico.csv`). Os dois pares reaproveitam os mesmos pedidos do 156; não somar as duas linhas.
- Cada linha é um serviço e um par: o 156 só aparece em serviços que ele realmente atende (45 serviços em comum com cada canal digital).

## 5. Contexto de escala (fontes públicas: PBH, autodeclarada, e IBGE)

Fonte: `docs/evidencias/S01_criterios_do_software.md` §8 (conferido no navegador em 20/11/2026). Nenhum desses números vem da base analisada e **não** foram usados nas estimativas.

- 496.956 solicitações de serviços entre janeiro e outubro de 2023 nos quatro canais (PBH APP, Portal de Serviços, 156 e BH Resolve), segundo a PBH em 27/12/2023.
- 1.118 serviços solicitáveis diretamente pela internet e 1.492 serviços no Portal, segundo a PBH em 05/10/2026. Na mesma fonte, entre janeiro e setembro de 2026, 92% das demandas chegaram pelo Portal ou pelo aplicativo, 6% pelo 156 e 2% presencialmente.
- 2.315.560 habitantes em Belo Horizonte (IBGE, Censo 2022).

Uso e limite: servem para dar escala ao volume (centenas de milhares de pedidos por ano), mas são de datas diferentes das da base (2020–2023) e de natureza autodeclarada. O mix de canais de 2026 **não** vale para o período analisado, e esta análise **não** estima o impacto sobre 2024–2026 (a fonte termina em jul/2023, D11).

## 6. O que **não** é possível afirmar

- **Causalidade.** Que mudar o pedido de um canal para outro economizaria o tempo estimado. O cidadão escolhe o canal, o estudo é observacional, e mesmo dentro do serviço o perfil do pedido pode diferir entre canais.
- **Encerrada não é resolvida.** "Encerrada" é encerramento administrativo. Um canal mais rápido ou com mais encerramentos pode estar só fechando o pedido mais cedo. Os números **não** medem problema resolvido nem satisfação.
- **Presencial.** Os pares com Presencial ficaram **de fora**: o resultado agregado é inconclusivo (um serviço, o Tapa-Buraco, define o sinal do tempo; e a JARI domina a proporção; `docs/interpretacao_resultados.md` §4). Também não se usaram as medianas globais por canal, que misturam serviços diferentes e seriam enganosas.
- **Generalização.** Só vale para Belo Horizonte, solicitações criadas de mai/2020 a abr/2023 (coorte madura da base que vai até jul/2023) e serviços com ao menos 30 registros nos dois canais do par. Nada sobre 2024–2026, outras cidades ou serviços sem comparação válida.
- **Totais como economia real.** Os "dias de espera por ano" são uma escala de grandeza baseada em medianas, não uma contagem do tempo vivido nem uma economia a ser realizada.
- **Aprovação.** As decisões de desenho (90 dias, ≥ 30 por célula, estratificação por serviço) seguem sem aprovação do professor (P15, P16), e este documento não passou por revisão do grupo.

## 7. Por que não há conversão em horas do cidadão (P5)

A P5 pergunta como converter o impacto em horas. **Não foi feito**, de propósito:

1. A medida disponível é o **tempo até o encerramento administrativo** (dias entre criação e encerramento). Ela mede quanto a solicitação ficou em andamento no sistema da PBH, e **não** quanto esforço ou tempo ativo o cidadão gastou. A maior parte desse tempo é espera sem esforço.
2. A base não tem identificador do cidadão nem registro de interações, então não há como estimar tempo de uso do canal (preencher o Portal, ligar para o 156, ir ao BH Resolve).
3. Qualquer fator de conversão (minutos por pedido, valor da hora) seria **inventado**, e a FONTE_DA_VERDADE §11 e §17 proíbem afirmar economia de tempo ou horas sem métrica compatível e fonte.

Por isso a P5 segue **aberta**, com a nota "conversão não feita: sem métrica compatível". Para fechá-la seria preciso dado de esforço do cidadão (por exemplo, o tempo de preenchimento ou de ligação) com fonte.
