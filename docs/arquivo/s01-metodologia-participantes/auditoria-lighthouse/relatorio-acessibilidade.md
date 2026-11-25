# Relatório de Auditoria de Acessibilidade — LAB05

**Ferramenta:** Lighthouse 13.6.0 (categoria: accessibility)
**Data:** 2026-11-24
**Chrome:** 158.0.8127.37
**Executor:** Guilherme Vieira
**Páginas auditadas:** 8 (homepage, busca, 6 páginas de serviço das tarefas)

---

## Scores por página

| Página | URL | Score |
|--------|-----|-------|
| Homepage | servicos.pbh.gov.br/ | 84/100 |
| Página de busca | servicos.pbh.gov.br/servicos+... | 81/100 |
| A1 — Poda de árvore | servicos.pbh.gov.br/servicos+arvore-poda... | 77/100 |
| A2 — Tapa-Buraco | servicos.pbh.gov.br/tapaburaco | 77/100 |
| A3 — Alvará de obra | servicos.pbh.gov.br/5e6fbeedea9b0e547cd7f1f1 | 77/100 |
| B1 — IPTU Emissão | servicos.pbh.gov.br/5e838678d9521a26a96ee9d9 | 77/100 |
| B2 — Iluminação pública | servicos.pbh.gov.br/5e57abbde1bf5e706b5f4125 | 77/100 |
| B3 — Autorização de Evento | servicos.pbh.gov.br/5e5e9a25e1bf5e706b16f25f | 77/100 |

**Média:** 78,5/100

---

## Falhas encontradas

### Críticas — presentes em todas as 8 páginas

| ID | Título | WCAG | Severidade |
|----|--------|------|-----------|
| `button-name` | Botões sem nome acessível | 4.1.2 | Crítico |
| `image-alt` | Imagens sem atributo `alt` | 1.1.1 | Crítico |
| `link-name` | Links sem nome discernível | 4.1.2 | Crítico |

**Observação:** Os botões sem nome são o widget de VLibras (acessibilidade em Libras) e o chatbot flutuante — elementos de terceiros que a PBH não controla diretamente. As imagens sem alt incluem o logo da SYDLE no rodapé e imagens decorativas.

### Importantes — 7 das 8 páginas (ausente apenas na busca)

| ID | Título | WCAG | Severidade |
|----|--------|------|-----------|
| `heading-order` | Hierarquia de headings fora de ordem | 1.3.1 | Importante |

**Observação:** Em todas as páginas de serviço há um `<h6>` para o formulário de avaliação de satisfação antes que todos os níveis intermediários sejam usados.

### Moderadas — 6 das 8 páginas (apenas nas páginas de serviço)

| ID | Título | WCAG | Severidade |
|----|--------|------|-----------|
| `aria-allowed-attr` | Atributos `aria-*` não compatíveis com o role | 4.1.2 | Moderado |
| `color-contrast` | Contraste insuficiente entre texto e fundo | 1.4.3 | Moderado |

**Contraste:** o texto cinza claro dos metadados ("Atualizado em: ...") sobre fundo branco apresenta razão de contraste < 4,5:1.

### Menores — apenas na página de busca

| ID | Título | WCAG | Severidade |
|----|--------|------|-----------|
| `aria-input-field-name` | Campo de busca sem nome acessível via ARIA | 4.1.2 | Menor |
| `label` | Select ("Classificar por") sem `<label>` associado | 1.3.1 | Menor |

---

## Resumo por critério WCAG

| Critério | Título | Falhas |
|----------|--------|--------|
| WCAG 1.1.1 | Conteúdo não textual | Imagens sem alt (8 pág.) |
| WCAG 1.3.1 | Informação e relacionamentos | Hierarquia de headings (7 pág.), Label ausente (1 pág.) |
| WCAG 1.4.3 | Contraste mínimo | Texto cinza claro (6 pág.) |
| WCAG 4.1.2 | Nome, Função, Valor | Botões sem nome (8 pág.), Links sem nome (8 pág.), aria-* inválido (6 pág.), ARIA input (1 pág.) |

---

## Arquivos brutos

Os JSONs do Lighthouse para cada página estão neste mesmo diretório (`data/auditoria/`).

---

## Interpretação para o relatório do LAB05

O Portal apresenta score médio de **78,5/100** — abaixo da referência WCAG AA (mínimo recomendado ~90/100). As falhas mais graves afetam usuários de leitores de tela:

1. **Botões e links sem nome** impedem navegação por teclado e leitores de tela de identificar elementos interativos.
2. **Imagens sem alt** ocultam contexto visual de leitores de tela (principalmente logotipos e ícones decorativos).
3. **Contraste insuficiente** afeta usuários com baixa visão, especialmente em texto de metadados.

A maioria das falhas é sistêmica (mesma plataforma SYDLE em todas as páginas), então a correção em um componente se propagaria para todo o Portal.
