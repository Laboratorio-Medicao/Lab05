# LAB05 — Canais de atendimento da PBH: tempo e taxa de encerramento

Laboratório de Experimentação de Software · Engenharia de Software · PUC Minas (Campus Lourdes, noite, 2026/2) · Professor: Danilo Maia
Atualizado em **25/11/2026** · Metodologia **v3.0** (dados abertos; sem participantes)

> **Leia primeiro:** [FONTE_DA_VERDADE.md](./FONTE_DA_VERDADE.md) (referência central) e [docs/metodologia.md](./docs/metodologia.md).

## O que é o projeto

Análise **observacional** dos dados abertos de solicitações dos cidadãos de Belo Horizonte (BH Digital), por canal: Portal de Serviços, PBH APP, Telefone 156 e Presencial (BH Resolve).

**Pergunta:** para um mesmo serviço, o tempo de encerramento e a proporção de solicitações encerradas diferem conforme o canal?

- **Fonte:** [CKAN da PBH](https://ckan.pbh.gov.br/dataset/solicitacoes-dos-cidadaos-por-meio-dos-canais-de-atendimento-da-pbh), licença CC-BY.
- **Cobertura real: maio/2020 a julho/2023.** O dataset não tem 2024–2026.
- **Sem participantes, sem sessões, sem planilhas manuais.** A metodologia anterior (experimento com pessoas) foi descontinuada; ver [docs/arquivo/](./docs/arquivo/s01-metodologia-participantes/README.md).
- Resultado = **associação**, não causa. Encerrada não significa resolvida.

## Como reproduzir (um comando)

Requer Python 3.12 e acesso à internet (~400 MB de download).

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/pipeline.py
```

No Windows (Git Bash): `py -3.12 -m venv .venv && source .venv/Scripts/activate`.

Em ~8–9 min (download) + ~1 min (processamento) o pipeline: baixa os 10 CSVs pela API do CKAN (1 req/s) para uma pasta temporária **fora do repositório**,
descarta as colunas de endereço na leitura, gera a base anonimizada, analisa e produz os gráficos. Os CSVs brutos são apagados ao final.

| Variação | Comando |
|---|---|
| Guardar os CSVs para não baixar de novo (pasta fora do repo) | `python scripts/pipeline.py --cache-dir ~/.cache/lab05` |
| Usar CSVs já baixados (sem rede) | `python scripts/pipeline.py --entrada ~/pasta_com_csvs` |
| Só a análise, a partir da base pronta | `python scripts/pipeline.py --base dados/processados/solicitacoes_analiticas.csv.gz` |
| Outros parâmetros | `--horizonte-dias 90` `--min-celula 30` |
| Testes | `python -m pytest` |

O pipeline recusa pastas de CSV bruto dentro do repositório (os originais têm logradouro, número e coordenadas).

## Onde estão os resultados

| Saída | Caminho |
|---|---|
| Resumo (números gerados pelo código) | `resultados/resumo.md` |
| Painel interativo-estático (abra no navegador) | `resultados/painel.html` |
| Documento final (rascunho revisado) | `docs/documento_final.md` |
| Apresentação de 10 min (slides, roteiro e banco de perguntas) | `docs/apresentacao/` (abra `slides.html` no navegador) |
| Gráficos (PNG) | `resultados/figuras/` |
| Tabelas (CSV) | `resultados/tabelas/` |
| Todos os resultados em JSON | `resultados/resultados.json` |
| Manifesto da coleta (URLs, tamanhos, SHA-256) e relatório de qualidade | `dados/manifesto_coleta.json`, `dados/qualidade_dados.json` |
| Base analítica anonimizada (não versionada) | `dados/processados/solicitacoes_analiticas.csv.gz` |

## Estrutura

```
Lab05/
├── README.md · FONTE_DA_VERDADE.md · requirements.txt
├── scripts/
│   ├── config.py         ← fonte, mapa de canais, lista branca de colunas, parâmetros
│   ├── coleta.py         ← download via API do CKAN (1 req/s, fora do repo)
│   ├── tratamento.py     ← leitura, anonimização, normalização, classificação
│   ├── estatistica.py    ← métricas, testes, tamanhos de efeito, Holm
│   ├── visualizacao.py   ← gráficos e painel HTML
│   └── pipeline.py       ← orquestra tudo (ponto de entrada)
├── tests/                ← pytest, só com dados sintéticos (tests/sintetico.py)
├── dados/                ← dicionário, manifesto, qualidade (e base processada, ignorada pelo git)
├── resultados/           ← saídas do pipeline com dados reais
└── docs/
    ├── metodologia.md    ← problema, GQM, métricas, análise, 7 categorias, ameaças
    ├── enunciado/        ← enunciado oficial (PDF)
    ├── evidencias/       ← critérios do software (real / em operação / alto impacto)
    └── arquivo/          ← metodologia anterior, DESCONTINUADA (só histórico)
```

## Regras do grupo

1. **Nunca** versionar CSV bruto da PBH (tem endereço e coordenadas) nem colunas de localização.
2. Respeitar o limite de 1 requisição por segundo ao CKAN (já implementado) e identificar o acesso (user-agent).
3. **Não inventar** números, fontes, aprovações ou resultados; o que não foi comprovado fica como pendência.
4. Qualquer mudança em horizonte, mínimo por célula, definições ou testes é decisão metodológica: registrar na [FONTE_DA_VERDADE](./FONTE_DA_VERDADE.md) §19.
5. Não interpretar as "situações" de atendimento nem os canais "Integração entre Sistemas"/"Origem Interna" além do que a PBH documenta.

## Pendências principais (detalhes na FONTE_DA_VERDADE §14)

| ID | Pendência | Quem |
|---|---|---|
| P15 | Professor aprovar a mudança de metodologia (dados abertos no lugar de participantes) | Grupo leva ao professor |
| P16 | Professor validar as decisões de desenho: coorte madura de 90 dias, mínimo de 30 por célula, estratificação por serviço | Professor |
| P17 | Confirmar com a PBH (SUMOG) se existem dados posteriores a jul/2023 e o significado dos canais/situações não documentados | Grupo |
| P13 | Datas reais de S02, S03 e entrega final | Grupo |
| P14 | Link do repositório / GitHub Projects; nomes completos dos integrantes | Grupo |

Falta para a entrega: revisão do trio (interpretação, ameaças, impacto, categorias e conclusões), nomes e links (P14), resposta do professor (P15, P16) e o ensaio da apresentação de 10 minutos. O rascunho do documento final está em `docs/documento_final.md` (falta a versão de entrega, #31) e o material da apresentação em `docs/apresentacao/` (#32).
