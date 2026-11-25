# Conclusões e limitações — LAB05 (issue #27)

**Versão 1.0 · 25/11/2026** · Metodologia v3.0 · Responde às duas perguntas do enunciado: "o que o estudo mostrou?" e "o que isso significa para quem usa esse software?"

> Estudo **observacional**: tudo aqui é **associação, não causa**. "Encerrada" é encerramento administrativo, **não** prova que o problema foi resolvido. O Presencial é **inconclusivo**. Nenhuma conclusão vai além de `docs/interpretacao_resultados.md`, e este documento não cria números: cada um vem da seção citada.
> A mudança de metodologia e as decisões de desenho **ainda não foram aprovadas pelo professor** (P15, P16).

## 1. O que o estudo mostrou

1. **A maior parte da diferença entre canais vem do serviço, não do canal.** O efeito típico dentro de um serviço é cerca de 10 vezes menor que o global (V de Cramér de 0,46 para mediana 0,040; ε² de 0,077 para 0,006). É confusão pelo tipo de serviço: cada canal recebe uma mistura diferente de demandas (interpretação §3.1).
2. **Portal e PBH APP são muito parecidos; o APP leva uma pequena vantagem.** Mesma mediana de 3 dias; o APP encerra um pouco mais e um pouco mais rápido na maioria dos serviços em comum. É o resultado mais robusto do estudo (mesmo sentido nas duas medidas e nos horizontes de 30, 90 e 180 dias), mas a diferença é **desprezível** (interpretação §1, §3.3 item 2 e §6).
3. **O Telefone 156 é mais lento, mas pouco, dentro do mesmo serviço.** A mediana geral é de 20 dias contra 3 dos canais digitais, porém o 156 é mais lento em 34 de 45 serviços em comum com o Portal e em 37 de 45 com o APP, com magnitude típica desprezível. A distância global vem sobretudo de o 156 atender outro conjunto de serviços. Na proporção encerrada não há vencedor consistente (interpretação §3.3 item 1).
4. **O Presencial não pode ser descrito pelos números agregados.** A proporção encerrada é dominada pelo recurso à JARI (88,7% das solicitações presenciais elegíveis) e o delta de tempo é dominado pelo Tapa-Buraco. Nos pares com Presencial, o resultado é **inconclusivo** (interpretação §2, §3.3 item 3 e §4).
5. **Há diferenças grandes, mas em poucos serviços.** Exemplos: Tapa-Buraco (APP 1 dia × 156 19 dias), Informação sobre Multa (Portal 9 × APP 1) e Iluminação Pública (APP 75,3% × 156 36,2% encerradas). Não seguem sempre o mesmo canal (interpretação §5).
6. **A escolha dos 90 dias não muda o sentido dos resultados.** O sentido de todos os pares se mantém nos horizontes de 30, 90 e 180 dias (interpretação §6).

## 2. O que isso significa para quem usa

**Para o cidadão.** Dentro do mesmo serviço, escolher entre o Portal e o APP faz pouca diferença no encerramento, e o 156 tende a ser um pouco mais lento (interpretação §3.3). Isso descreve o que aconteceu com quem escolheu cada canal, e não promete que trocar de canal acelere o atendimento: o cidadão escolhe o canal, e o estudo não separa o efeito do canal do perfil de quem o escolhe. Também não diz que o pedido foi resolvido, só que foi encerrado.

**Para a gestão da PBH.** A diferença global está sobretudo em **qual serviço** cada canal atende, não no canal de entrada (interpretação §3.1). Os serviços em que a diferença entre canais é grande (Q4, interpretação §5) são os candidatos a investigar primeiro. Que o roteamento e a triagem do serviço pesam mais que o canal é uma **hipótese** da interpretação, não algo que os dados mostram. Vale ainda conferir o que "encerrada" significa em cada serviço, o que os dados abertos não documentam (K1, K2).

**Impacto.** A estimativa de impacto para quem usa o serviço está **pendente** no card #29 (`docs/impacto.md` ainda não existe). Por isso este documento **não traz nenhum número de impacto**. Quando existir, deve usar só os pares com conclusão sustentada (Portal × APP e canais digitais × 156) e deixar claro que as diferenças típicas são desprezíveis (interpretação §9).

## 3. Limitações

Cada limitação cita o ID da ameaça correspondente (`docs/metodologia.md` §8, card #24).

1. **Confusão pelo tipo de serviço e autosseleção do canal (I1, I2).** A estratificação corrige a mistura de serviços, mas não a de perfis dentro do serviço. Urgência e perfil do solicitante não estão nos dados, e a região existe na fonte, mas é descartada na leitura por privacidade (dicionário §2); qualquer diferença residual pode vir deles.
2. **"Encerrada" não é "resolvida" (K1, K2).** O significado das situações e dos canais "Integração entre Sistemas" e "Origem Interna" não é documentado pela PBH. Um canal que encerra mais rápido pode só fechar o pedido mais cedo, e os canais não documentados ficaram fora da análise principal.
3. **Os pares com Presencial não sustentam conclusão (C2, E3).** O delta de tempo é dominado pelo Tapa-Buraco, e o OR de Mantel–Haenszel, pela JARI, e é instável entre horizontes. Só 20 e 15 serviços são comuns ao Presencial e aos canais digitais, e 2 no par 156 × Presencial.
4. **Um número combinado resume mal (C3).** O efeito varia muito de serviço para serviço (I² entre 0,89 e 0,99); por isso a contagem de serviços e a mediana por serviço acompanham todo valor combinado.
5. **O valor de p quase não discrimina (C1, C7).** Nos testes agregados quase todo p é < 0,0001; por serviço, só 30 e 59 de 286 testes ficam abaixo de 0,05 após Holm (interpretação §5). A leitura é pelo tamanho do efeito. A correção de Holm vale dentro de cada família de testes, não entre famílias.
6. **Hipóteses escritas depois dos resultados (C6).** As definições e os testes foram fixados antes da análise, mas as hipóteses H0/H1 foram formalizadas depois; não é um estudo pré-registrado.
7. **Independência e empates (C4, C5).** A base não identifica o cidadão, então ICs e p podem estar otimistas, e os empates (encerramento no mesmo dia) tornam o tempo menos preciso nos serviços rápidos.
8. **Tempo: período longo, sem análise temporal (I4, I3, K3).** Plataforma, regras e demanda (incluindo a pandemia) mudaram entre 2020 e 2023 e o ano não entra como estratificador. A coorte madura de 90 dias deixa de fora os pedidos recentes, e o corte de observação é inferido.
9. **Medida grosseira e nome do serviço (K4, K5).** A resolução é de 1 dia e "0 dia" significa o mesmo dia civil. Além disso, o serviço é identificado pelo nome normalizado, e a normalização pode juntar ou separar serviços de forma imperfeita.
10. **Validade externa (E1, E2, E4).** Só Belo Horizonte, de mai/2020 a jul/2023, e só serviços com pelo menos 2 canais comparáveis. Os canais não comparáveis ficaram fora da análise (298.570 registros, `funil_elegibilidade.csv`; E4, K2).

## 4. O que não é possível afirmar

Ver `docs/interpretacao_resultados.md` §8. Em resumo: que mudar de canal acelera o atendimento; que o Presencial encerra menos ou é mais lento para o mesmo serviço; que encerrado significa resolvido; e qualquer coisa fora de BH, do período e dos serviços com ≥ 2 canais comparáveis.

## 5. Trabalhos futuros

- **Dados após jul/2023:** perguntar à PBH se existem (P17); a fonte aberta termina em jul/2023.
- **Significado das situações:** obter da PBH a regra de "Situação Atendimento Atual" (P17), para separar encerramento de resolução (K1).
- **Combinação com survey:** ouvir usuários, o que o enunciado valoriza (§2b) e cobriria o que os dados de operação não têm (urgência, perfil, motivo da escolha do canal; I2).
- **Análise temporal:** o estudo atual é uma coorte retrospectiva com análise agregada no período, sem estudo de tendência temporal; estudar a evolução ano a ano exigiria incluir o ano na análise (I4).
- **Sensibilidade de ponderação:** decidir sobre o peso alternativo do delta combinado (D14, C2).
- **Sensibilidade do OR de MH:** não há sensibilidade equivalente à do delta (#39); avaliar, por exemplo, o OR sem o serviço Recurso à JARI (C2).
