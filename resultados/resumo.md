# Resumo dos resultados (gerado por `scripts/pipeline.py`)

> Gerado automaticamente a partir da base processada. Estudo observacional: associação, não causa.

- Período de criação: 2020-05-11 a 2023-07-31
- Parâmetros: horizonte = 90 dias; mínimo por célula = 30; α = 0.05

## Funil de elegibilidade

| Etapa | Registros |
|---|---:|
| Registros na base analítica (sem duplicatas) | 1.480.736 |
| Excluídos: inconsistentes | 7 |
| Excluídos: canal não comparável (integração, origem interna, e-mail) | 298.570 |
| Excluídos: seguimento < 90 dias (coorte imatura) | 139.233 |
| Elegíveis (análise principal) | 1.042.926 |

## Métricas por canal (população elegível)

| Canal | Solicitações | % encerrada (corte) | % encerrada ≤ 90 d | Mediana (d) | Q1–Q3 | P90 | Mediana KM (d) |
|---|---:|---:|---:|---:|---|---:|---:|
| Portal de Serviços | 549.574 | 93,4% | 87,0% | 3 | 0–16 | 57 | 3 |
| PBH APP | 329.202 | 96,1% | 90,7% | 3 | 0–14 | 45 | 3 |
| Telefone 156 | 114.093 | 94,8% | 84,8% | 20 | 9–38 | 95 | 21 |
| Presencial (BH Resolve) | 50.057 | 11,5% | 10,6% | 4 | 1–20 | 55 | n/d |

n/d = a curva de Kaplan–Meier não chega a 50% (menos da metade encerrou).

## Pares de canais ajustados por serviço

A = primeiro canal. OR de Mantel–Haenszel > 1: A encerra mais em 90 d. Delta de Cliff > 0: A mais lento. p com correção de Holm (6 pares).

| Par (A × B) | Serviços (prop.) | OR MH [IC 95%] | p (CMH, Holm) | I² | Serviços (tempo) | Delta combinado [IC 95%] | Magnitude | p (van Elteren, Holm) |
|---|---:|---|---|---:|---:|---|---|---|
| Portal de Serviços × PBH APP | 159 | 0.84 [0.83; 0.86] | < 0,0001 | 0,89 | 149 | 0.088 [0.085; 0.092] | desprezível | < 0,0001 |
| Portal de Serviços × Telefone 156 | 45 | 1.12 [1.09; 1.16] | < 0,0001 | 0,94 | 45 | -0.108 [-0.117; -0.099] | desprezível | < 0,0001 |
| Portal de Serviços × Presencial (BH Resolve) | 20 | 19.10 [17.98; 20.28] | < 0,0001 | 0,99 | 20 | -0.171 [-0.198; -0.144] | pequena | < 0,0001 |
| PBH APP × Telefone 156 | 45 | 1.12 [1.09; 1.15] | < 0,0001 | 0,95 | 45 | -0.130 [-0.138; -0.123] | desprezível | < 0,0001 |
| PBH APP × Presencial (BH Resolve) | 15 | 13.81 [12.88; 14.81] | < 0,0001 | 0,99 | 15 | -0.391 [-0.419; -0.363] | média | 0,0120 |
| Telefone 156 × Presencial (BH Resolve) | 2 | 0.55 [0.46; 0.66] | < 0,0001 | 0,94 | 2 | 0.052 [0.020; 0.084] | desprezível | < 0,0001 |

## Testes por serviço e par

- Pares (serviço × par de canais) testados: 286
- Proporção com p ajustado (Holm) < 0.05: 30
- Tempo com p ajustado (Holm) < 0.05: 59
- Testes de proporção usados: {'qui2': 213, 'fisher': 56, 'degenerado': 17}
- Mediana da proporção de empates nos tempos: 0,027

## Impacto estimado (associação, não causa)

Estimativa de contrafactual hipotético: o que mudaria se os pedidos do segundo canal (B) tivessem o desempenho do primeiro (A) no mesmo serviço. É associação, não causa: o cidadão escolhe o canal e encerrar não significa resolver.

Coorte de 2020-05-11 a 2023-04-26 (2,96 anos). A = primeiro canal do par. As duas medidas têm sinais próprios. Tempo (diferença de mediana e dias de espera por ano): valor positivo = B mais lento que A no mesmo serviço; valor negativo = B mais rápido (neste resultado, em Portal de Serviços × PBH APP o valor de tempo é negativo: PBH APP é mais rápido que Portal de Serviços no mesmo serviço). Taxa (encerradas em ≤ 90 d a mais por ano): valor positivo = B encerra menos que A (seriam encerradas mais solicitações de B em até 90 dias com o desempenho de A); valor negativo = B encerra mais que A. IC de 95% por bootstrap reamostrando serviços. Nas estimativas pontuais, tempo e taxa apontam no mesmo sentido nos 3 pares comparados, mas cada medida tem o próprio IC e deve ser lida separadamente.

| Par (A × B) | Serviços | Pedidos de B por ano | Diferença de mediana ponderada (dias) | Dias de espera por ano (B − A) | Encerradas em ≤ 90 d a mais por ano |
|---|---:|---:|---:|---:|---:|
| Portal de Serviços × PBH APP | 159 | 110.551 | -1,69 [-3,37; -0,32] | -186.607 [-421.157; -25.214] | -760 [-1.647; -8] |
| Portal de Serviços × Telefone 156 | 45 | 38.470 | 2,31 [0,84; 4,50] | 88.973 [34.911; 158.072] | 348 [18; 735] |
| PBH APP × Telefone 156 | 45 | 38.470 | 2,69 [1,02; 5,38] | 103.616 [38.194; 186.419] | 336 [-154; 829] |

Pares com Presencial ficam de fora (resultado inconclusivo) e não se usam as medianas globais. Não há conversão em horas do cidadão (P5): dias de espera até o encerramento não são horas de esforço.
