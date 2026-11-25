# Verificação do pipeline por reexecução do zero (issue #38)

## Quem verificou

A verificação foi feita por um **agente de IA (Claude Sonnet)**, a pedido do Arthur, na sessão de 25/11/2026. **Não** foi feita por um integrante do grupo. A FONTE_DA_VERDADE §2.3 aceita "segunda pessoa/ferramenta, com registro"; este arquivo é o registro. Quem quiser reforçar a verificação pode repetir os passos abaixo em outra máquina.

Ponto de partida: commit `d87eedd`, em uma worktree nova (`issue-38-verificacao`), com venv novo e sem nenhuma saída gerada na pasta.

## Ambiente

| Item | Valor |
|---|---|
| Sistema | Windows 11 Pro (10.0.26300), Git Bash |
| Python | 3.12.10 |
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| scipy | 1.16.3 |
| matplotlib | 3.11.2 |
| pytest | 9.1.1 |

Versões tiradas de `pip freeze` após `pip install -r requirements.txt`.

## Passos executados

Na raiz da worktree, no Git Bash:

1. `python3.12 -m venv .venv` (comando do README): **falhou**, `python3.12: command not found`. Desvio: `py -3.12 -m venv .venv`. **Achado:** o README só tem comandos Unix.
2. `source .venv/bin/activate` (README): **falhou**, o arquivo não existe no Windows. Desvio: `source .venv/Scripts/activate`.
3. `pip install -r requirements.txt`: sem problemas.
4. `python -m pytest -q` (antes das correções): **1 falha, 54 passaram.**
   - `test_resumo_so_tem_numeros_calculados`: `read_text()` sem `encoding` lê em cp1252 no Windows e quebra os acentos do `resumo.md` (UTF-8).
   - `test_intervalo_minimo_entre_requisicoes`, já conhecido por falhar de vez em quando, **passou** nesta rodada.
5. Correções (achados da verificação, ambas fora do README):
   - `scripts/coleta.py`: causa: a resolução de 15,625 ms de `time.monotonic()` no Python 3.12/Windows fazia o intervalo real ficar até ~16 ms abaixo do pedido. Correção: relógio `time.perf_counter()` mais um laço de reconferência (dorme enquanto `perf_counter() - self._ultima < self.intervalo_s`). O intervalo (1 s) e o user-agent não mudaram. Testes novos: `test_intervalo_minimo_mesmo_com_sleep_curto` (simula `sleep` acordando 20 ms antes) e `test_intervalo_real_medido_com_relogio_de_alta_resolucao` (mede os intervalos com `perf_counter` e intervalo de 0,25 s, múltiplo exato de 15,625 ms). Ambos falhavam antes da correção (o segundo, 5 de 5 rodadas, com mínimo medido de 0,239 a 0,242 s) e passam depois.
   - `tests/test_pipeline.py`: 6 chamadas `read_text()` passaram a `read_text(encoding="utf-8")`.
6. `python -m pytest -q` repetido 5 vezes, sem `PYTHONUTF8`: **57 passed** nas 5 rodadas.
7. `python scripts/pipeline.py --cache-dir "$HOME/.cache/lab05"`, início às 03:03:53 UTC (00:03:53 local), com download real do CKAN.

## Resultados

| Item | Resultado |
|---|---|
| pytest antes das correções | 54 passed, 1 failed |
| pytest depois (5 rodadas) | 57 passed em todas |
| Duração total do pipeline | 9 min 14 s |
| Download (10 CSVs, 1 req/s) | cerca de 8 min 20 s (estimado pelo horário de gravação do último CSV) |
| Tratamento, análise e gráficos | cerca de 50 s |
| Registros na base analítica | 1.480.736 (igual ao esperado) |
| SHA-256 dos 10 CSVs vs. `d87eedd` | **iguais** (`recursos[*].sha256`) |
| `sha256_base_analitica` vs. `d87eedd` | **igual** |

Como os 10 CSVs têm o mesmo SHA-256 do commit, a PBH não republicou os arquivos desde a execução original.

CSVs brutos mantidos em `~/.cache/lab05` (fora do repositório) para o #39; apagar ao final.

Observação: o download real foi feito com a primeira versão da correção (laço com `time.monotonic()`); a troca para `perf_counter` veio depois, na revisão. O efeito possível naquela execução é de até ~16 ms abaixo de 1 s em alguns intervalos.

## Diferenças nas saídas

Comparação das saídas regeneradas com as versionadas em `d87eedd`:

| Arquivo | Diferença | Classificação |
|---|---|---|
| `resultados/tabelas/*.csv` | nenhuma | idêntico |
| `resultados/resumo.md` | nenhuma | idêntico |
| `dados/manifesto_coleta.json` | `gerado_em_utc` e, em cada recurso, os campos de origem: `origem: pasta_local` virou URL, id, nome, `tamanho_declarado`, `ultima_modificacao` e `do_cache`; o dataset ganhou título, licença, `metadata_modified`, mantenedor e periodicidade. `bytes`, `sha256` e `sha256_base_analitica` iguais | esperada (a execução original usou pasta local, esta usou download) |
| `dados/qualidade_dados.json` | só fim de linha; o conteúdo JSON é igual (`==` após carregar) | esperada, sem diferença de dados |
| `resultados/resultados.json` | 41 números de ponto flutuante diferem na última casa (p-valores e p-valores de Holm da análise estratificada por par). Maior diferença absoluta: 2,8e-16; maior diferença relativa: 4,3e-15. Nenhum valor não numérico, chave ou contagem diferiu | (a) arredondamento na última casa, por versão de pacote/plataforma |
| `resultados/figuras/04_distribuicao_tempos.png` e `resultados/painel.html` | PNG com 22 bytes a menos (68.956 para 68.934); o painel difere só pela imagem embutida dessa figura | (a) renderização do matplotlib; as tabelas e o JSON de resultados não mudam de conclusão |

Nenhuma diferença real (classe b) foi encontrada. As saídas regeneradas foram restauradas com `git checkout -- resultados dados` e **não** entram no commit.

## Conclusão

**Reproduzido com ressalvas.** O pipeline roda do zero e gera os mesmos 1.480.736 registros, os mesmos SHA-256 e as mesmas tabelas. Ressalvas:

- no Windows, o README precisa de comandos próprios (venv e ativação); foi acrescentada uma linha de Windows (Git Bash);
- havia duas falhas de portabilidade nos testes e na espera de 1 req/s, corrigidas nesta issue (57 testes passando);
- 41 números de `resultados.json` mudam na última casa decimal (até 4,3e-15 em termos relativos), o que não altera nenhuma conclusão;
- a verificação foi feita por um agente de IA, não por um integrante.
