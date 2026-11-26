# Banco de perguntas da banca — LAB05

**Regra do grupo:** o professor pode pedir a **qualquer** integrante que explique **qualquer** parte (enunciado §8). Por isso cada integrante estuda **todas** as perguntas abaixo, não só as do seu bloco.

**Checklist humano (o material está pronto; o ensaio não):**

- [ ] Ensaio 1 cronometrado, ≤ 10:00
- [ ] Ensaio 2 cronometrado, ≤ 10:00
- [ ] Cada integrante respondeu 5 perguntas sorteadas deste banco, sem consultar
- [ ] Nomes completos dos integrantes nos slides e no roteiro (P14)
- [ ] `slides.html` aberto no projetor da sala e exportação em PDF testada (Ctrl+P)

**Como ler as fontes:** **DF** = `docs/documento_final.md` (a fonte de todo número); depois dela vêm os documentos de apoio, sempre com seção. As respostas têm no máximo 3 linhas; o detalhe está na fonte.

---

## Item 1 — O software: real, em operação, alto impacto

**1.1 Por que o objeto é real, está em operação e tem alto impacto?**
R: Real: o Portal carrega pacotes `@sydle/*` e traz "Powered by SYDLE". Em operação: no ar desde 12/05/2020. Impacto: 1.492 serviços catalogados (1.118 solicitáveis pela internet), 496.956 solicitações de jan a out/2023, 2.315.560 habitantes.
Fonte: DF §1, Tabela 1; `docs/evidencias/S01_criterios_do_software.md`.

**1.2 Esses números de volume são confiáveis?**
R: Os de volume são autodeclarados pela PBH, sem fonte independente, e mudam com a data (em 18/08/2026 eram 1.489 e 903), por isso levam a data. Os acessos mensais ao Portal são desconhecidos: o pedido pela LAI (P10) segue sem resposta registrada.
Fonte: DF §1; Apêndice B (P10).

**1.3 Se o estudo não usa código-fonte, que "software" é esse?**
R: O objeto é o ecossistema de atendimento ao cidadão (Portal, PBH APP, Telefone 156, BH Resolve), observado pelas solicitações que a PBH publica como dados abertos. O código não é analisado.
Fonte: DF §1; `FONTE_DA_VERDADE.md` §4.

---

## Item 2 — Pergunta, caminho, planejamento e dados

**2.1 Qual é a pergunta e como ela virou métricas (GQM)?**
R: "Para um mesmo serviço, o tempo de encerramento e a proporção encerrada diferem conforme o canal?" Q1 tempo por canal; Q2 proporção encerrada; Q3 mesmo serviço (OR de Mantel–Haenszel, delta de Cliff combinado); Q4 serviços com maior diferença.
Fonte: DF §2.2, Tabela 2.

**2.2 Por que a metodologia mudou de participantes para dados abertos? E a auditoria Lighthouse?**
R: O experimento com 32 participantes (celular × computador) exigia recrutar e moderar dezenas de sessões, sobrecarga incompatível com o grupo. A auditoria Lighthouse de 8 páginas fazia parte da proposta antiga; foi gerada em 24/11/2026 antes do aceite (D12) e está arquivada, fora da análise. O objeto e os três critérios do software continuam válidos.
Fonte: DF §2.1; `docs/metodologia.md` §2; `FONTE_DA_VERDADE.md` §14 (P12), §18 (D12) e §19 (v3.0).

**2.3 O professor aprovou a mudança de metodologia?**
R: Não há registro de aprovação (P15), nem das decisões de desenho: coorte de 90 dias, mínimo de 30 por célula, estratificação por serviço (P16). Tratamos as duas como abertas e dizemos isso no documento.
Fonte: DF, aviso inicial, §2.1 e Apêndice B; `FONTE_DA_VERDADE.md` §14.

**2.4 Por que 90 dias de seguimento e mínimo de 30 por célula?**
R: Os 90 dias formam a coorte madura: sem isso, as solicitações recentes pareceriam "abertas" só por falta de tempo (censura à direita); 30 e 180 dias mantêm o sentido do **OR de Mantel–Haenszel** em todos os pares. O mínimo de 30 é uma regra prática para que a mediana e a proporção de cada célula não dependam de poucos casos e para que os testes assintóticos sejam razoáveis; é arbitrária, e o documento não testa a sensibilidade a ela. As duas decisões esperam validação do professor (P16).
Fonte: DF §2.3, §3 e §6.4; `docs/metodologia.md` §6.

**2.5 Quais são as variáveis e as hipóteses? Foram pré-registradas?**
R: Fator: canal (4 níveis). Dependentes: tempo em dias (só encerradas) e "encerrada em até 90 dias". Controle: serviço. As H0 dizem "sem diferença". Não são pré-registradas: foram escritas em 25/11/2026, depois dos resultados, embora testes e definições tenham sido fixados antes (C6).
Fonte: DF §2.3 e §8 (C6).

**2.6 Como a coleta respeita a ética e a privacidade?**
R: API do CKAN a 1 requisição por segundo, com user-agent identificado; o Portal não é acessado de forma automatizada. Endereço e localização são descartados na leitura (lista branca), o Id é pseudonimizado e os CSVs brutos ficam fora do repositório; 74 testes cobrem isso.
Fonte: DF §3.

**2.7 O pipeline é reproduzível? Quem o reexecutou?**
R: Foi reexecutado do zero em 25/11/2026 por um agente de IA (Claude Sonnet), a pedido de um integrante, e não por um integrante. Os 10 CSVs saíram com os mesmos SHA-256; só houve diferenças de forma (última casa decimal de 41 números). Veredito: "reproduzido com ressalvas".
Fonte: DF §3 (Reprodutibilidade).

**2.8 Os dados vão até 2026?**
R: Não. A cobertura real é de maio/2020 a julho/2023; a proposta inicial supunha até 2026 e a fonte desmentiu (D11). Perguntar à PBH se há dados posteriores é a pendência P17.
Fonte: DF §3 e Apêndice B; `FONTE_DA_VERDADE.md` §18 (D11).

**2.9 O que é a coorte madura e por que ela evita a censura à direita?**
R: Só entram solicitações com pelo menos 90 dias de seguimento até o corte de observação. Sem isso, as recentes pareceriam "abertas" por falta de tempo, e a taxa de encerramento sairia artificialmente baixa. O custo: 139.233 registros da coorte imatura ficam fora, e o corte é um proxy (a maior data de encerramento de cada arquivo, K3).
Fonte: DF §3 (Tabela 3), §8 (I3, K3).

**2.10 Por que estratificar por serviço?**
R: Porque cada canal recebe uma mistura diferente de serviços, e o serviço está ligado ao tempo e à taxa de encerramento (confusão, I1). Comparar canais dentro do mesmo serviço retira essa mistura. É controle estatístico, não experimental: urgência e perfil do solicitante continuam sem controle.
Fonte: DF §2.3, §4 (Tabela 4) e §6.2.

**2.11 Como vocês garantem, na prática, a espera de 1 requisição por segundo? Isso é ética?**
R: O cliente usa `time.perf_counter()` com laço de reconferência, porque no Python 3.12/Windows `time.monotonic()` tem resolução de 15,625 ms e deixava o intervalo real até ~16 ms abaixo do pedido; o teste mede cada intervalo com relógio de alta resolução. Além disso, o user-agent é identificado (o servidor bloqueia o padrão) e o Portal não é acessado de forma automatizada.
Fonte: DF §3; `scripts/coleta.py` (`_esperar`); `tests/test_coleta.py` (`test_intervalo_real_medido_com_relogio_de_alta_resolucao`); `docs/evidencias/verificacao_pipeline.md`; `FONTE_DA_VERDADE.md` §4.2.

**2.12 Dá para confiar numa reprodução feita por um agente de IA?**
R: Ela confere o que uma máquina verifica: mesmos SHA-256 dos 10 CSVs e da base, tabelas idênticas, 74 testes. Não foi feita por um integrante, e o documento diz isso; o veredito é "reproduzido com ressalvas" (duas falhas de portabilidade, uma delas na espera de 1 req/s, corrigidas sem mudar parâmetros nem resultados). Um integrante pode repetir o procedimento do Apêndice A.
Fonte: DF §3 (Reprodutibilidade) e Apêndice A; `docs/evidencias/verificacao_pipeline.md` (Conclusão).

**2.13 O professor foi avisado da mudança de metodologia?**
R: A metodologia (v3.0, 24/11/2026) registra que a mudança ainda não foi submetida ao professor (P15), e não há registro de aprovação, nem do desenho (P16). Por isso a apresentação declara isso e não trata a mudança como aprovada; a validação é pendência do grupo com o professor.
Fonte: DF, aviso inicial e Apêndice B; `docs/metodologia.md` §2; `FONTE_DA_VERDADE.md` §14 e §19 (v3.0).

---

## Item 3 — Sete categorias da pesquisa

**3.1 Por que não é um experimento, se o laboratório se chama "Experimento Final"?**
R: Porque o canal não foi atribuído aleatoriamente nem pelo pesquisador: o cidadão escolhe por onde pedir (autosseleção). O enunciado aceita estudo observacional, mas exige classificar corretamente e discutir a força da evidência, que aqui é de associação, não de causa.
Fonte: DF §4; `docs/metodologia.md` §7 ("Por que não é um experimento").

**3.2 Quais são as sete categorias e a classificação de vocês?**
R: Natureza: aplicada. Objetivos: descritiva e exploratória-comparativa. Abordagem: quantitativa. Procedimentos: pesquisa documental e observacional retrospectivo (*ex post facto*). Tempo: coorte retrospectiva. Controle: estatístico, por serviço. Evidência: associação, não causa.
Fonte: DF §4, Tabela 4.

**3.3 O que mudou na revisão das categorias?**
R: "Longitudinal retrospectivo" foi corrigido para coorte retrospectiva com análise agregada: os três anos são analisados juntos, sem tendência temporal. As demais mudaram só de redação.
Fonte: DF §4; `docs/metodologia.md` §7.

**3.4 Por que "descritiva e exploratória-comparativa" e não "explicativa"?**
R: Q1 e Q4 descrevem; Q2 e Q3 comparam, mas só medem associação, e nenhum teste busca o mecanismo causal. A explicação sobre o fluxo interno do serviço (triagem, roteamento) é uma hipótese, não algo que os dados mostram.
Fonte: DF §4 e §6.3.

**3.5 Isto é um quase-experimento?**
R: Não alegamos isso. O documento o classifica como observacional retrospectivo (*ex post facto*): não houve atribuição de tratamento, nem por regra ou evento externo, o cidadão escolhe o canal, e o controle é só estatístico (estratificação por serviço). Por isso a conclusão é de associação, não de causa.
Fonte: DF §2.3 (Design) e §4 (Tabela 4: Controle e Nível de evidência).

---

## Item 4 — Conceitos da disciplina

**4.1 Como Goodhart e Campbell se aplicam ao estudo?**
R: Quando uma medida vira meta, deixa de medir bem. Se a taxa de encerramento virasse meta, poderia ser "jogada" (encerrar sem resolver). Por isso o texto diz "encerrada", nunca "resolvida" (K1). A cautela que levamos ao gestor é leitura nossa, não resultado dos dados.
Fonte: DF §10, Tabela 11, e §8 (K1).

**4.2 E a falácia de McNamara?**
R: Medir só o que é fácil (a data de encerramento) e ignorar o que importa ao cidadão (resolução, satisfação). A resolução é um atributo externo do processo que os dados não trazem; não a medimos.
Fonte: DF §10, Tabela 11.

**4.3 Como o GQM de Basili foi aplicado?**
R: Analisar as solicitações do BH Digital, com o propósito de comparar, quanto ao tempo e à taxa de encerramento, do ponto de vista da gestão do atendimento, no contexto dos dados abertos da PBH de mai/2020 a jul/2023. Daí saem Q1 a Q4 e suas métricas.
Fonte: DF §2.2.

**4.4 Que tipo de métrica é o tempo de encerramento? Por que mediana e não média?**
R: É métrica de processo, análoga a lead time e MTTR, em escala de razão. A distribuição é muito assimétrica (no Portal, média de 23,1 dias contra mediana de 3) e tem muitos empates em 0, então usamos mediana, quartis e testes de postos.
Fonte: DF §5.1, Tabela 5.

**4.5 O que é confusão (confounding) neste estudo?**
R: O tipo de serviço está ligado ao canal e ao tempo: cada canal recebe uma mistura diferente de demandas. Por isso o efeito global some em grande parte dentro do serviço: V de Cramér de 0,46 para 0,040 (mediana de 58 serviços).
Fonte: DF §6.2 e §8 (I1).

**4.6 Quais são a entidade e os atributos medidos?**
R: Entidade: o processo de atendimento de cada solicitação. Atributos internos: tempo de encerramento (medida derivada da diferença entre duas datas medidas diretamente) e encerramento em até 90 dias (derivada). O atributo externo que interessa ao cidadão, a resolução, não é medido (K1).
Fonte: DF §10, Tabela 11.

**4.7 Que escala tem a taxa de encerramento?**
R: "Encerrada em até 90 dias" é nominal binária em cada solicitação, e os testes usam essa variável (qui-quadrado, Fisher, CMH). A taxa de encerramento até o corte é uma razão (%), só descritiva; o tempo, em dias, é razão.
Fonte: DF §5.1, Tabela 5.

---

## Item 5 — O que foi reaproveitado dos laboratórios anteriores

**5.1 O que foi reaproveitado dos Labs 01 a 04 e o que é novo?**
R: Conceitos: Lab01 coleta via API (novo: cliente do CKAN a 1 req/s); Lab03 métricas de operação (tempo ≈ lead time/MTTR); Lab04 escolha de teste, tamanho de efeito e painel (novo: testes não paramétricos e estratificados). Lab02 foi substituído.
Fonte: DF §11, Tabela 12.

**5.2 Onde está o código dos Labs 01 e 04?**
R: Não está neste repositório: os laboratórios entram como conceito. A evidência do que é novo está em `scripts/coleta.py`, `scripts/estatistica.py` e `scripts/visualizacao.py`.
Fonte: DF §11.

**5.3 Por que não simularam poder e erro tipo I, como no Lab04?**
R: O estudo usa todas as solicitações publicadas, não uma amostra planejada, e com n dessa ordem o poder para diferenças mínimas já é quase total. A questão vira a relevância prática, por isso a leitura é pelo tamanho do efeito.
Fonte: DF §11 e §5.2.

---

## Item 6 — Resultados e análise (tipo e escala dos dados)

**6.1 Qual é a decisão sobre as hipóteses?**
R: Rejeitadas: H-Q1 e H-Q2 (p < 0,0001) e, nos seis pares, H-Q3p (CMH) e H-Q3t (van Elteren), com Holm. Os sinais rejeitam no tempo em 4 pares e na proporção só em Portal × PBH APP; por serviço, 30 e 59 de 286 comparações. Nenhuma é relevante pela regra: sem Presencial, delta desprezível e diferença de risco mediana < 1 p.p.; com Presencial, inconclusivo.
Fonte: DF §6.2 ("Decisão sobre as hipóteses") e §2.3.

**6.2 Por que não decidir só pelo p?**
R: Com n da ordem de 10⁵ a 10⁶, quase todo p sai minúsculo e não discrimina (C1). A leitura é pelo tamanho do efeito e pela consistência entre serviços; a regra exige p < 0,05 (Holm) e magnitude ao menos "pequena".
Fonte: DF §5.2 e §8 (C1).

**6.3 O que é o delta de Cliff e como se lê?**
R: Mede a dominância estocástica: a chance de um tempo do canal A ser maior que o de B, menos a chance contrária. Vai de −1 a 1; |delta| < 0,147 é desprezível, < 0,33 pequena, < 0,474 média. Delta > 0 = A mais lento.
Fonte: DF §5.2; `docs/metodologia.md` §6.

**6.4 O que é o CMH (OR de Mantel–Haenszel)?**
R: O OR de Mantel–Haenszel combina as tabelas 2×2 (canal × encerrada em 90 dias) de cada serviço num OR comum; o teste CMH verifica se esse OR é 1, controlando o serviço. OR > 1 quer dizer que A tem mais chance de encerrar. O OR comum supõe efeito parecido entre serviços; com I² de 0,89 a 0,99 isso não vale (C3), então ele não representa serviço algum e lemos junto a mediana da diferença de risco e o teste dos sinais.
Fonte: DF §5.2, Tabela 7, §8 (C3).

**6.5 Isso é o paradoxo de Simpson?**
R: Simpson é o caso extremo da confusão: o sentido se inverte ao separar por estrato. Em geral vimos atenuação (V de Cramér de 0,46 para 0,040), que é confusão sem inversão. Há um padrão do tipo Simpson no Presencial: no agregado ele encerra muito menos (10,6% contra 87,0% do Portal), mas, nos serviços em comum, encerra mais que o Portal em 12 de 18 serviços sem empate (p 0,71, sem significância). A D14 é outra coisa: a escolha do peso entre serviços inverte o resumo combinado. Não usamos o rótulo porque a inversão não é robusta (pares inconclusivos).
Fonte: DF §6.1, §6.2 (Tabelas 6, 7 e 8) e §8 (I1, C2); `resultados/tabelas/pares_ajustados_por_servico.csv` (Portal × Presencial: 6 e 12 serviços, p dos sinais com Holm 0,71).

**6.6 O que é a D14 e por que o Presencial é "inconclusivo"?**
R: Com o peso n_A·n_B, um serviço grande domina o delta combinado: no Tapa-Buraco, o Presencial tem 217 encerradas contra 94.968 do Portal e 133.634 do APP. Com outro peso ou com a mediana por serviço, o sinal se inverte; logo, o tempo do Presencial frente aos digitais é inconclusivo.
Fonte: DF §5.3 e §6.2; `docs/interpretacao_resultados.md` §4; `FONTE_DA_VERDADE.md` §18.

**6.7 E por que 156 × Presencial "não se interpreta"?**
R: Só 2 serviços têm as duas células com mínimo de 30 registros. O OR (0,55) e a diferença de risco (−12,8 pp) saem de apenas esses dois serviços e não generalizam.
Fonte: DF §6.2, Tabelas 7 e 8; §8 (E3).

**6.8 Se o Presencial tem 10,6% encerrado, ele é o pior canal?**
R: Não se pode dizer. 44.391 dos 50.057 pedidos presenciais (88,7%) são recursos à JARI, que ficam "em andamento" (1,2% encerrados). Nos pares com Presencial, a heterogeneidade é quase total (I² de 0,99) e a diferença de risco mediana fica perto de zero.
Fonte: DF §6.1 e §6.2.

**6.9 O Telefone 156 é mais lento? Por quê?**
R: A mediana é 20 dias contra 3, mas no mesmo serviço o 156 é mais lento em cerca de 3 de cada 4 serviços em comum com magnitude desprezível (delta mediano de −0,06). A distância vem sobretudo de ele atender outro conjunto de serviços.
Fonte: DF §6.1 e §6.2 ("O que se pode dizer").

**6.10 O APP é melhor que o Portal?**
R: É o resultado mais robusto: o APP encerra mais em 94 de 159 serviços em comum e é mais rápido em 98 de 149, com o mesmo sentido em qualquer ponderação. Mas a diferença é desprezível para o cidadão médio.
Fonte: DF §6.2.

**6.11 O horizonte de 90 dias muda a conclusão?**
R: Não: o OR de Mantel–Haenszel mantém o sentido de todos os pares em 30, 90 e 180 dias (Portal × APP: 0,84, 0,84 e 0,77). Nos pares com Presencial o OR é instável (Portal × Presencial de 12,0 a 24,5; APP × Presencial de 7,6 a 23,2), dominado pela JARI.
Fonte: DF §6.4.

**6.12 Por que mediana condicional, Kaplan–Meier e correção de Holm?**
R: Só as encerradas têm tempo, então a mediana é condicional a ter encerrado e vem junto da proporção encerrada; Kaplan–Meier (abertas como censuradas) confere. Holm ordena os p de uma família e compara o menor com 0,05/m, o seguinte com 0,05/(m−1), e assim por diante, parando no primeiro que não rejeita; controla a chance de ao menos um falso positivo na família, com mais poder que Bonferroni. As famílias são: proporções por serviço-par, tempos por serviço-par, omnibus por serviço e pares ajustados. Não corrige entre famílias (C7).
Fonte: DF §5.1, §5.2 e §8 (C7); `docs/metodologia.md` §6.

**6.13 Onde a diferença entre canais é realmente grande?**
R: Em poucos serviços. Tempo: Tapa-Buraco (1 dia no APP contra 19 no 156). Proporção em 90 dias: Iluminação Pública, luminária apagada à noite (APP 75,3% contra 36,2% do 156). São os candidatos a investigar.
Fonte: DF §6.3.

**6.14 O que significa um I² de 0,89 a 0,99?**
R: O I² mede quanto da variação do OR entre serviços vem de diferença real entre eles, não de acaso; perto de 0,99 é quase tudo. Quer dizer que o efeito do canal muda de serviço para serviço, e o OR combinado não representa serviço algum (C3). Por isso lemos junto a mediana por serviço e o teste dos sinais.
Fonte: DF §5.2 e §8 (C3).

**6.15 O que é o teste de van Elteren?**
R: É a versão estratificada do teste de postos (Mann–Whitney): compara o tempo de dois canais dentro de cada serviço e combina os serviços num único teste, controlando o serviço. Entra como teste de H-Q3t, para o tempo dos seis pares.
Fonte: DF §2.3 e §5.2; `docs/metodologia.md` §6.

**6.16 O que é o teste dos sinais e por que usá-lo?**
R: Conta em quantos serviços cada canal leva vantagem e testa se a chance é a mesma (H0). Cada serviço pesa um voto, então um serviço grande, como o Tapa-Buraco, não domina o resultado; é a contraprova do valor combinado.
Fonte: DF §2.3, §5.2 e §6.2.

**6.17 Por que delta de Cliff e não a diferença de medianas?**
R: Há muitos empates: o encerramento no mesmo dia é frequente (28,7% no Portal), e a mediana pode ser igual com distribuições diferentes. O delta de Cliff mede dominância estocástica (um canal tender a ser mais lento), que é o que os testes de postos avaliam.
Fonte: DF §5.1, §5.2 e Tabela 6; `docs/metodologia.md` §6.

**6.18 Que testes e tamanhos de efeito valem para o resultado global?**
R: H-Q1 (tempo): Kruskal–Wallis, com ε² de 0,077. H-Q2 (proporção em 90 dias): qui-quadrado r×2, com V de Cramér de 0,46. Os dois rejeitam, mas misturam serviços, e não há limiar de magnitude fixado para essas medidas; dentro do serviço, a mediana do V cai para 0,040 e a do ε² para 0,006.
Fonte: DF §2.3, §6.1 e §6.2.

**6.19 O peso n_A·n_B foi escolhido antes dos resultados?**
R: O peso principal, sim: testes, horizonte e peso foram fixados antes. O peso alternativo, n_A·n_B/(n_A+n_B), e a mediana por serviço foram acrescentados em 25/11/2026, depois de ver os resultados (D14), quando um serviço se mostrou dominante; a análise principal não mudou.
Fonte: DF §5.3 e §8 (C2, C6).

**6.20 Qual é a mediana de Kaplan–Meier do Presencial?**
R: Não existe: só 11,5% encerraram até o corte, menos da metade. A mediana do Presencial (4 dias) vem apenas das encerradas, por isso não é comparável com a dos outros canais.
Fonte: DF §6.1, Tabela 6 e texto da Figura 2.

**6.21 O 156 atende os mesmos serviços que os canais digitais?**
R: Não: o 156 atende 68 serviços, contra mais de 360 nos digitais, em geral de fiscalização e manutenção urbana. Por isso a distância de 3 contra 20 dias nas medianas gerais vem sobretudo do conjunto de serviços, e encolhe no mesmo serviço.
Fonte: DF §6.2 ("O que se pode dizer", item 1).

---

## Item 7 — Ameaças à validade (4 tipos)

**7.1 Quais são as ameaças dos 4 tipos e quais são as mais sérias?**
R: Vinte: conclusão (C1 a C7), interna (I1 a I4), construto (K1 a K5) e externa (E1 a E4). As mais sérias são I1 (confusão pelo serviço), C2 (um serviço domina o efeito com Presencial), K1 (encerrada não é resolvida) e E1 (só BH, mai/2020 a jul/2023).
Fonte: DF §8, Tabela 10; `docs/metodologia.md` §8.

**7.2 "Encerrada" significa "resolvida"?**
R: Não. É encerramento administrativo: um canal que encerra antes pode só fechar o pedido mais cedo. A fonte não documenta o significado da situação (K2), então não classificamos em "resolvido" ou "negado".
Fonte: DF §8 (K1, K2) e §3.

**7.3 Escrever as hipóteses depois dos resultados é um problema?**
R: Sim, é uma ameaça (C6): o rigor é menor que o de um estudo pré-registrado. A mitigação foi fixar antes testes, horizonte e peso, e exigir magnitude mínima; a análise de sensibilidade da D14 também foi acrescentada depois de ver os resultados, sem mudar a análise principal.
Fonte: DF §2.3, §5.3 e §8 (C6).

**7.4 O que a autosseleção do canal e a censura fazem com o resultado?**
R: Autosseleção (I2): o cidadão escolhe o canal, e urgência e perfil não estão nos dados; sobra confusão residual, e por isso falamos em associação. Censura (I3): pedidos recentes parecem abertos; mitigada pela coorte de 90 dias, mas o corte de observação é um proxy (K3).
Fonte: DF §8 (I2, I3, K3).

**7.5 O resultado vale para outras cidades ou depois de 2023?**
R: Não. Só Belo Horizonte, de mai/2020 a jul/2023 (inclui a pandemia), e só os serviços com ao menos 2 canais comparáveis: 164 de 422, e os 258 fora somam 4,2% das elegíveis. Os canais Integração, Origem Interna e E-mail ficaram de fora.
Fonte: DF §8 (E1 a E4).

**7.6 Por que os canais Integração entre Sistemas, Origem Interna e E-mail ficaram de fora?**
R: A PBH não documenta o significado de Integração entre Sistemas e Origem Interna, nem o da coluna de situação, e por isso não os interpretamos. Os três canais somam 298.570 registros (20,2% da base), e o resultado não vale para eles (K2, E4).
Fonte: DF §3 (Tabela 3 e Limitações da fonte) e §8 (K2, E4).

**7.7 Os pedidos são independentes entre si?**
R: Não dá para verificar: a fonte não traz identificador do cidadão (C4). A independência é declarada como suposição, e os ICs e os valores de p podem estar otimistas.
Fonte: DF §3 (Limitações da fonte) e §8 (C4).

---

## Item 8 — Impacto e o que não se pode afirmar

**8.1 Como o impacto foi calculado?**
R: É um contrafactual hipotético: "se os pedidos do canal B tivessem o desempenho do canal A no mesmo serviço". A diferença de mediana (B − A) por serviço é ponderada pelo volume anual de B; o IC de 95% vem de bootstrap de serviços.
Fonte: DF §7 (Método).

**8.2 Quais são os números e como se lê o sinal?**
R: Portal × APP (B = APP): −1,69 dia na mediana e −186.607 dias de espera por ano; o sinal negativo quer dizer que o APP é mais rápido. Com o 156 (B = 156), +2,31 e +2,69 dias: o 156 é mais lento.
Fonte: DF §7, Tabela 9 e "Como ler o sinal".

**8.3 Esses dias de espera por ano são uma economia de tempo?**
R: Não. São escala de grandeza, não uma economia que alguém vá obter: somam diferenças de medianas entre serviços e multiplicam por centenas de milhares de pedidos. O Tapa-Buraco responde por 48% do Portal × APP.
Fonte: DF §7 ("Limites do número") e §9.4.

**8.4 Por que os pares com Presencial ficam fora do impacto? E por que não há conversão em horas?**
R: Ficam fora por serem inconclusivos (D14). Não se converteu em horas (P5, aberta) porque a medida é o tempo até o encerramento administrativo, não o esforço do cidadão, e qualquer fator de conversão seria inventado.
Fonte: DF §7 e Apêndice B (P5).

**8.5 O que o estudo não permite afirmar?**
R: Que mudar de canal acelera o atendimento; que o Presencial encerra menos ou é mais lento no mesmo serviço; que encerrado é resolvido; que os dias de espera são economia; e qualquer coisa fora de BH, de mai/2020 a jul/2023 e dos serviços com ao menos 2 canais comparáveis.
Fonte: DF §9.4.

**8.6 Qual é a recomendação ao gestor?**
R: A diferença global está em qual serviço cada canal atende; os serviços da Seção 6.3 (Tapa-Buraco, Iluminação Pública, JARI) são os primeiros a investigar. Para o cidadão, Portal e APP fazem pouca diferença, e o 156 tende a ser um pouco mais lento. Como leitura nossa (Goodhart, §10): cuidado ao usar a taxa de encerramento como meta.
Fonte: DF §9.2, §6.3 e §10.

**8.7 O que vocês fariam a seguir?**
R: Perguntar à PBH se há dados após jul/2023 e qual é a regra da situação (P17); combinar com um survey de usuários; incluir o ano na análise; testar o OR de Mantel–Haenszel sem o serviço Recurso à JARI.
Fonte: DF §9.5.

**8.8 Se o delta é desprezível, por que um impacto de 1,69 dia por pedido?**
R: São medidas diferentes: o delta mede dominância (probabilidade), não dias; os 1,69 dia são a diferença de mediana por serviço, ponderada. Para o cidadão médio a diferença é desprezível; os 186.607 dias por ano só parecem grandes por multiplicar poucos dias por centenas de milhares de pedidos.
Fonte: DF §6.2 (item 2), §7 (introdução e "Limites do número").

**8.9 O que mudaria com mais dados?**
R: O que mais limita é o que falta: resolução além do encerramento (K1, K2), identificador do cidadão (C4), urgência e perfil (I2) e o ano (I4). Dados após jul/2023 testariam a validade no tempo (E1), e o survey com usuários traria o lado do cidadão; a PBH precisa confirmar se esses dados existem (P17).
Fonte: DF §3 (Limitações da fonte), §8 e §9.5.