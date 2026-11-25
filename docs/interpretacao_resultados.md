# Interpretação dos resultados — LAB05 (issue #25)

**Versão 1.0 · 24/11/2026** · Papel C (Análise e Impacto) · Metodologia v3.0

> Estudo **observacional**: tudo aqui é **associação, não causa**. "Encerrada" é encerramento administrativo, **não** prova que o problema do cidadão foi resolvido.
> Nenhum número foi digitado à mão sem fonte: cada um aponta para um arquivo em `resultados/`, gerado por `python scripts/pipeline.py` com os dados reais (execução de 24/11/2026).
> A mudança de metodologia e as decisões de desenho (90 dias, ≥ 30 por célula, estratificação por serviço) **ainda não foram aprovadas pelo professor** (P15, P16).

## 1. Resposta curta

| Pergunta (GQM) | Resposta | Força da evidência |
|---|---|---|
| Q1. Que canal encerra mais rápido? | Portal e PBH APP (mediana de 3 dias); o Telefone 156 leva 20 dias. **Dentro do mesmo serviço** o 156 continua mais lento na maioria dos serviços, mas a diferença típica é **desprezível**. A distância global vem sobretudo de o 156 atender outro tipo de serviço | Consistente, de magnitude desprezível |
| Q2. A proporção encerrada difere? | Portal, APP e 156 encerram entre 85% e 91% em ≤ 90 dias. O Presencial encerra só 10,6%, mas **isso é efeito de um serviço** (recurso à JARI) | Diferença global grande, **não** sustentada dentro dos serviços |
| Q3. As diferenças se mantêm dentro do serviço? | **Pouco.** Só o par Portal × APP tem sentido consistente nas duas medidas (APP um pouco melhor), e com magnitude desprezível. Nos pares com Presencial o resultado agregado é **inconclusivo** (ver §4) | Fraca a moderada |
| Q4. Onde a diferença é grande? | Em serviços específicos: Tapa-Buraco (APP 1 dia × 156 19 dias), Informação sobre Multa (Portal 9 × APP 1), Iluminação Pública (APP 75% × 156 36% encerradas) | Forte em cada serviço, mas são poucos casos |

**Mensagem principal:** a maior parte da diferença entre canais que se vê nos números gerais vem de **qual serviço** cada canal atende, e não do canal em si. Quando se compara o mesmo serviço, os canais digitais e o telefone ficam próximos, com exceções pontuais.

## 2. Q1 e Q2: visão por canal (sem ajustar pelo serviço)

Fonte: `resultados/tabelas/metricas_por_canal.csv`, população elegível (1.042.926 solicitações, `funil_elegibilidade.csv`).

| Canal | Solicitações | % encerrada ≤ 90 d | Mediana (d) | Q1–Q3 | P90 | Encerradas no mesmo dia | Serviços |
|---|---:|---:|---:|---|---:|---:|---:|
| Portal de Serviços | 549.574 | 87,0% | 3 | 0–16 | 57 | 28,7% | 414 |
| PBH APP | 329.202 | 90,7% | 3 | 0–14 | 45 | 27,1% | 366 |
| Telefone 156 | 114.093 | 84,8% | 20 | 9–38 | 95 | 3,5% | 68 |
| Presencial (BH Resolve) | 50.057 | 10,6% | 4 | 1–20 | 55 | 22,3% | 83 |

- **Tempo:** Portal e APP têm a mesma mediana; o 156 tem uma mediana quase 7 vezes maior e quase nunca encerra no mesmo dia.
- **Proporção:** o Presencial destoa muito. Das 50.057 solicitações presenciais elegíveis, **44.391 (88,7%) são recursos à JARI** (`pares_por_servico.csv`), serviço que fica "em andamento" no sistema (1,2% encerradas). Sem a JARI, o retrato do Presencial muda completamente.
- **Teste global** (`resultados.json`, `comparacao_ingenua`): qui-quadrado com V de Cramér = 0,46 (associação forte) e Kruskal–Wallis com ε² = 0,077. Esses valores **misturam serviços diferentes** e servem só como ponto de partida.

## 3. Q3: comparando o mesmo serviço

Fonte: `resultados/tabelas/pares_ajustados_por_servico.csv` e `omnibus_por_servico.csv`. Como n ≈ 10⁶, quase todo p sai < 0,0001; a leitura é feita **pelo tamanho do efeito e pela consistência entre serviços** (teste dos sinais), conforme a METODOLOGIA §6.

### 3.1 Quanto da diferença some ao controlar o serviço

| Medida | Global (sem ajuste) | Dentro do serviço (58 serviços com ≥ 3 canais) |
|---|---|---|
| Proporção (V de Cramér) | 0,46 | mediana 0,040; 12 de 58 serviços com p (Holm) < 0,05 |
| Tempo (ε²) | 0,077 | mediana 0,006; 24 de 58 serviços com p (Holm) < 0,05 |

O efeito típico dentro de um serviço é **cerca de 10 vezes menor** que o global. É um caso de **confusão pelo tipo de serviço**: cada canal recebe uma mistura diferente de demandas.

### 3.2 Pares de canais

Convenção: para o par A × B, OR > 1 significa que A encerra mais em 90 dias, e delta > 0 que A é mais lento. "Serviços" conta em quantos serviços cada canal levou vantagem; o p do teste dos sinais já tem a correção de Holm.

| Par | Serviços | Proporção: OR MH · dif. de risco mediana · serviços A/B (p sinais) | Tempo: delta combinado · serviços em que A/B é mais lento (p sinais) | Leitura |
|---|---:|---|---|---|
| Portal × APP | 159 / 149 | 0,84 · −0,59 pp · 52/94 (0,004) | +0,088 (desprezível) · 98/51 (0,0007) | **APP um pouco melhor nas duas medidas, de forma consistente**, mas com diferença desprezível |
| Portal × 156 | 45 | 1,12 · +0,32 pp · 25/20 (1,0) | −0,108 (desprezível) · 11/34 (0,003) | 156 mais lento na maioria dos serviços, mas pouco; **sem sentido consistente** na proporção |
| APP × 156 | 45 | 1,12 · +0,78 pp · 28/17 (0,68) | −0,130 (desprezível) · 8/37 (0,0001) | Igual ao anterior |
| Portal × Presencial | 20 | 19,1 · −0,28 pp · 6/12 (0,71) | −0,171 (pequena) · 17/3 (0,008) | **Inconclusivo**: agregado e serviços apontam em sentidos opostos (§4) |
| APP × Presencial | 15 | 13,8 · +0,10 pp · 9/3 (0,68) | −0,391 (média) · 10/5 (0,60) | **Inconclusivo** (§4) |
| 156 × Presencial | 2 | 0,55 · −12,8 pp · 0/2 (1,0) | +0,052 · 2/0 (0,60) | Só 2 serviços: **não interpretar** |

### 3.3 O que se pode dizer

1. **Telefone 156 × canais digitais.** O 156 é mais lento em cerca de 3 de cada 4 serviços em comum (34 de 45 contra o Portal; 37 de 45 contra o APP), e esse padrão é estatisticamente consistente. A magnitude típica, porém, é desprezível (delta mediano por serviço de −0,06). A diferença de 3 × 20 dias nas medianas gerais vem sobretudo de **o 156 atender outro conjunto de serviços** (68 serviços contra mais de 360 nos canais digitais), em geral de fiscalização e manutenção urbana, que levam mais tempo. Na proporção encerrada, não há vencedor consistente.
2. **Portal × APP.** O APP encerra um pouco mais e um pouco mais rápido na maioria dos 150 serviços em comum. É o resultado mais robusto do estudo (mesmo sentido nas duas medidas, nos horizontes de 30, 90 e 180 dias e com qualquer ponderação, §4), mas a diferença é **desprezível** para o cidadão médio.
3. **Presencial.** Os números agregados (OR de 14 a 19) não descrevem o canal. A proporção é dominada pela JARI (I² = 0,99), e na mediana dos serviços a diferença de risco fica perto de zero (−0,28 pp e +0,10 pp). **Não se pode dizer que o Presencial encerra menos** quando o serviço é o mesmo.

## 4. Achado da interpretação: um serviço domina o delta combinado

O delta combinado é uma média dos deltas por serviço com peso n_A × n_B, calculado só com as encerradas (`scripts/estatistica.py`, `estratificado_por_par`). Com esse peso, um serviço com muitíssimos registros num canal domina o resultado mesmo que tenha poucos no outro. O cálculo abaixo foi feito a partir de `resultados/tabelas/pares_por_servico.csv` (código no Apêndice).

| Par | Serviço com maior peso (fatia do peso) | Delta combinado (n_A × n_B) | Delta com peso n_A·n_B/(n_A+n_B) | Mediana dos deltas por serviço |
|---|---|---:|---:|---:|
| Portal × APP | Tapa-Buraco (59%) | +0,088 | +0,070 | +0,048 |
| Portal × 156 | Ouvidoria (57%) | −0,108 | −0,071 | −0,057 |
| APP × 156 | Ouvidoria (35%) | −0,130 | −0,074 | −0,065 |
| Portal × Presencial | Tapa-Buraco (44%) | **−0,171** | **+0,074** | **+0,103** |
| APP × Presencial | Tapa-Buraco (68%) | **−0,391** | **+0,027** | **+0,032** |

- No Tapa-Buraco, o Presencial tem só **217 encerradas** contra 94.968 do Portal e 133.634 do APP, e é bem mais lento (mediana de 8 dias contra 3 e 1). Esse único serviço responde por **toda** a vantagem dos canais digitais sobre o Presencial no delta combinado.
- Com uma ponderação que não favorece o canal maior, ou olhando a mediana por serviço, o sinal **se inverte**: o Presencial passa a ser ligeiramente mais rápido. A contagem de serviços concorda (Portal mais lento em 17 de 20).
- **Conclusão:** nos pares com Presencial, o delta combinado (−0,17 "pequena" e −0,39 "média") **não deve ser apresentado como resultado**. O tempo do Presencial frente aos canais digitais é **inconclusivo**. Nos três pares sem Presencial o sinal é o mesmo com qualquer ponderação e a magnitude segue desprezível, então a leitura da §3.3 se mantém.
- **Não alteramos o pipeline.** O peso foi fixado antes de ver os resultados (FONTE_DA_VERDADE §6), e trocá-lo agora seria mudar a análise depois de ver os dados. Fica como **ameaça à validade de conclusão** e como sugestão de análise de sensibilidade, a decidir pelo grupo (registrada na FONTE_DA_VERDADE §18, D14). A figura `06_comparacao_pares_ajustada.png` e o painel mostram o delta combinado; ao apresentá-los, é preciso mencionar esta ressalva.

## 5. Q4: onde a diferença entre canais é grande

Fonte: `resultados/tabelas/ranking_servicos_tempo.csv` e `ranking_servicos_proporcao.csv` (15 maiores de cada).

**Tempo** (maior |delta|):

| Serviço | Par | Medianas (d) | Delta | Magnitude |
|---|---|---|---:|---|
| Tapa-Buraco | APP × 156 | 1 × 19 | −0,72 | grande |
| Árvore: análise de intervenção motivada por edificação | Portal × APP | 9 × 0 | +0,57 | grande |
| Informação sobre Notificação de Trânsito: Multa | Portal × APP | 9 × 1 | +0,52 | grande |
| Autorização para afastamento: Feira da Afonso Pena | APP × Presencial | 11 × 2 | +0,47 | média |

**Proporção encerrada em ≤ 90 dias** (maior |diferença de risco|):

| Serviço | Par | % encerrada | Diferença | Magnitude (h) |
|---|---|---|---:|---|
| Recurso à JARI | APP × Presencial | 65,0% × 1,2% | +63,8 pp | grande |
| Iluminação Pública: luminária apagada à noite | APP × 156 | 75,3% × 36,2% | +39,1 pp | grande |
| Compensação de débitos com precatório próprio | Portal × APP | 48,6% × 87,1% | −38,5 pp | grande |
| Programa Locação Social | Portal × APP | 37,8% × 69,1% | −31,3 pp | média |

Leitura: as diferenças grandes existem, mas estão **concentradas em poucos serviços** e não seguem sempre o mesmo canal: às vezes o Portal perde para o APP, às vezes o 156 perde para o APP. Isso combina com a ideia de que o fluxo interno de cada serviço (para onde a solicitação é roteada e como é triada) pesa mais que o canal de entrada. **Isso é uma hipótese**, não algo que os dados mostram. Dos 286 pares serviço × canal testados, 30 diferem na proporção e 59 no tempo após Holm (`resumo.md`).

## 6. Sensibilidade

Fonte: `resultados/tabelas/sensibilidade_horizonte.csv` (OR de Mantel–Haenszel em 30, 90 e 180 dias).

| Par | 30 d | 90 d | 180 d |
|---|---:|---:|---:|
| Portal × APP | 0,84 | 0,84 | 0,77 |
| Portal × 156 | 1,16 | 1,12 | 1,10 |
| APP × 156 | 1,18 | 1,12 | 1,19 |
| Portal × Presencial | 12,0 | 19,1 | 24,5 |
| APP × Presencial | 7,6 | 13,8 | 23,2 |

- O **sentido** de todos os pares se mantém nos três horizontes: a escolha de 90 dias não muda a conclusão.
- Nos pares com Presencial, o OR muda muito com o horizonte (de 7,6 para 23,2), outro sinal de que a estimativa é **instável** e dominada pela JARI.

## 7. Pressupostos e limites da análise

- **Independência:** não é verificável, porque a base não identifica o cidadão (`resultados.json`, `pressupostos`). Pode haver vários pedidos da mesma pessoa.
- **Empates nos tempos:** são frequentes (proporção mediana de empates de 0,027, máxima de 0,44), por isso o tempo é lido pelo delta de Cliff e não por diferença de medianas.
- **Testes de proporção por serviço:** 213 qui-quadrado, 56 Fisher e 17 degenerados (todos encerrados nos dois canais), estes fora da família de Holm.
- **Heterogeneidade:** I² entre 0,89 e 0,99 em todos os pares. O efeito varia muito de serviço para serviço, então um único número combinado resume mal; por isso a contagem de serviços e a mediana por serviço vêm sempre junto.
- **Armadilha de medição (Goodhart/McNamara):** "encerrada" pode ser encerramento administrativo. Um canal que "encerra mais rápido" pode só estar fechando o pedido mais cedo, e não resolvendo o problema. Os dados não permitem separar os dois casos.

## 8. O que **não** é possível afirmar

- Que mudar de canal faz o pedido ser atendido mais rápido (o estudo é observacional e o cidadão escolhe o canal).
- Que o Presencial encerra menos ou é mais lento para um mesmo serviço (§3.3 e §4).
- Que encerrado significa resolvido.
- Nada fora de BH, de mai/2020–jul/2023 e dos serviços com ≥ 2 canais comparáveis.

## 9. Implicações para as próximas etapas

- **Ameaças (#24, Marcos):** acrescentar a dominância do delta combinado por um serviço (§4) como ameaça de **conclusão**, e a confusão pelo tipo de serviço (§3.1) como exemplo concreto de ameaça **interna**.
- **Impacto (#29):** usar só os pares com conclusão sustentada (Portal × APP e canais digitais × 156) e deixar claro que as diferenças típicas são desprezíveis. Uma estimativa de impacto baseada no Presencial ou nas medianas gerais seria **enganosa**.
- **Apresentação:** a mensagem "a diferença está no serviço, não no canal" e o caso do Tapa-Buraco/JARI ilustram bem a confusão e são bons exemplos para a banca.
- **Decisão do grupo:** incluir ou não, como sensibilidade no pipeline, o delta combinado com peso n_A·n_B/(n_A+n_B) e a mediana por serviço (D14).

## Apêndice: verificação da ponderação (§4)

Reproduzível a partir do arquivo versionado, sem a base processada:

```python
import pandas as pd
p = pd.read_csv("resultados/tabelas/pares_por_servico.csv")
for (a, b), s in p[p.delta_cliff.notna()].groupby(["canal_a", "canal_b"]):
    w = s.encerradas_a * s.encerradas_b                       # peso usado no pipeline
    wh = w / (s.encerradas_a + s.encerradas_b)                # peso alternativo
    i = w.idxmax()
    print(a, b, len(s),
          round((w * s.delta_cliff).sum() / w.sum(), 3),      # reproduz delta_combinado
          round((wh * s.delta_cliff).sum() / wh.sum(), 3),
          round(s.delta_cliff.median(), 3),
          s.servico[i], round(w[i] / w.sum(), 2))             # serviço de maior peso
```

A primeira coluna de delta reproduz exatamente o `delta_combinado` de `pares_ajustados_por_servico.csv`. Isso confirma que `encerradas_a` × `encerradas_b` é o peso usado no código.
