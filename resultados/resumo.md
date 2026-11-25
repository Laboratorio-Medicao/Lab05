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
