# P10 — Enviar pedido via LAI à PBH (instruções para quem vai enviar)

Responsável pelo envio: **Arthur** · Criado em 20/11/2026 · Issue #16 · Pendência **P10**
Contexto: [FONTE_DA_VERDADE.md](../../FONTE_DA_VERDADE.md) §14 · [S01_criterios_do_software.md](./S01_criterios_do_software.md) §5

## 1. Para que serve

O Portal de Serviços da PBH (https://servicos.pbh.gov.br) não publica quantos acessos tem por mês. Nosso trabalho (LAB05, Laboratório de Experimentação de Software, PUC Minas) precisa desse número para mostrar o **alto impacto** do software, que o enunciado exige com "números e fontes". Vamos pedir o dado pela **Lei de Acesso à Informação (Lei 12.527/2011)**.

Esse dado serve só como **contexto** e para uma análise secundária de impacto. Ele não entra no experimento.

## 2. O que você precisa fazer (passo a passo)

1. **Achar o canal de LAI da PBH.** No Portal, na página inicial, há um cartão **"Lei de Acesso à Informação – LAI"** ("Direito de acesso às informações públicas"). Pode começar por ele. *Ainda não verificamos para onde ele leva nem se exige login gov.br.*
2. **Se pedir login gov.br:** use a **sua própria conta**. Não compartilhe senha nem códigos com ninguém, nem com o assistente de IA, nem no grupo.
3. **Preencher o formulário** com o texto da seção 3 abaixo (copiar e colar). Se o formulário tiver campos separados (assunto, descrição), use o assunto e o corpo indicados.
4. **Formato de resposta:** pedir planilha/CSV, se houver o campo.
5. **Antes de enviar**, conferir: o pedido **não** inclui dado pessoal de terceiros, e o seu contato é institucional ou o que você aceita expor.
6. **Enviar.**
7. **Salvar o protocolo** (número, tela de confirmação e e-mail de confirmação, se vier). Tirar uma captura da tela do protocolo **sem mostrar CPF, senha ou token**.
8. **Passar para o grupo** (ver seção 5).

## 3. Texto do pedido (copiar e colar)

**Assunto:** Pedido de acesso à informação — acessos ao Portal de Serviços da PBH

**Corpo:**

> Com base na Lei nº 12.527/2011 (Lei de Acesso à Informação), solicito, para fins de pesquisa acadêmica (disciplina Laboratório de Experimentação de Software, curso de Engenharia de Software, PUC Minas), os seguintes dados do Portal de Serviços da Prefeitura de Belo Horizonte (servicos.pbh.gov.br):
>
> 1. Número mensal de acessos ao Portal (sessões e usuários únicos), de janeiro de 2025 a outubro de 2026.
> 2. Distribuição desses acessos por tipo de dispositivo (celular, computador, tablet), se disponível.
> 3. Número mensal de solicitações de serviço registradas no Portal, por serviço, para os seguintes serviços: poda de árvore; alvará; reparo de buraco na via; segunda via de guia municipal.
>
> Solicito os dados em formato de planilha ou CSV. Não solicito dados pessoais, apenas dados agregados.
>
> Atenciosamente,
> [Nome de quem envia], [contato institucional]

Notas:
- Os 4 serviços são os **candidatos** das tarefas do experimento; ainda não são definitivos. Não tem problema pedir os quatro.
- Se o formulário limitar o tamanho, mantenha os itens 1 e 3 e corte o item 2.
- Não é necessário justificar além do que está no texto; a LAI dispensa justificativa do motivo.

## 4. O que NÃO fazer

- Não enviar pedido com dados de participantes da pesquisa ou de qualquer pessoa.
- Não inventar informação sobre o grupo ou a instituição que não possa comprovar.
- Não compartilhar senha, código ou token do gov.br.
- Não enviar o mesmo pedido duas vezes (se o sistema falhar, primeiro conferir se o protocolo foi gerado).
- Não usar o Portal para nada além do necessário (sem abrir solicitações de serviço reais).

## 5. O que devolver ao grupo

Preencher e mandar ao Marcos (ou editar este arquivo):

| Campo | Valor |
|---|---|
| Quem enviou | Arthur |
| Data e hora do envio | _a preencher_ |
| Canal usado (nome e endereço da página) | _a preencher_ |
| Exigiu login gov.br? | _a preencher_ |
| **Número do protocolo** | _a preencher_ |
| Captura da tela do protocolo arquivada em | `docs/evidencias/capturas/` (nome sugerido: `AAAA-MM-DD_lai_protocolo.png`) |
| Prazo informado pelo sistema | _a preencher_ (referência legal: 20 dias, prorrogáveis por 10; conferir) |
| Resposta (data e arquivo) | _a preencher quando chegar_ |

## 6. Quando a P10 conta como encerrada

Para a issue #16: quando o **protocolo de envio** estiver arquivado. A resposta pode demorar além da sprint e **não deve travar a issue**; ela deve ser registrada aqui quando chegar. Se a PBH negar ou não responder no prazo, registrar isso também (é resultado válido, e o grupo mantém o número de acessos como "desconhecido" na proposta).

## 7. Observações do grupo

- O assistente de IA **não enviou** nem vai enviar este pedido. Envio externo com identificação pessoal deve ser feito por uma pessoa.
- Não verificamos ainda o formulário real da LAI; se os campos forem diferentes, adapte o texto e anote o que mudou.
