# LAB05 — Usabilidade e acessibilidade do Portal de Serviços da PBH

Laboratório de Experimentação de Software · Engenharia de Software · PUC Minas (Campus Lourdes, noite, 2026/2) · Professor: Danilo Maia
Atualizado em **23/11/2026** · Sprint atual: **S01 (Proposta)**

> **Leia primeiro:** [FONTE_DA_VERDADE.md](./FONTE_DA_VERDADE.md). Ela é a referência central do projeto: o que o professor exige, o que foi decidido, o que já foi feito e o que falta.

## O que é o projeto

Experimento com pessoas comparando **celular × computador** no [Portal de Serviços da PBH](https://servicos.pbh.gov.br) (plataforma SYDLE ONE), mais uma auditoria de acessibilidade (WCAG) com axe DevTools e Lighthouse.

- **Pergunta:** o cidadão encontra e inicia um serviço com a mesma eficácia, eficiência e satisfação no celular e no computador?
- **Amostra planejada:** 32 participantes analisáveis, 8 por sequência de contrabalanceamento.
- **Importante:** hoje existe **só planejamento**. Não há coleta nem resultado. Nenhum número de estimativa (como o poder estatístico) é resultado.

## Regras do grupo (leia antes de mexer em qualquer coisa)

1. **Sem crawler nem varredura** no Portal. Navegação manual e uso pontual. O robots.txt do Portal tem `Disallow: /`.
2. **Sem teste de carga** em sistema de terceiros. No máximo 1 requisição por segundo.
3. **Sem login, sem formulário enviado, sem dado pessoal** nos testes com o Portal.
4. **Não inventar** números, fontes, aprovações ou resultados. O que não foi comprovado fica como pendência.
5. **Não commitar** HTML completo do Portal: ele contém tokens de autorização. Só os trechos já redigidos em `docs/evidencias/capturas/`.
6. Antes de mudar uma decisão metodológica, registre o motivo na [FONTE_DA_VERDADE.md](./FONTE_DA_VERDADE.md) §19.

## O que precisa ser feito agora (issue #16: critérios do software)

Issue: [#16 — Critérios do software: real, em operação e alto impacto](https://github.com/Laboratorio-Medicao/Lab05/issues/16) (parte da #15).

| Pendência | O que fazer | Quem | Situação |
|---|---|---|---|
| P7 — HTML da página inicial | Registrar como o HTML foi obtido | Marcos | **Encerrada** |
| P8 — Termos de uso | Ler e registrar os termos do Portal | Marcos | **Encerrada** (Política de Privacidade ainda não lida) |
| P9 — Habitantes de BH (IBGE) | Conferir o número no IBGE Cidades | Marcos | **Encerrada** (2.315.560, Censo 2022) |
| **P10 — Pedido via LAI** | **Enviar o pedido à PBH, guardar o protocolo e registrar** | **Arthur** | **Enviada em 22/11/2026** (protocolo a anexar depois) |
| Fontes das notícias da PBH e da SYDLE | Abrir cada fonte, anotar URL, data de acesso e o trecho com o número | Marcos | **Encerrada** (5 fontes conferidas em 20/11/2026) |

### Para o Arthur

@ALuiz19 — **Arthur, a P10 é sua.**

1. Abra [docs/evidencias/P10_pedido_LAI_instrucoes.md](./docs/evidencias/P10_pedido_LAI_instrucoes.md). Tem o passo a passo e o **texto do pedido pronto para copiar e colar**.
2. Envie o pedido pelo canal de LAI da PBH (o Portal tem um cartão "Lei de Acesso à Informação – LAI").
3. Se pedir login gov.br, use a **sua própria conta** e não compartilhe senha nem códigos.
4. Guarde o **número do protocolo** e uma captura da tela (sem CPF nem dados sensíveis) em `docs/evidencias/capturas/`.
5. Preencha a tabela da seção 5 do arquivo e avise o grupo.

Para a issue #16 basta o **protocolo**; a resposta da PBH pode chegar depois (prazo legal: 20 dias, prorrogáveis por 10).

## Dependem do professor (o grupo precisa levar a pergunta)

Nada disso foi respondido. Todas seguem **abertas** e não devem ser tratadas como aprovadas.

| Pendência | Pergunta ao professor |
|---|---|
| P12 | Pode usar axe DevTools e Lighthouse, acionados manualmente, apesar do `Disallow: /` do Portal? (informar que a leitura dos termos foi feita por assistente de IA no navegador de um integrante, com autorização dele) |
| P11 | Precisa de comitê de ética? |
| P1 | Como tratar o tempo da tarefa abandonada antes de 300 s ou encerrada por pedido de ajuda? |
| P2 | A regra provisória de fechamento dos blocos (8 por sequência) está ok? |
| P3 | Haverá critério de exclusão por proporção de tarefas no teto de 300 s? |

## Dependem do grupo

| Pendência | Decisão |
|---|---|
| P4 | O teste exploratório proposto para a RQ4 (Wilcoxon pareado por participante sobre a diferença na taxa de erro por passo alcançado, com permutação de sinais como sensibilidade) está adequado? |
| P5 | Faremos a conversão do impacto em horas? |
| P6 | Qual o n mínimo abaixo de 32? |
| P13 | Datas reais de S02, S03 e entrega final (do cronograma da disciplina) |
| P14 | Link do repositório e do GitHub Projects; confirmar nomes dos integrantes |

## Como o repositório está organizado

```
Lab05/
├── README.md                 ← você está aqui
├── FONTE_DA_VERDADE.md       ← referência central (leia primeiro)
├── requirements.txt          ← versões fixadas (numpy, scipy, pandas, matplotlib, pytest)
├── dados/
│   ├── dicionario_de_dados.md ← PROPOSTA, a confirmar com o papel B
│   └── sinteticos/           ← dados FALSOS (SINTETICO_*), só para testar o código
├── scripts/
│   ├── esquema.py            ← dicionário em código (colunas, domínios, sequências)
│   ├── validar_dados.py      ← validador dos dados
│   ├── analise.py            ← RQ1–RQ4, Holm, checagem de ordem, auditoria Q4
│   └── gerar_dados_sinteticos.py
├── notebooks/
│   └── analise_S02.py        ← notebook em formato percent (# %%)
├── tests/                    ← pytest
└── docs/
    ├── enunciado/            ← enunciado oficial do professor (PDF)
    ├── proposta/             ← proposta metodológica S01 (versão final)
    ├── relatorios/           ← relatório de fechamento da S01
    └── evidencias/           ← evidências dos critérios do software
        ├── S01_criterios_do_software.md   ← registro principal (issue #16)
        ├── P10_pedido_LAI_instrucoes.md   ← instruções do pedido LAI
        └── capturas/                      ← capturas e trechos arquivados
```

Pastas previstas para quando houver conteúdo: `dados/brutos/` (coleta real, imutável), `instrumentos/`, `resultados/` (só saídas de dados reais).

## Como rodar a análise (issue #25)

> **Hoje só existem dados sintéticos. Nada do que estes comandos produzem é resultado.**

```bash
pip install -r requirements.txt
python scripts/gerar_dados_sinteticos.py                 # (re)gera dados/sinteticos/ (semente 20261117)
python scripts/validar_dados.py dados/sinteticos         # relatório de validação; saída 1 se houver erro
python scripts/analise.py dados/sinteticos --saida <pasta temporária>
python notebooks/analise_S02.py                          # ou abra no VS Code como notebook (células # %%)
python -m pytest
```

- Opções da análise: `--p1 {teto_300,tempo_registrado,excluir_tarefa}` e `--p2 {p2_provisoria,todos_analisaveis,blocos_completos_por_id}` (as primárias estão marcadas **PENDENTE** até o professor decidir P1 e P2; as demais saem como sensibilidade) e `--sem-teste-rq4` (se o professor recusar o teste da RQ4, P4).
- A análise recusa misturar dado real e sintético e nunca grava saída sintética em `resultados/`. Sem `--saida`, sintético vai para `dados/sinteticos/saida/`.
- Com dados reais: `dados/brutos/` + `dados/CHECKSUMS.sha256`, validar, conferir por segunda pessoa (FONTE_DA_VERDADE §2.3) e só então rodar `python scripts/analise.py dados/brutos` (saída em `resultados/`).

## Lacunas conhecidas (para ninguém se surpreender)

- O script de poder estatístico (`power_analysis.py`) e o `results_v3_2.json`, citados na proposta, **não estão no repositório**.
- O piloto (3 participantes), o termo de consentimento e a planilha de observação **ainda não existem**.
- Os nomes dos integrantes e os papéis A/B/C **não estão confirmados** na documentação.
- O dicionário de dados é **proposta do papel C** e ainda não foi confirmado com o papel B; o formato do export do axe DevTools precisa ser conferido com um arquivo real.
- A análise (issue #25) foi rodada **só com dados sintéticos**: não há resultado. P1, P2 e P4 seguem pendentes com o professor.
- Não há `.gitignore`: `__pycache__/`, `.pytest_cache/` e `dados/sinteticos/saida/` não devem ser commitados.

## Próximas etapas

| Etapa | Conteúdo | Data |
|---|---|---|
| S01 | Proposta, evidências do software, piloto | A confirmar (P13) |
| S02 | Coleta (32 sessões analisáveis), auditoria, análise | A confirmar (P13) |
| S03 | Impacto, 7 categorias revisadas, conclusões, rascunhos | A confirmar (P13) |
| Final | Documento e apresentação de 10 minutos | A confirmar (P13) |
