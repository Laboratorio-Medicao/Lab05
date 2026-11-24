# Piloto S01 — checklist de execução e relatório (issue #19)

> **Estado: NÃO EXECUTADO.** Este arquivo é o kit de preparação. Nenhuma sessão foi feita; todos os campos de resultado abaixo estão em branco de propósito. Só marcar `[x]` com evidência (CSV preenchido, JSON exportado). Ver FONTE_DA_VERDADE §2.3 e D4.

Escopo (Proposta §9): 3 participantes, cada um nos dois dispositivos, mais auditoria de 3 páginas. **Não entram na análise final** (`piloto = 1`, `origem = real`).

## 0. Antes de marcar sessões — decisões que o piloto precisa fechar

Divergências encontradas entre o roteiro (`docs/sessao/roteiro-sessao.md`) e o dicionário (`dados/dicionario_de_dados.md`). Resolver **antes** da primeira sessão, senão a planilha não captura o que o roteiro pergunta:

| Item | Roteiro | Dicionário / esquema | Ação |
|---|---|---|---|
| Faixa etária | 18–24, 25–34, 35–44, 45–54, 55+ | `18-24`, `25-34`, `35-44`, `45-59`, `60+` | **Resolvido 24/11/2026:** roteiro alinhado ao dicionário |
| Uso prévio do Portal | Sim / Não | `nunca`, `raramente`, `as_vezes`, `frequentemente` | **Resolvido:** roteiro alinhado |
| Familiaridade | Baixa / Média / Alta | inteiro 1–5 | **Resolvido:** roteiro alinhado |
| Versão do Portal | não registrada no roteiro | `hash_ui_package`, `versao_chrome`, `versao_portal_obs` | **Resolvido:** passo incluído na preparação do roteiro |
| Passo do erro | "registrar em qual passo" | `passos.csv` exige `catalogo_passos.csv` congelado | Montar catálogo dos 6 caminhos **durante** o piloto |
| Escala SEQ/SUS | "aplicar" | SEQ 1–7; SUS 1–5, 10 itens | **Criados** em `formularios-sus-seq.md`; texto do SUS a conferir com a fonte |
| Sequência/bloco | "consultar alocação" | `sequencia` 1–4, `bloco`, `ordem_realizacao` | Tabela de alocação do piloto (abaixo) |

## 1. Preparação

- [ ] Roteiro, tarefas A/B e termo revisados pelo grupo (issue #18, merge #33)
- [x] Formulários SUS e SEQ escritos (`formularios-sus-seq.md`); [ ] conferir texto do SUS com a fonte; [ ] imprimir
- [ ] Planilhas: copiar `modelo_*.csv` para uma pasta **fora do git** durante a coleta
- [ ] Celular Android + Chrome; computador ≥ 1366×768 + Chrome; anotar versões
- [ ] Cronômetro; sala; gravação de tela só com consentimento no termo
- [ ] ~~3 voluntários de fora~~ **Dispensado (decisão do Marcos, 24/11/2026):** não há como recrutar. Os 3 participantes do piloto serão integrantes do grupo ou conhecidos já à mão; ver desvio no §9
- [ ] Alocação do piloto (uma sequência diferente por pessoa, FDV §6.3):

| Participante | Sequência | 1º dispositivo / conjunto | 2º dispositivo / conjunto | Data | Moderador |
|---|---|---|---|---|---|
| P01 | 1 | celular-A | computador-B | | |
| P02 | 2 | celular-B | computador-A | | |
| P03 | 3 | computador-A | celular-B | | |

(Sequência 4 = computador-B/celular-A não é coberta por 3 pessoas; registrar que o piloto não cobre os 4 braços.)

## 2. Objetivos do piloto e critério de decisão

| Objetivo (issue #19) | Como medir | Critério sugerido (**a confirmar com o grupo**, não vem da proposta) | Resultado |
|---|---|---|---|
| Dificuldade parecida entre A e B | Taxa de conclusão, mediana de `tempo_s`, SEQ por conjunto, nos 3 participantes | Nenhum conjunto com diferença grande e sistemática; com n=3 é só indício, não teste | |
| Nenhuma tarefa exige login | Cada uma das 6 tarefas chega à tela-alvo sem tela de login gov.br | 6/6 sem login. Se alguma exigir, trocar a tarefa e registrar | |
| Sessão cabe em 30 min | Cronometrar a sessão inteira (boas-vindas → encerramento) | ≤ 30 min nas 3 sessões; senão cortar/encurtar etapa | |
| Planilha captura tudo | Preencher as 5 tabelas de verdade e rodar `scripts/validar_dados.py` | Validador sem erro; nada que o moderador quis anotar ficou sem coluna | |

Registrar também: tela-alvo real de cada tarefa (URL), ocorrências de falha técnica, dúvidas sobre o enunciado das tarefas, itens do roteiro que o moderador teve que improvisar.

### Tela-alvo observada por tarefa (preencher no piloto)

| Tarefa | URL da tela-alvo | Exige login? | Caminho previsto (passos) | Observações |
|---|---|---|---|---|
| A1 poda de árvore | | | | |
| A2 buraco na via | | | | |
| A3 alvará de obra | | | | |
| B1 segunda via IPTU | | | | |
| B2 iluminação pública | | | | |
| B3 licença para evento | | | | |

## 3. Execução (por sessão)

- [ ] P01 feita — tempo total: ___ min — válida? ___
- [ ] P02 feita — tempo total: ___ min — válida? ___
- [ ] P03 feita — tempo total: ___ min — válida? ___

## 4. Auditoria de 3 páginas

Limite de 1 requisição/segundo (D3). **Depende do aceite do professor (P12)** — não rodar antes. Páginas sugeridas (a confirmar): inicial + 2 telas-alvo do piloto.

- [ ] Aceite do professor registrado
- [ ] axe: 3 páginas × (mobile, desktop) — JSON exportado sem edição
- [ ] Lighthouse: 3 páginas × (mobile, desktop) × 3 execuções
- [ ] `indice_auditoria.csv` preenchido (`modelo_indice_auditoria.csv`)
- [ ] Export real do **axe DevTools** conferido contra o formato 3 do dicionário §8 (hoje só inferido)

## 5. Fechamento

- [ ] Dados reais em `dados/brutos/` (+ `CHECKSUMS.sha256`), com `piloto = 1`, sem dado pessoal; textos livres triados
- [ ] `python scripts/validar_dados.py` sem erro
- [ ] Relatório curto abaixo preenchido; decisões registradas na FONTE_DA_VERDADE §19
- [ ] Ajustes nas tarefas/roteiro/termo feitos e mergeados; conjuntos A/B definitivos declarados
- [ ] Issue #19 comentada com os resultados e fechada

## 6. Relatório do piloto (preencher depois)

**Data(s):** &nbsp; **Moderadores:** &nbsp; **Versão do Portal / Chrome:**

**Resultado por objetivo:** (ver §2)

**Mudanças feitas por causa do piloto:**

**Problemas não resolvidos / levar ao professor:**

**O piloto não prova:** dificuldade igual entre A e B (n=3); só detecta problema grosseiro.

---

## 7. Ensaio prévio de navegação (24/11/2026) — NÃO é dado do piloto

Feito pelo assistente (Claude em Chrome), no Chrome do Marcos, a pedido dele: uma aba, sem login, sem clicar em "Solicitar", sem formulário, poucas requisições. É só um teste do material; **não** conta como sessão, não vai para `dados/` e não substitui a verificação feita pelo moderador no piloto.

| Tarefa | O que se viu | Login? |
|---|---|---|
| B1 segunda via IPTU | Card "Guias - IPTU - Emissão" na página inicial abre `.../servicos+guias-iptu-emissao+5e838678d9521a26a96ee9d9`; página de serviço com botão "Solicitar" | Não até a página do serviço |
| A1 poda de árvore | Busca "poda de árvore" → 17 itens; 1º: "Árvore - Poda de Árvore em Passeios, Praças, etc." (`.../servicos+arvore-poda-de-arvore-em-passeios-pracas-etc+5e7a17e4d9521a26a9abf17a`). Texto: serviço só em logradouros públicos | Não |
| A2 buraco | Busca "buraco" → 27 itens; 1º: "Tapa-Buraco" (`.../tapaburaco`). Há ao lado "Via Pública - Recapeamento" (possível erro de caminho) | Não |
| A3 alvará de obra | Busca "alvará" → 248 itens, topo irrelevante (Extrato de Débitos, Alvará de Localização e Funcionamento, ISSQN). "alvará de obra" → 51 itens com **vários candidatos**: Licenciamento de Edificação/Alvará na Hora, Revalidação de Alvará de Construção, Comunicação de Início de Obra, Alvará/Dispensa para Execução de Obra em Logradouro Público, Licença de Demolição | Não verificado |
| B2 iluminação pública | Busca "iluminação" → 17 itens; topo com 3 serviços parecidos: "Luminária Apagada Durante a Noite", "Intermitente (Piscando)", "Quebrada ou Ausente". "Lâmpada queimada" cabe em mais de um | Não verificado (só a lista) |
| B3 licença para evento | Busca "evento" → 11 itens; 1º "Autorização de Evento", 3º "Consulta Prévia de Evento" (dois candidatos) | Não verificado (só a lista) |

**Achados para decidir antes do piloto:**
1. **A3 não tem tela-alvo única.** O roteiro diz "página do serviço de alvará de construção/reforma com lista de documentos", mas o Portal tem pelo menos 4 serviços plausíveis. Escolher uma tela-alvo e dizer ao moderador o que fazer se o participante parar em outra. Sem isso, a conclusão da A3 depende do julgamento de cada moderador.
2. A3 parece mais difícil que as demais (busca com 248 resultados): pode quebrar a equivalência A × B, que é objetivo do piloto.
3. O "Conteúdo" do serviço abre fechado (acordeão): o critério "visualiza os documentos exigidos" precisa dizer se expandir a seção é necessário.
4. O texto da página não é extraível por ferramenta de leitura de texto (conteúdo montado por JavaScript): o catálogo de passos precisa ser montado com navegação manual.
5. B2 e B3 também têm mais de um serviço plausível (ver tabela). Definir a tela-alvo única de A3, B2 e B3 e a regra para quando o participante parar em outra. Falta abrir as páginas de A3, B2 e B3 para conferir login.

## 8. Decisões tomadas em 24/11/2026 (a pedido do Marcos, que autorizou decidir)

Revisáveis pelo grupo e pelo Guilherme (papel B, dono da issue).

- **Telas-alvo únicas** definidas em `docs/sessao/tarefas-conjunto-a.md` e `-b.md`. As 6 páginas abriram sem login em 24/11/2026 (só a página do serviço; "Solicitar" não foi clicado).
- **B2 reescrita** ("apagada de noite") para casar com um único serviço do Portal.
- **A3:** conclusão exige expandir "Exigências do Serviço?"; outros serviços de alvará contam como erro de caminho.
- Questionário inicial do roteiro alinhado ao dicionário; roteiro agora manda registrar versão do Portal/Chrome.
- Continua pendente: recrutar 3 pessoas, executar as sessões, auditoria (aceite do professor), preencher os dados reais.

## 9. Desvio registrado: piloto sem participantes de fora

**O que mudou:** a Proposta §9 prevê 3 participantes que não repetem e não entram na análise final. Sem recrutamento externo, o piloto usa pessoas do grupo (ou quem estiver disponível). Eles continuam fora da análise final (`piloto = 1`).

**O que isso enfraquece (declarar no relatório):**
- Quem escreveu, testou ou explorou as tarefas já conhece os caminhos. Neste projeto, o Guilherme escreveu as tarefas e o Marcos navegou nas 6 telas-alvo em 24/11/2026. Se forem participantes, os tempos e a taxa de conclusão sairão otimistas e **não servem** para julgar se A e B têm dificuldade parecida nem se cabem em 30 min.
- Os objetivos "nenhuma tarefa exige login" e "planilha captura tudo" **continuam testáveis** com qualquer pessoa. Os objetivos "dificuldade parecida" e "30 min" ficam só como **indício fraco**.
- Quando houver escolha: usar quem **menos** viu as tarefas (o Arthur, se não participou do roteiro) e quem nunca usou o Portal. Registrar `uso_previo_portal` e se a pessoa conhecia as tarefas em `notas_moderador`.
- Outros colegas da disciplina ou da família, se algum aceitar, são melhores que o grupo, mesmo que não tenham sido "recrutados". Se aparecer alguém, usar.

**Levar ao professor (junto com P12):** o piloto foi feito sem participantes externos; só valida a mecânica (login, planilha, cronometragem), não a equivalência A × B.
