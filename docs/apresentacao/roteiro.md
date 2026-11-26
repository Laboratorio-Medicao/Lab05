# Roteiro da apresentação (10 minutos) — LAB05

Formato (enunciado §8): **reunião simulada com o gestor do atendimento da PBH**. Quem fala se dirige ao gestor ("vocês", "o senhor"), não à banca. Slides em `docs/apresentacao/slides.html` (só o teclado navega: setas e espaço; Ctrl+P exporta PDF, um slide por página). Números e fontes: `docs/documento_final.md`. Nas falas, números grandes são arredondados ("1,04 milhão", "187 mil dias"); os slides trazem o valor exato.

**Quem é quem** (nomes completos pendentes, P14): **A** = Planejamento e Método; **B** = Instrumentação e Operação; **C** = Análise e Impacto. Troque "A, B, C" pelos nomes quando forem confirmados.

## 1. Quadro de tempo

| # | Bloco | Quem | Tempo | Acumulado | Slides | Mensagem-chave |
|---|---|---|---|---|---|---|
| 1 | Abertura: a reunião com o gestor, a pergunta | A | 0:45 | 0:45 | 1 | Para o mesmo serviço, o canal muda o tempo e a chance de encerramento? |
| 2 | O software: real, em operação, alto impacto | A | 1:00 | 1:45 | 2 | Três critérios, cada número com fonte e data; volume autodeclarado |
| 3 | Caminho, GQM, hipóteses e 7 categorias | A | 1:15 | 3:00 | 3, 4 | Dados de operação no lugar de participantes (sem registro de aprovação do professor); observacional, não experimento |
| 4 | Dados, ética e reprodutibilidade | B | 1:15 | 4:15 | 5, 6 | 1 req/s, sem endereço, 1.042.926 elegíveis; reproduzido com ressalvas, por agente de IA |
| 5 | Resultado global | B | 0:45 | 5:00 | 7 | Sem olhar o serviço, os canais parecem diferentes (a JARI explica o Presencial) |
| 6 | "A diferença vem sobretudo do serviço" e a decisão sobre as hipóteses (figura 05) | C | 1:30 | 6:30 | 8, 9 | Efeito cerca de 10 vezes menor no mesmo serviço; há diferenças estatísticas, nenhuma relevante |
| 7 | Pares ajustados e D14 (figura 06) | C | 1:00 | 7:30 | 10 | Com o Presencial, o Tapa-Buraco decide e o sinal se inverte: inconclusivo |
| 8 | Impacto (figura 07) e o que não se pode afirmar | C | 1:00 | 8:30 | 11, 12 | Contrafactual hipotético, escala de grandeza; encerrada não é resolvida |
| 9 | Ameaças (4 tipos) e conceitos da disciplina | B | 0:45 | 9:15 | 13, 14 | 20 ameaças, nenhuma tratada como resolvida; Goodhart e McNamara |
| 10 | Reaproveitamento dos labs | B | 0:15 | 9:30 | 15 | Conceitos dos labs; o desenho do Lab02 foi substituído |
| 11 | Recomendação ao gestor e pendências | A | 0:30 | 10:00 | 16 | Investigar os serviços, não o canal; cautela com a taxa como meta; P15 e P16 |
| | **Total** | A 3:30 · B 3:00 · C 3:30 | **10:00** | | 16 | |

Passagens de bastão: A para B aos 3:00; B para C aos 5:00; C para B aos 8:30; B para A aos 9:30. Não há folga: o ensaio decide se falta tempo. Se estourar, corte primeiro o slide 6 (só o funil) e o slide 14 (conceitos); **não corte** a decisão sobre as hipóteses (slide 9), a D14 (slide 10), o contrafactual (slide 11) nem o "encerrada não é resolvida" (slide 12). O bloco 8 é o mais denso (cerca de 134 palavras em 1:00, perto do ritmo corrido): se não couber no ensaio, tire "quase metade só no Tapa-Buraco" ou a segunda negação.

## 2. O que dizer, bloco a bloco

### Bloco 1 — Abertura (A, 0:45, slide 1)

Bom dia, obrigado por nos receber. Somos [nomes], da PUC Minas, e analisamos os dados abertos de atendimento da própria prefeitura. Vocês atendem o cidadão por quatro canais: Portal de Serviços, PBH APP, Telefone 156 e o presencial no BH Resolve. A pergunta que trouxemos é: para um mesmo serviço, o canal por onde o pedido entra muda o tempo até o encerramento e a chance de ele ser encerrado? Os dados vão de maio de 2020 a julho de 2023.

### Bloco 2 — O software (A, 1:00, slide 2)

Primeiro, por que este software serve ao estudo. Ele é real: o Portal roda sobre a plataforma SYDLE ONE, o que aparece no código da página e no rodapé. Está em operação desde 12 de maio de 2020. E tem alto impacto: 1.492 serviços catalogados, 1.118 deles solicitáveis pela internet, e cerca de 497 mil solicitações de janeiro a outubro de 2023 nos quatro canais, numa cidade de 2,3 milhões de habitantes. Um aviso: os números de volume são autodeclarados pela prefeitura, por isso cada um vem com fonte e data.

### Bloco 3 — Caminho, GQM, hipóteses e categorias (A, 1:15, slides 3 e 4)

Nossa proposta inicial era um experimento com 32 participantes, comparando celular e computador. Era inviável para o grupo, então passamos a usar dados reais de operação: mesmo objeto, sem participantes. Dizemos com franqueza que não há registro de aprovação do professor para essa mudança nem para as decisões de desenho, as pendências P15 e P16. A hipótese nula é que não há diferença entre canais, e só chamamos de relevante se o teste rejeitar e o efeito for ao menos pequeno. E isto não é um experimento: ninguém atribuiu o canal, o cidadão escolhe. É observacional retrospectivo, nas sete categorias. Nos procedimentos, são dados já existentes, sem intervenção nossa; no controle, o canal é autosselecionado, então o controle é estatístico, por serviço; e o nível de evidência é de associação, não de causa.

### Bloco 4 — Dados, ética e reprodutibilidade (B, 1:15, slides 5 e 6)

Os dados vêm do CKAN da PBH, licença CC-BY, e cobrem de maio de 2020 a julho de 2023; não há 2024 a 2026, ao contrário do que supúnhamos. A coleta usa a API a uma requisição por segundo, com user-agent identificado. Endereço e localização são descartados na leitura, antes de chegar à memória ou ao disco, e o Id é pseudonimizado; 74 testes automatizados cobrem isso. Da base de 1,48 milhão de registros, ficam cerca de 1,04 milhão elegíveis, depois de tirar 7 registros inconsistentes, os canais não comparáveis e a coorte com menos de 90 dias de seguimento. O pipeline foi reexecutado do zero por um agente de IA, a pedido de um integrante, e não por um de nós; o veredito é "reproduzido com ressalvas".

### Bloco 5 — Resultado global (B, 0:45, slide 7)

Olhando os canais sem considerar o serviço, parece haver muita diferença. Portal e PBH APP têm mediana de 3 dias; o Telefone 156, 20 dias. Encerram em até 90 dias entre 84,8% e 90,7% dos pedidos. O Presencial aparece com só 10,6%, mas 44.391 dos 50.057 pedidos presenciais são recursos à JARI, que ficam "em andamento" no sistema. Por isso a mediana do Presencial não é comparável.

### Bloco 6 — A diferença vem sobretudo do serviço (C, 1:30, slides 8 e 9)

Esta é a mensagem central: a diferença vem sobretudo do serviço, não do canal. Comparando dentro do mesmo serviço, o efeito típico é cerca de 10 vezes menor: o V de Cramér, uma medida de associação de 0 a 1, cai de 0,46 para 0,040 na mediana de 58 serviços. Isso se explica por confusão pelo tipo de serviço: cada canal recebe uma mistura diferente de demandas, e a JARI é o exemplo extremo. Sobre as hipóteses: os testes globais e os testes por par, dentro do serviço, rejeitam a igualdade; os testes dos sinais rejeitam no tempo em quatro pares e, na proporção, só entre Portal e APP. Mas nenhuma diferença é relevante pela regra de magnitude: sem o Presencial, o delta de Cliff, que mede o quanto um canal tende a ser mais lento que o outro, é desprezível, e a diferença de risco mediana fica abaixo de 1 ponto percentual. Com o Presencial, a magnitude é inconclusiva, e 156 contra Presencial, com 2 serviços, não se interpreta.

### Bloco 7 — Pares ajustados e D14 (C, 1:00, slide 10)

Por que o Presencial fica sem conclusão? Para resumir os serviços num número, cada serviço pesa pelo volume que tem nos dois canais. No Tapa-Buraco, o Portal tem 94.968 pedidos encerrados e o Presencial, só 217, e lá o Presencial é mais lento: 8 dias contra 3. Esse serviço sozinho decide o resultado. Com outro peso, ou serviço a serviço, o sinal se inverte: o Portal é mais lento em 17 dos 20 serviços em comum. Na proporção, a JARI faz o mesmo papel. Registramos isso como a divergência D14, achada depois dos resultados. Sem o Presencial, o sinal não muda com o peso.

### Bloco 8 — Impacto e o que não se pode afirmar (C, 1:00, slides 11 e 12)

Para dar escala, usamos um contrafactual hipotético: e se, no mesmo serviço, os pedidos de um canal tivessem o desempenho do outro? Se os pedidos do APP tivessem o desempenho do Portal, cada um levaria cerca de 1,7 dia a mais até o encerramento; somado num ano, dá a ordem de 187 mil dias, quase metade só no Tapa-Buraco. Com o 156 é o contrário: ele é mais lento, 2,31 dias frente ao Portal e 2,69 frente ao APP. Isso é escala de grandeza, não economia que alguém vá obter, e os pares com Presencial ficam de fora. O que não podemos afirmar: que mudar de canal acelera o atendimento, porque o cidadão escolhe o canal; que o Presencial encerra menos ou é mais lento no mesmo serviço; e, sobretudo, que encerrada signifique resolvida.

### Bloco 9 — Ameaças e conceitos (B, 0:45, slides 13 e 14)

Mapeamos 20 ameaças à validade, dos quatro tipos: conclusão, interna, construto e externa. As mais sérias são a confusão pelo serviço, o serviço que domina o efeito com o Presencial, "encerrada não é resolvida" e a validade restrita a Belo Horizonte entre 2020 e 2023. Nenhuma é tratada como resolvida. Da disciplina, Goodhart e McNamara pesam aqui: se a taxa de encerramento virasse meta, poderia ser "jogada", e a data de encerramento é só o que é fácil de medir.

### Bloco 10 — Reaproveitamento dos labs (B, 0:15, slide 15)

Dos laboratórios anteriores, reaproveitamos conceitos: coleta por API (Lab01), métricas de operação (Lab03), escolha de teste e tamanho de efeito (Lab04). O desenho do Lab02 foi substituído.

### Bloco 11 — Recomendação e pendências (A, 0:30, slide 16)

Para vocês: a diferença global está em qual serviço cada canal atende; Tapa-Buraco, Iluminação Pública e a JARI são os primeiros a investigar. E, pelo que a disciplina ensina com Goodhart, se a taxa de encerramento virar meta, vale acompanhar também se o problema foi resolvido (leitura nossa). Ficam P15 e P16 com o professor. Obrigado.

## 3. Pontos que a banca costuma cobrar, e onde aparecem

| Ponto | Onde |
|---|---|
| Decisão sobre as hipóteses (há diferenças estatísticas, nenhuma relevante) | Slide 9; banco de perguntas, item 6 |
| Por que é observacional e não experimento | Slides 3 e 4; banco, item 3 |
| "A diferença vem sobretudo do serviço" (JARI, efeito ~10 vezes menor) | Slides 7 e 8 |
| D14 (Tapa-Buraco, pares inconclusivos, 156 × Presencial) | Slides 9 e 10 |
| Impacto como contrafactual hipotético | Slide 11 |
| Encerrada não é resolvida (Goodhart, McNamara) | Slides 12, 14 e 16 |
| Sete categorias | Slide 4 |
| Ameaças dos 4 tipos | Slide 13 |
| Reaproveitamento dos labs | Slide 15 |
| Mudança de metodologia sem registro de aprovação (P15 e P16) | Slides 3 e 16 |
