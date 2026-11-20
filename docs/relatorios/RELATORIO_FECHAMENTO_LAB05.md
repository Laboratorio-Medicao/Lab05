# Relatório de fechamento — LAB05 S01

Data: 17/11/2026.

## 1. Veredito

**Finalizado com pendências externas.** O texto está metodologicamente coerente e sem contradições internas relevantes. Não é "aprovado pelo professor": as pendências P1 a P14 da seção 10 da proposta dependem do professor, do grupo ou de evidência documental.

## 2. Arquivos produzidos

- `LAB05_S01_Proposta_FINAL.md` (fonte oficial)
- `LAB05_S01_Proposta_FINAL.pdf` (gerado do Markdown)
- `RELATORIO_FECHAMENTO_LAB05.md` (este arquivo)

Cópias preservadas: `LAB05_S01_Proposta_v2_pre_FINAL.md` (estado anterior), `original_S01.txt` (texto de 16/11).

## 3. Correções mais importantes

| Tema | Seção | Alteração |
|---|---|---|
| Auditoria e robots.txt | Resumo, 1, 2, 6 | Removida a afirmação de que toda medição é manual. Agora distingue participantes (navegação manual), integrante que aciona axe e Lighthouse em páginas selecionadas, verificações automatizadas dessas ferramentas na página aberta e ausência de crawler. Não se afirma que o robots.txt autoriza ou proíbe as ferramentas: a compatibilidade é pendência (P8, P12). |
| RQ4 | 3, 4, 6, 7, 8 | Conduzida como análise exploratória descritiva, sem p-valor. A permutação só seria considerada se o grupo e o professor definirem critério e estratégia (P4), porque a permutabilidade não é defensável: rótulos não randomizados, passos sequenciais, mesma página nos dois dispositivos, denominadores diferentes, complexidade e posição associadas. "Sem violação detectada" distinto de ausência comprovada. Passos sem elemento identificável formam a categoria "indeterminado", com quantidade e motivo reportados. |
| Estimativa de impacto | 7, 9 | Resultado principal: impacto relativo (razão das médias geométricas, RQ1, RQ3). Conversão em horas como análise secundária pendente (P5). Sem dados inventados. |
| GQM × RQs | 3 | Correspondência explícita; lista do que entra nos testes e do que é descritivo. |
| Poder | 4 | Tabela por cenário (S0, S1, S2) e por RQ, conferida em `results_v3_2.json`, com limitações. |
| Amostra e recrutamento | 4 | 32 analisáveis, 8 por sequência; 36–38 agendados (reservas incluídas); 3 do piloto fora da análise; 39–41 recrutados. Regra operacional provisória de fechamento, marcada como não aprovada (P2). |
| HTTP 200 em 0,49 s | 1, 10 | Frase retirada do texto até haver evidência de medição compatível com a navegação manual (P7). A leitura do HTML ficou com marcador de pendência. |
| Pendências | 10 | Duplicatas e colchetes removidos do texto principal; 14 itens com tipo e responsável. |
| Texto | todo | Removidas as notas de auditoria e instruções internas do corpo. |

## 4. Pendências restantes

Todas listadas na seção 10 da proposta.

- **Professor ou instituição:** P1 (tempo de abandono e de pedido de ajuda), P2 (blocos completos e fechamento), P3 (critério ligado ao teto de 300 s), P11 (ética/CEP), P12 (validação das ferramentas de auditoria), P4 (com o grupo).
- **Grupo:** P5 (conversão em horas), P6 (n mínimo), P4.
- **Documental:** P7 (HTTP 200 e leitura do HTML), P8 (termos de uso), P9 (IBGE), P10 (LAI), P13 (datas), P14 (repositório e autoria).

## 5. Validações realizadas

- **Enunciado:** conteúdo exigido da S01 presente (software com os três critérios, pergunta, caminhos, 7 categorias, plano de coleta e análise, piloto). O enunciado não fixa n, número de hipóteses nem regra de descarte. A seção 6 mantém os cuidados de ética (consentimento, sem dados pessoais, robots.txt e termos de uso) como pendências onde não há evidência.
- **Cálculos:** os 9 valores de poder (S0, S1, S2 × RQ1, RQ2, RQ3, n = 32) foram conferidos em `results_v3_2.json` (S1: 0,671, 0,821 e 0,818). Aritmética de recrutamento: 32/0,90 ≈ 35,6; 32/0,85 ≈ 37,6; mais 3 do piloto dá 39–41.
- **Consistência:** 4 RQs, um par H0/H1 cada; Holm só em RQ1–RQ3; RQ4 fora; 32 e 8 por sequência; nenhum "20%", "quadrado latino" como método nem "diferença mediana"; todos os P1 a P14 referenciados existem na tabela.
- **Markdown e PDF:** o PDF foi gerado do Markdown. A comparação por palavras acusou 5 diferenças, todas de quebra de linha em hífen. Revisei visualmente as páginas 3, 4, 7 e 8 do PDF final (tabelas de hipóteses, poder, ameaças e pendências legíveis, sem conteúdo cortado; algumas linhas de tabela atravessam a quebra de página) e as páginas 1, 2, 5, 6 e 9 de uma montagem anterior com o mesmo texto e margens maiores. A última página tem poucas linhas.
- **Limites da validação:** não há numeração de página no PDF; a ferramenta usada não suporta rodapé.

## 6. O que o grupo precisa fazer antes de entregar ao professor

1. Levar ao professor P1, P2, P3, P11 e P12 e registrar as respostas.
2. Documentar P7 a P10: como foi obtido o HTML da página inicial, a leitura dos termos de uso, o número do IBGE e o envio do pedido LAI. Reincluir o tempo de resposta só se houver evidência.
3. Confirmar P13 (datas) e preencher P14 (repositório e autoria).
4. Decidir P4 e P5, se quiserem um teste na RQ4 ou a conversão em horas, e P6 (n mínimo).
5. Confirmar que concordam com a RQ4 descritiva e com a categoria "indeterminado", adotadas nesta versão por instrução, não por votação registrada.
6. Conferir o PDF visualmente nas páginas não vistas.
