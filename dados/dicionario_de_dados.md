# Dicionário de dados — LAB05

> **PROPOSTA do papel C (Análise), a confirmar com o papel B (Instrumentação e Operação, Guilherme).** Criada em 23/11/2026 na issue #25. Nada aqui foi acordado com quem vai coletar: nomes de colunas, códigos e regras podem mudar. Quando mudar, atualizar junto `scripts/esquema.py` (versão executável deste dicionário) e os testes.
>
> **Não existe dado coletado.** Os únicos dados do repositório são **sintéticos** (`dados/sinteticos/`, prefixo `SINTETICO_`, coluna `origem = sintetico`), feitos só para testar o código. **Nada é resultado** (FONTE_DA_VERDADE §2.3).

Fontes do desenho: FONTE_DA_VERDADE §5.2, §6, §8 e §9; Proposta §3, §4, §6 e §7.

## 1. Organização das pastas

| Caminho | Conteúdo | Regra |
|---|---|---|
| `dados/brutos/` | Tabelas reais anonimizadas (`participantes.csv`, `sessoes.csv`, `sus.csv`, `catalogo_passos.csv`, `passos.csv`) e `auditoria/` | **Imutável** depois do commit: correção entra como novo arquivo ou nova versão, com registro na FONTE_DA_VERDADE §19 |
| `dados/brutos/auditoria/` | `indice.csv`, `axe/*.json`, `lighthouse/*.json` exportados manualmente | JSON exatamente como exportado (sem editar) |
| `dados/CHECKSUMS.sha256` | `sha256  caminho` de cada bruto, caminho relativo a `dados/` (ex.: `brutos/sessoes.csv`) | Gerado ao versionar os brutos; o validador confere |
| `dados/sinteticos/` | Mesmas tabelas com prefixo `SINTETICO_` e `SINTETICO_CHECKSUMS.sha256` | Só dado falso; **nunca** gravar em `resultados/` |
| `resultados/` | Saídas da análise de **dados reais** | Criada só quando houver coleta |

Formato: CSV UTF-8, separador vírgula, cabeçalho na 1ª linha, decimal com ponto, booleanos como `0`/`1`, datas `AAAA-MM-DD`, texto vazio = célula vazia.

## 2. Regras gerais

- **Sem dado pessoal.** Nenhuma coluna de nome, e-mail, telefone, CPF, RG, endereço, contato, data de nascimento. O validador recusa colunas com esses nomes e procura padrões de e-mail, CPF e telefone nos textos livres.
- **Código do participante** `P\d\d` (P01, P02, …), atribuído na sessão, sem tabela de correspondência com nome no repositório.
- **Origem:** toda tabela tem a coluna `origem` com `real` ou `sintetico`. É proibido misturar: o validador e a análise recusam conjunto com as duas origens, e a origem precisa bater com o nome do arquivo (prefixo `SINTETICO_` ⇔ `sintetico`).
- **Diferenças** na análise são sempre **celular − computador**, por participante.
- Passar no validador **não** torna o dado "Verificado": isso exige conferência por segunda pessoa, com registro (FONTE_DA_VERDADE §2.3).

## 3. `participantes.csv` (1 linha por pessoa que teve sessão, inclusive piloto e sessões inválidas)

| Coluna | Tipo | Domínio / regra |
|---|---|---|
| `participante` | texto | `P\d\d`, único |
| `sequencia` | inteiro | 1 = celular-A/computador-B; 2 = celular-B/computador-A; 3 = computador-A/celular-B; 4 = computador-B/celular-A (FDV §6.3) |
| `bloco` | inteiro ≥ 1 | Bloco sorteado de 4 em que a pessoa foi alocada; reposição fica no mesmo bloco e sequência |
| `ordem_realizacao` | inteiro ≥ 1 | Ordem cronológica das sessões, única; usada pela regra P2 ("8 primeiros por sequência") |
| `data` | data | `AAAA-MM-DD` da sessão |
| `faixa_etaria` | categoria | `18-24`, `25-34`, `35-44`, `45-59`, `60+` (faixas **a confirmar** com o questionário do papel B) |
| `uso_previo_portal` | categoria | `nunca`, `raramente`, `as_vezes`, `frequentemente` (a confirmar) |
| `familiaridade_digital` | inteiro | 1–5, autoavaliação (a confirmar) |
| `valida` | 0/1 | 0 = sessão inválida (falha técnica, interrupção); entra só na descrição |
| `motivo_invalida` | texto | Obrigatório se `valida = 0` |
| `reposto_por` | texto | Código de quem repôs a sessão inválida; precisa existir e estar na **mesma sequência** |
| `piloto` | 0/1 | 1 = piloto (3 pessoas), nunca entra na análise final |
| `hash_ui_package` | texto | Hash(es) `ui-package` observados na sessão (ver `docs/evidencias/S01_criterios_do_software.md` §2.1) |
| `versao_chrome` | texto | Versão do Chrome usada |
| `versao_portal_obs` | texto | Outras marcas de versão observadas (ex.: `window.SYDLE.app.hash`) |
| `o_que_mais_atrapalhou` | texto livre | Resposta aberta; **triada contra dado pessoal** antes do commit |
| `notas_moderador` | texto livre | Idem |
| `origem` | categoria | `real` ou `sintetico` |

Analisável = `valida = 1` e `piloto = 0`. Meta: 8 analisáveis por sequência; o validador avisa quando há falta ou excedente.

## 4. `sessoes.csv` (1 linha por tarefa: 6 por participante válido)

| Coluna | Tipo | Domínio / regra |
|---|---|---|
| `participante` | texto | Existe em `participantes.csv` |
| `dispositivo` | categoria | `celular`, `computador` |
| `conjunto` | categoria | `A`, `B`; coerente com a sequência |
| `periodo` | inteiro | 1 = primeiro dispositivo, 2 = segundo; coerente com a sequência |
| `tarefa_id` | texto | `A1`–`A3`, `B1`–`B3` (letra = conjunto). Mapa código → tarefa real a definir após o piloto |
| `ordem_tarefa` | inteiro | 1–3, ordem sorteada dentro do conjunto |
| `concluida` | 0/1 | 1 ⇔ `motivo_fim = concluida` |
| `tempo_s` | decimal | (0, 300]; `tempo_s = 300` ⇔ `motivo_fim = teto`. Cronômetro conforme FDV §6.3 |
| `motivo_fim` | categoria | `concluida`, `teto`, `abandono`, `ajuda`, `falha_tecnica` |
| `pediu_ajuda` | 0/1 | 1 ⇒ não concluída; `motivo_fim = ajuda` ⇒ 1 |
| `erros` | inteiro ≥ 0 | Total de erros da tarefa (clique em caminho errado, volta, busca refeita) = soma de `n_erros` em `passos.csv`, inclusive `fora_do_caminho` |
| `seq` | inteiro | SEQ pós-tarefa, 1–7 |
| `origem` | categoria | `real` ou `sintetico` |

Regras extras: participante válido tem exatamente 3 tarefas distintas por dispositivo, com `ordem_tarefa` 1, 2 e 3. `falha_tecnica` só pode aparecer em sessão inválida (`valida = 0`), que é reposta (regra P2, item 1).

**Tempo de abandono e de pedido de ajuda antes de 300 s (P1, pendente):** o moderador registra o tempo transcorrido no evento. A análise tem três variantes fixadas antes da coleta (`teto_300` provisória; `tempo_registrado` e `excluir_tarefa` como sensibilidade) até o professor decidir.

## 5. `sus.csv` (2 linhas por participante válido: uma por dispositivo)

| Coluna | Tipo | Domínio / regra |
|---|---|---|
| `participante`, `dispositivo` | texto | Par único |
| `item_1` … `item_10` | inteiro | 1–5, na ordem do questionário SUS em português (versão validada a registrar) |
| `origem` | categoria | `real` ou `sintetico` |

O escore **não** é digitado: o script calcula (ímpares x − 1, pares 5 − x, soma × 2,5).

## 6. `catalogo_passos.csv` (1 linha por passo previsto de cada tarefa, por dispositivo)

**Congelado com commit antes do cruzamento com os erros** (RQ4): o validador imprime um hash do catálogo para citar na mensagem do commit de congelamento. O rótulo é por dispositivo porque o layout é responsivo.

| Coluna | Tipo | Domínio / regra |
|---|---|---|
| `tarefa_id` | texto | Igual a `sessoes.csv` |
| `passo_id` | texto | Identificador do passo no caminho previsto (ex.: `p1`…`pN`); `fora_do_caminho` é reservado e não entra aqui |
| `dispositivo` | categoria | `celular`, `computador` |
| `pagina_url` | texto | Página do passo (a mesma do índice da auditoria) |
| `elemento` | texto | Elemento usado no passo (campo, botão, link, região), descrito ou seletor |
| `rotulo_wcag` | categoria | `com_violacao`, `sem_violacao_detectada` (= não detectada por axe nem checklist manual; nunca "sem violação"), `indeterminado` |
| `regras_axe` | texto | Regras violadas **no elemento**, separadas por `;`; violação só do checklist manual entra como `manual:<critério WCAG>`. Obrigatório se `com_violacao` |
| `motivo_indeterminado` | texto | Obrigatório se `indeterminado` |
| `origem` | categoria | `real` ou `sintetico` |

Chave única: (`tarefa_id`, `passo_id`, `dispositivo`).

## 7. `passos.csv` (1 linha por participante × tarefa × passo do catálogo)

| Coluna | Tipo | Domínio / regra |
|---|---|---|
| `participante`, `dispositivo`, `tarefa_id` | texto | Iguais a `sessoes.csv` |
| `passo_id` | texto | Existe no catálogo para a tarefa e o dispositivo, ou `fora_do_caminho` |
| `alcancado` | 0/1 | O participante chegou ao passo |
| `n_erros` | inteiro ≥ 0 | Erros registrados no passo; > 0 exige `alcancado = 1` |
| `origem` | categoria | `real` ou `sintetico` |

**Erro fora do caminho previsto:** registrado em uma linha com `passo_id = fora_do_caminho` (e `alcancado = 1`). Conta no total de erros da tarefa, mas **não** entra na RQ4; a análise reporta quantos foram.

Na RQ4 (exploratória), por participante: taxa = erros ÷ passos alcançados, em passos com violação e sem violação detectada, dispositivos somados, indeterminados e `fora_do_caminho` fora; entra quem alcançou ≥ 1 passo em cada grupo.

## 8. Auditoria (Q4 e rótulos da RQ4)

`auditoria/indice.csv` (sintético: `SINTETICO_indice.csv`), 1 linha por JSON exportado:

| Coluna | Tipo | Domínio / regra |
|---|---|---|
| `arquivo` | texto | Caminho relativo a `auditoria/` (ex.: `axe/inicio_mobile.json`) |
| `pagina_url` | texto | Página auditada |
| `data` | data | `AAAA-MM-DD` |
| `versao_chrome` | texto | Versão do Chrome |
| `ferramenta` | categoria | `axe`, `lighthouse` |
| `modo` | categoria | `mobile`, `desktop` |
| `execucao` | inteiro | 1–3 (Lighthouse: 3 execuções por página e modo; axe: 1) |
| `origem` | categoria | `real` ou `sintetico` |

Formatos aceitos pelo leitor (`analise.normalizar_axe`):

1. **axe-core JSON** (objeto com `violations`, cada uma com `id`, `impact`, `tags`, `nodes`) — formato principal;
2. lista de objetos no formato 1;
3. export da extensão **axe DevTools** com `allIssues` (ou `issues`), um item por nó, com `ruleId` e `impact`. **Este formato foi inferido e precisa ser conferido com um export real no piloto.**

Lighthouse: JSON padrão do relatório (`categories.accessibility.score`, `audits["largest-contentful-paint"].numericValue` em ms, `audits["cumulative-layout-shift"].numericValue`).

Contagem: "por regra" = 1 por regra violada na página; "por nó" = soma dos elementos afetados. Top 10 só com tags WCAG (`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`); `best-practice` aparece à parte. Nota Lighthouse é ordinal (mediana/distribuição). LCP e CLS: mediana das 3 execuções no modo mobile.

A auditoria depende do aceite do professor (P12) e do limite de 1 requisição/segundo (D3).

## 9. Pendências deste dicionário

- Confirmar com o papel B: nomes de colunas, faixas do questionário, como a planilha de observação registra o passo do erro, e quem preenche `catalogo_passos.csv`.
- Confirmar o formato real do export do axe DevTools (formato 3 acima).
- P1 (tempo de abandono/ajuda), P2 (fechamento) e P4 (teste da RQ4) seguem com o professor.
