# Formulários SUS e SEQ — LAB05

> **Pendência:** o texto dos 10 itens do SUS abaixo é a versão em português usada no Brasil (adaptação transliterada do SUS de Brooke), escrita de memória pelo assistente em 24/11/2026. **Conferir palavra por palavra com a fonte** (a adaptação transcultural em português) e registrar a referência na FONTE_DA_VERDADE §19 antes de usar em dado real. Escala e pontuação seguem `dados/dicionario_de_dados.md` §5.

Código do participante: P___  Dispositivo: ( ) celular ( ) computador

## SEQ (uma vez após cada tarefa, escala 1–7)

> "No geral, esta tarefa foi: 1 = muito difícil … 7 = muito fácil."

( )1 ( )2 ( )3 ( )4 ( )5 ( )6 ( )7  → coluna `seq` em `sessoes.csv`

## SUS (uma vez por dispositivo, após as 3 tarefas)

Responder de 1 (discordo totalmente) a 5 (concordo totalmente), pensando **neste dispositivo**:

| # | Item | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Eu acho que gostaria de usar esse sistema com frequência. | | | | | |
| 2 | Eu achei o sistema desnecessariamente complexo. | | | | | |
| 3 | Eu achei o sistema fácil de usar. | | | | | |
| 4 | Eu acho que precisaria de ajuda de uma pessoa com conhecimentos técnicos para usar o sistema. | | | | | |
| 5 | Eu acho que as várias funções do sistema estão muito bem integradas. | | | | | |
| 6 | Eu acho que o sistema apresenta muita inconsistência. | | | | | |
| 7 | Eu imagino que as pessoas aprenderiam como usar esse sistema rapidamente. | | | | | |
| 8 | Eu achei o sistema atrapalhado de usar. | | | | | |
| 9 | Eu me senti confiante ao usar o sistema. | | | | | |
| 10 | Eu precisei aprender várias coisas novas antes de conseguir usar o sistema. | | | | | |

→ colunas `item_1` … `item_10` em `sus.csv`. O escore **não** é calculado à mão: o script calcula (ímpares x − 1, pares 5 − x, soma × 2,5).
