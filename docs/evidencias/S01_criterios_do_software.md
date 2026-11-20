# Evidências dos critérios do software — Portal de Serviços da PBH

Issue: Laboratorio-Medicao/Lab05#16 (parte de #15) · Sprint S01 · Criado em 20/11/2026
Referências: [FONTE_DA_VERDADE.md](../../FONTE_DA_VERDADE.md) §4 e §14 · [Proposta §1](../proposta/LAB05_S01_Proposta_FINAL.md) · [Enunciado](../enunciado/ENUNCIADO_LAB05.pdf) §2

> **Estado honesto deste registro:** nada abaixo encerra P7, P8, P9 ou P10. O que foi verificado está marcado como tal; o restante é **roteiro para o grupo executar à mão no navegador**, porque (a) o enunciado exige respeito a robots.txt e termos de uso, (b) o robots.txt do Portal tem `Disallow: /` e a P12 (aceite do professor) está aberta, e (c) o site institucional da PBH bloqueia acesso automatizado ("Acesso Bloqueado"), bloqueio que não deve ser contornado.

Legenda de status: **V-API** = verificado por consulta a API pública em 20/11/2026 · **A fazer** = depende de acesso manual do grupo · **Não verificado** = citado na proposta, sem checagem independente.

---

## 1. Matriz critério × evidência

| Critério (enunciado §2a) | Afirmação (Proposta §1) | Fonte | Status | Como completar |
|---|---|---|---|---|
| Real | HTML da página inicial carrega `@sydle/pbh-components`, `@sydle/sydle-one-components`, `@sydle/service-desk-components`, `org: "bhdigital"` | Página inicial do Portal | **Confirmado no HTML (P7 encerrada)** | §2 |
| Real | SYDLE ONE é plataforma de BPM, CRM e Service Desk | sydle.com/br | **Verificado (§8)** | Concluído |
| Em operação | Portal no ar desde maio/2020, com login gov.br | PBH, 12/05/2020 | **Verificado (§8)**: lançamento em 12/05/2020. Login gov.br confirmado no próprio Portal (P7), não no trecho lido da notícia | Concluído |
| Em operação | Versão atual / último release | — | **Lacuna**: o enunciado pede "versão atual, data do último release". Plataforma comercial: registrar versão observada dos pacotes `ui-package` (P7) e a data da observação | Roteiro §2 |
| Alto impacto | 1.492 serviços catalogados, 1.118 solicitáveis pela internet; 92% das demandas jan–set/2026 via Portal ou app | PBH, 05/10/2026 | **Verificado (§8)** | Concluído |
| Alto impacto | 496.956 solicitações jan–out/2023 (Portal + app + 156 + BH Resolve) | PBH, 27/12/2023 | **Verificado (§8)**. Lembrar: soma de 4 canais | Concluído |
| Alto impacto | BH eleita cidade mais digital do Brasil pelo 3º ano | PBH, 18/08/2026 | **Verificado (§8)** | Concluído |
| Alto impacto | 2.315.560 habitantes, Censo 2022 | IBGE | **Verificado** (API + navegador, §3) | Concluído (P9) |
| Alto impacto | Acessos mensais ao Portal | — | **Desconhecido** | Pedido LAI (§5, P10). **Não inventar o número** |

---

## 2. P7 — HTML da página inicial (roteiro manual)

Objetivo: documentar **como** a leitura do HTML foi obtida, de forma compatível com navegação manual. Fazer **uma** abertura da página inicial, em navegador comum, por uma pessoa.

1. Anotar data/hora, navegador e versão, e a URL exata.
2. Abrir a página inicial normalmente. Usar "Exibir código-fonte" (view-source) **ou** DevTools > Elements/Network, sem scripts, sem recarregamentos repetidos.
3. Localizar e copiar apenas o trecho que cita os pacotes `@sydle/*` e `org: "bhdigital"`.
4. Salvar o trecho em `docs/evidencias/capturas/` com nome `AAAA-MM-DD_portal_html_trecho.txt` (e uma captura de tela, se possível).
5. Registrar a versão/hash dos pacotes `ui-package` vistos (alimenta a regra "Portal muda durante a coleta", Proposta §8).
6. **Tempo de resposta (HTTP 200 em 0,49 s):** só reincluir na proposta se a medição for refeita de modo compatível com navegação manual (ex.: aba Network do DevTools numa única abertura), com a captura arquivada. Caso contrário, fica fora.
7. Preencher a tabela de registro abaixo.

| Campo | Valor |
|---|---|
| Data/hora | 20/11/2026, 18:57 |
| Quem coletou | Marcos Alberto |
| Navegador e versão | Chrome 158.0.8127.36 (arm64) |
| URL | https://servicos.pbh.gov.br |
| Método (view-source / DevTools) | view-source (Cmd+Option+U) e cópia do HTML, conforme informado pelo coletor em 20/11/2026 |
| Trecho arquivado em | [capturas/2026-11-20_portal_html_trecho.txt](./capturas/2026-11-20_portal_html_trecho.txt) (tokens redigidos). Captura de tela: não informada |
| Pacotes e versões/hash observados | `pbh-components` v:31309267200adce4ee6b7d4bc3b0b864; `sydle-one-components` v:9ef695195486dfa6dd532ed5932cc119; `service-desk-components` v:49472ac3036e940f5b83d29a5c1feff5; demais hashes no arquivo do trecho. `org: "bhdigital"`; app hash `lmegnwzk` |

**Resultado da leitura (20/11/2026):** o HTML confirma o que a proposta afirma: carrega `@sydle/pbh-components`, `@sydle/sydle-one-components`, `@sydle/service-desk-components` e `org: "bhdigital"`; o texto de login cita o acesso único gov.br. Achados adicionais, sem interpretação além do que o código mostra: a página é uma aplicação de página única (conteúdo montado por JavaScript); usa o widget VLibras e Google Tag Manager; o HTML contém tokens de autorização (redigidos e **não versionados**). O `<meta name="robots" content="noindex">` é da página e **não** substitui a leitura do `robots.txt`.

**P7 encerrada em 20/11/2026** (método confirmado pelo coletor). Ressalvas: captura de tela não anexada (opcional); número de aberturas da página não informado; o tempo de resposta de 0,49 s continua fora da proposta.

---

## 3. P9 — População de Belo Horizonte

| Item | Valor |
|---|---|
| Consulta | API de Dados Agregados do IBGE, agregado 9514 (Censo 2022), variável 93 (população residente), município 3106200 (Belo Horizonte), total de sexo/idade |
| Data do acesso | 20/11/2026 |
| Resultado | **2.315.560 pessoas** (2022) |
| URL (GET) | `https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6[3106200]&classificacao=2[6794]|287[100362]|286[113635]` |
| Acesso | 1 requisição, via terminal (não é a conferência "no navegador" que a P9 descreve) |

Confirma o número citado na proposta.

**Conferência no navegador (20/11/2026, ~19:20):** o assistente abriu, no Chrome do coletor e com autorização dele, `https://cidades.ibge.gov.br/brasil/mg/belo-horizonte/panorama` (uma abertura, sem login). A página "IBGE | Cidades@ | Minas Gerais | Belo Horizonte | Panorama" mostra: código do município 3106200; **"População no último censo [2022]: 2.315.560 pessoas"**; população estimada [2026]: 2.415.451 pessoas; densidade demográfica [2022]: 6.988,18 hab/km². O texto da página diz "Em 2022, a população era de 2.315.560 habitantes". Captura: [capturas/2026-11-20_ibge_cidades_bh.jpg](./capturas/2026-11-20_ibge_cidades_bh.jpg).

**P9 encerrada em 20/11/2026.** O número da proposta (2.315.560, Censo 2022) está correto. Observação: o IBGE publica também uma estimativa para 2026 (2.415.451); se a proposta citar população "atual", deixar claro que 2.315.560 é do Censo 2022. O site do IBGE é de terceiros e a abertura foi única.

---

## 4. P8 — Termos de uso do Portal

### 4.1 O que foi tentado em 20/11/2026 (busca na web; o Portal e o site institucional **não** foram acessados por ferramenta automatizada)

Duas buscas na web (resultados e trechos, não o conteúdo das páginas):

| Documento encontrado | URL | O que a busca mostra | Vale para o Portal? |
|---|---|---|---|
| Termos de uso do app BH SIM | https://prefeitura.pbh.gov.br/pbhapp/termos-de-uso | Termos do **aplicativo**; remetem ao menu "Sobre o BHSIM" | **Não** (é outro produto) |
| Política de privacidade do BH SIM | https://prefeitura.pbh.gov.br/pbhapp/politica-de-privacidade | Atualizada em 11/05/2026; cita login único do governo federal | **Não** (é outro produto) |
| Política de privacidade do site institucional | https://prefeitura.pbh.gov.br/politica-de-privacidade | Política do site da Prefeitura; isenta responsabilidade por sites de terceiros | **Não confirmado** |
| Política do SIF e da BHTRANS | …/sif/politica-de-privacidade/ ; …/bhtrans/bhtrans-operador-politica-de-privacidade | Sistemas distintos | **Não** |

**Conclusão parcial:** não foi localizado, por busca, um termo de uso ou política próprios de `servicos.pbh.gov.br`. **Isso não prova que não existam**: o Portal é uma aplicação de página única, e um link no rodapé pode não ser indexado. Também não é possível afirmar que os termos do BH SIM ou do site institucional se aplicam ao Portal. O conteúdo dessas páginas **não foi lido** (o site institucional bloqueia acesso automatizado e não foi contornado); só se conhecem os trechos mostrados pela busca.

Nenhuma restrição sobre axe DevTools, Lighthouse ou acesso automatizado foi encontrada, mas **nenhum texto de termos foi lido**, então isso é ausência de leitura, não ausência de restrição.

### 4.1b Captura do rodapé do Portal enviada pelo coletor (20/11/2026)

Arquivo: [capturas/2026-11-20_portal_rodape.png](./capturas/2026-11-20_portal_rodape.png) (captura de tela de https://servicos.pbh.gov.br, parte inferior da página inicial; data da captura informada como 20/11/2026, não consta na imagem).

O que a imagem mostra, sem interpretação além do visível:
- **Rodapé:** logo da Prefeitura, endereço (Av. Afonso Pena, 1212 – Centro, 30130-003), link `www.pbh.gov.br`, selo "Melhores.com — Prêmio" e a legenda **"Powered by SYDLE"**. **Nenhum link de "Termos de uso" ou "Política de privacidade" aparece na parte do rodapé capturada.**
- **Cartões acima do rodapé:** Fale Conosco, **Lei de Acesso à Informação – LAI** ("Direito de acesso às informações públicas"), Ouvidoria, Avalie.
- **Barra superior:** atalhos de acessibilidade ([1] conteúdo, [2] menu, [3] busca, [4] rodapé), Alto contraste, A+ / A−, "Acessibilidade", botão do VLibras.
- **Menu:** Portal da Prefeitura, O Portal, Serviços, Canais de Atendimento, Legislação para Atendimento Digital, Acompanhe sua Solicitação, Entrar.

Uso das evidências:
- **Critério "Real":** "Powered by SYDLE" no rodapé é evidência visual adicional de que o Portal usa SYDLE.
- **P8:** a captura cobre só o rodapé visível. **Não prova que não existam termos**: eles podem estar nos menus "O Portal" ou "Legislação para Atendimento Digital", que não foram abertos na captura.
- **P10:** o Portal tem um cartão próprio de LAI, que pode ser o canal para o pedido (a confirmar ao abrir o cartão).

### 4.2 Leitura dos Termos de Uso do Portal (20/11/2026, ~19:10)

**Como foi feito:** o assistente de IA (Claude em Chrome) operou o Chrome do coletor, **com autorização expressa dele**, em uma única sessão: abriu `https://servicos.pbh.gov.br/` uma vez, abriu o menu "O Portal" (que lista: Sobre o Portal, Política de Privacidade, Avalie o Portal, Dúvidas Frequentes, **Termos de Uso**), abriu "Termos de Uso" e rolou a página lendo. Sem login, sem formulário, sem envio de dados, poucas requisições. A aba foi fechada ao final. Esta leitura foi feita por navegação conduzida por ferramenta, **não** por uma pessoa digitando; isso deve ser informado ao professor junto com a P12.

| Campo | Valor |
|---|---|
| Data/hora e quem leu | 20/11/2026, ~19:10; leitura feita pelo assistente no navegador do coletor Marcos Alberto, com autorização dele |
| Link de termos no Portal? | **Sim**: menu "O Portal" > "Termos de Uso". URL: `https://servicos.pbh.gov.br/termos-de-uso+5df3bbb5ad0ab2006ceca0ad` (a página exibia "1445 visualizações"). O rodapé não tem link (ver §4.1b) |
| Estrutura do documento | 5 seções: (1) veracidade, integridade e atualização dos dados; (2) uso de informações de navegação (política de cookies); (3) uso do Google Analytics; (4) gestão e controle de cookies pelo usuário; (5) alterações nos termos de uso |
| Trechos relevantes (resumo) | Ao navegar ou usar os serviços, o usuário "declara estar ciente e concordar" com os termos. É vedado cadastro/acesso com dados de terceiros sem autorização. Dados inseridos devem ser verdadeiros. O Portal usa cookies e Google Analytics (dados de navegação, "estritamente anônimas"). A PBH pode alterar os termos a qualquer momento, com publicação na mesma página |
| Menciona acesso automatizado, robôs, raspagem, testes de carga, ou ferramentas de inspeção/auditoria (axe, Lighthouse)? | **Não.** Nenhum desses temas aparece no texto lido |
| Documentos vizinhos | Política de Privacidade do Portal existe no mesmo menu e **não foi lida** nesta sessão. Termos/política do BH SIM e do site institucional não se aplicam ao Portal por inferência e não foram lidos |
| Evidência | Captura do início: [capturas/2026-11-20_portal_termos_de_uso_inicio.jpg](./capturas/2026-11-20_portal_termos_de_uso_inicio.jpg). Texto transcrito apenas em resumo |

**Interpretação e limites (não ir além disso):**
- Os termos lidos **não proíbem nem autorizam** expressamente auditoria com axe/Lighthouse. Ausência de menção não é autorização.
- A seção 3 informa que o Portal registra comportamento de navegação via Google Analytics; as sessões do experimento e da auditoria gerarão tráfego registrado. Registrar essa observação na proposta, se o professor julgar relevante.
- Isso **não resolve** o `Disallow: /` do robots.txt nem a P12: a decisão sobre o uso das ferramentas continua do professor. O arquivo `robots.txt` do Portal **não foi lido** nesta etapa.
- Foi lida uma única versão do documento em uma única data; a seção 5 diz que os termos podem mudar. Reler antes da coleta (S02).

**P8: leitura registrada em 20/11/2026.** Resultado: termos existem, sem menção a acesso automatizado ou ferramentas de auditoria. Ressalva: Política de Privacidade não lida.

---

## 5. P10 — Pedido via LAI (rascunho, **não enviado**)

Enviar é uma ação externa e deve ser feita pelo grupo, com o integrante responsável. Rascunho:

> **Assunto:** Pedido de acesso à informação — acessos ao Portal de Serviços da PBH
>
> Com base na Lei nº 12.527/2011 (Lei de Acesso à Informação), solicito, para fins de pesquisa acadêmica (disciplina Laboratório de Experimentação de Software, Engenharia de Software, PUC Minas), os seguintes dados do Portal de Serviços da Prefeitura de Belo Horizonte:
> 1. Número mensal de acessos (sessões e usuários únicos), de janeiro de 2025 a outubro de 2026.
> 2. Distribuição desses acessos por tipo de dispositivo (celular, computador, tablet), se disponível.
> 3. Número mensal de solicitações de serviço registradas no Portal, por serviço, para os serviços: poda de árvore, alvará, reparo de buraco na via, segunda via de guia municipal.
>
> Pedido de formato: planilha ou CSV. Não solicito dados pessoais.
>
> [Nome do solicitante, contato institucional]

Observações: (i) os serviços listados são as **candidatas** da proposta, ainda não definitivas; (ii) usar contato institucional, não dado pessoal desnecessário; (iii) a resposta alimenta apenas o contexto e a análise secundária de impacto (P5), não o experimento.

| Campo | Valor |
|---|---|
| Canal | _a preencher (canal de transparência da PBH)_ |
| Data do envio | _a preencher_ |
| Protocolo | _a preencher_ |
| Prazo legal de resposta | 20 dias, prorrogáveis por mais 10 (Lei 12.527/2011, art. 11) — conferir antes de citar |
| Resposta (data e arquivo) | _a preencher_ |

**Encerra P10 quando** o protocolo de envio estiver arquivado e a resposta (ou o vencimento do prazo) registrada.

---

## 6. Cuidados éticos desta etapa

- **Atualização (20/11/2026, tarde):** depois deste registro inicial, o coletor autorizou expressamente que o assistente operasse o seu Chrome para ler os Termos de Uso (§4.2): uma sessão, uma abertura da página inicial e poucas navegações, sem login nem formulários. Isso é navegação conduzida por ferramenta e deve ser informado ao professor (P12). Antes disso: nenhuma requisição automatizada foi feita ao Portal.
- (Texto original desta seção) Nenhuma requisição automatizada foi feita ao Portal nem ao site institucional da PBH. A única consulta externa automatizada foi uma chamada à API pública do IBGE (1 requisição) e uma tentativa de ler o robots.txt do site institucional da PBH, que retornou "Acesso Bloqueado" e não foi repetida.
- As coletas manuais acima devem ser pontuais (uma abertura por página), sem repetição, em linha com o limite de 1 req/s e com `Disallow: /`.
- Nada aqui substitui o aceite do professor (P12).

## 7. Resumo do que falta para fechar a issue #16

| Pendência | Status em 20/11/2026 | Quem |
|---|---|---|
| P7 | **Encerrada** (HTML coletado, trecho arquivado sem tokens, método confirmado) | Marcos |
| P8 | **Encerrada** — Termos de Uso lidos (§4.2); sem menção a automação/ferramentas; Política de Privacidade não lida | Grupo |
| P9 | **Encerrada** — conferido no IBGE Cidades pelo navegador | Grupo |
| P10 | Aberta — rascunho §5 pronto, não enviado | Grupo (A) |
| Fontes PBH e SYDLE (6 afirmações) | Não verificadas de forma independente | Grupo, no navegador |

---

## 8. Conferência das fontes no navegador (20/11/2026, ~19:30–19:40)

**Como foi feito:** o assistente de IA (Claude em Chrome) operou o Chrome do coletor, com autorização expressa dele: uma aba, cada URL aberta uma vez, rolagem para ler, uma captura por página, aba fechada ao final. Sem login, sem formulário, sem aceitar cookies. Navegação conduzida por ferramenta; informar ao professor junto com a P12. Todas as páginas da PBH abriram normalmente no navegador (o bloqueio visto antes foi só para acesso por linha de comando).

| Afirmação da proposta | Fonte (URL) | O que a página mostra | Resultado | Captura |
|---|---|---|---|---|
| Portal lançado em maio/2020 na plataforma atual | [prefeitura.pbh.gov.br/noticias/prefeitura-lanca-novo-portal-de-servicos-para-facilitar-pedidos-line](https://prefeitura.pbh.gov.br/noticias/prefeitura-lanca-novo-portal-de-servicos-para-facilitar-pedidos-line) | "Prefeitura lança novo portal de serviços para facilitar pedidos on-line"; criado em 12/05/2020, atualizado em 22/05/2020. O novo Portal "inaugura uma plataforma unificada, o BH Digital"; "mais de 1 mil serviços" já com informações | **Confere** (lançamento). A menção a gov.br **não apareceu na parte lida**; o login gov.br está confirmado no HTML do Portal (§2) | [jpg](./capturas/2026-11-20_pbh_noticia_2020-05-12.jpg) |
| 496.956 solicitações, jan–out/2023 | [.../area-de-modernizacao-da-pbh-destaca-principais-resultados-em-encontro-anual](https://prefeitura.pbh.gov.br/noticias/area-de-modernizacao-da-pbh-destaca-principais-resultados-em-encontro-anual) | Criado em 27/12/2023. "De janeiro a outubro, os canais de atendimento da PBH (PBH APP, Portal de Serviços, 156 e atendimento presencial BH Resolve) registraram **496.956** solicitações de serviços." Também: Portal com 1.387 serviços, 936 solicitáveis na plataforma, 128 no PBH App; 168 serviços digitais em dez/2016 | **Confere** | [jpg](./capturas/2026-11-20_pbh_noticia_2023-12-27.jpg) |
| BH cidade mais digital pelo 3º ano | [.../belo-horizonte-e-eleita-cidade-mais-digital-do-brasil-pelo-terceiro-ano-consecutivo](https://prefeitura.pbh.gov.br/noticias/belo-horizonte-e-eleita-cidade-mais-digital-do-brasil-pelo-terceiro-ano-consecutivo) | Criado em 18/08/2026, atualizado em 16/11/2026. "Pelo terceiro ano consecutivo ... cidade mais digital do Brasil no ranking de Prefeituras Digitais 2026 do Melhores.com", nota 8,7 de 10 | **Confere**. Atenção: esta página cita **1.489 serviços, 903 solicitáveis**, números diferentes dos de 05/10/2026 | [jpg](./capturas/2026-11-20_pbh_noticia_2026-08-18.jpg) |
| 1.492 serviços; 1.118 solicitáveis; 92% das demandas | [.../em-uma-decada-pbh-amplia-em-mais-de-500-servicos-digitais-simplifica-processos-e-melhora](https://prefeitura.pbh.gov.br/noticias/em-uma-decada-pbh-amplia-em-mais-de-500-servicos-digitais-simplifica-processos-e-melhora) | Criado em 05/10/2026. "168 serviços, em 2016, para 1.118 atualmente, que podem ser solicitados diretamente pela internet" (+565,5%); "Portal de Serviços reúne informações sobre 1.492 serviços"; "entre janeiro e setembro de 2026, 92% das demandas ... Portal de Serviços ou pelo aplicativo", 6% por telefone 156, 2% presencial no BH Resolve; BH SIM com 129 serviços | **Confere** | [jpg](./capturas/2026-11-20_pbh_noticia_2026-10-05.jpg) |
| SYDLE ONE: BPM, CRM e Service Desk | [www.sydle.com/br](https://www.sydle.com/br/) | Título da página: "SYDLE ONE \| Plataforma de BPM, ECM, CRM, Service Desk e Billing."; subtítulo "Plataforma digital corporativa all-in-one" | **Confere** (a página lista também ECM e Billing) | [jpg](./capturas/2026-11-20_sydle_home.jpg) |

**Observações para a proposta (sem alterá-la aqui):**
1. **Números de datas diferentes:** 05/10/2026 → 1.492 catalogados / 1.118 solicitáveis; 18/08/2026 → 1.489 / 903; 27/12/2023 → 1.387 / 936. Citar sempre com a data da fonte; não misturar.
2. **Título citado de forma diferente:** a lista de fontes da proposta cita "amplia em mais de 500 serviços digitais"; o título real é "amplia em **mais de 500%** serviços digitais". Provável erro de digitação (faltou o "%"); corrigir com registro.
3. **Natureza das fontes:** todos os números de impacto vêm da **própria PBH** (autodeclarados), e a eleição é um ranking de uma empresa privada (Melhores.com), de metodologia não verificada. Não há fonte independente para o volume de uso.
4. As notícias foram lidas na parte visível após rolagem curta; trechos não exibidos não foram lidos.
5. A SYDLE foi aberta sem aceitar cookies; o banner de cookies não foi respondido.

**Resultado:** as cinco fontes foram conferidas em 20/11/2026 e os números da proposta correspondem ao que as páginas mostram.
