# Relatório de Piloto — LAB05

**Data:** 2026-11-24
**Moderador:** Guilherme Vieira (P00 — sessão de validação)
**Objetivo:** Verificar se todas as tarefas são navegáveis no Portal sem login e ajustar telas-alvo.

---

## Resultado por tarefa

| Tarefa | Termo testado | Resultado | Serviço encontrado | Status |
|--------|--------------|-----------|-------------------|--------|
| A1 — Poda de árvore | "poda de árvore" | 17 itens | Árvore - Poda de Árvore em Passeios, Praças, etc. | ✅ Válida |
| A2 — Buraco na via | "buraco na via" | 4 itens | Tapa-Buraco / Via Pública - Recapeamento | ✅ Válida |
| A3 — Alvará de obra | "alvará de obra" | 51 itens | Licenciamento de Edificação/Alvará na Hora | ✅ Válida |
| B1 — Segunda via IPTU | "IPTU" | 62 itens | Guias - IPTU - Emissão (1º resultado) | ✅ Válida |
| B2 — Iluminação com defeito | "iluminação pública" | 16 itens | Iluminação Pública - Manutenção de Luminária Apagada Durante a Noite | ✅ Válida |
| B3 — Licença evento | "licença evento" | 3 itens | Autorização de Evento (1º resultado) | ✅ Válida |

Todos os serviços são acessíveis **sem login**. A página de detalhes de cada serviço carrega completa antes do botão "Solicitar".

---

## Achados da busca

- **A2:** busca "buraco na via" retorna "Via Pública - Recapeamento" (terminologia técnica, não "tapa-buraco"). É uma descoberta de usabilidade legítima. Busca direta por "tapa-buraco" provavelmente funcionaria.
- **B1:** busca "segunda via IPTU" retorna apenas 1 item errado ("Guias - Dívida Ativa"). Busca por "IPTU" retorna 62 itens com o serviço correto como 1º resultado. Os participantes provavelmente vão usar "IPTU" naturalmente.
- **B2:** busca "iluminação pública defeito" retorna **zero resultados**. Busca por "iluminação pública" retorna 16 itens com múltiplas variantes corretas. O Portal não aceita combinações muito específicas.

Esses achados são dados válidos de usabilidade e não invalidam as tarefas — mostram exatamente o tipo de dificuldade que o estudo quer medir.

---

## Ajustes feitos

- Telas-alvo dos arquivos de tarefa atualizadas com os nomes exatos dos serviços no Portal.
- Nenhuma alteração nos cenários entregues ao participante.
- Nenhuma tarefa eliminada.

---

## Conclusão

Piloto validado. As 6 tarefas funcionam e os serviços são acessíveis sem autenticação. Prosseguir para coleta com 32 participantes conforme o plano.
