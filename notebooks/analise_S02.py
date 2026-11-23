# %% [markdown]
# # LAB05 — Análise da S02 (notebook em formato percent)
#
# > **AVISO: DADOS SINTÉTICOS ATÉ A COLETA. NADA AQUI É RESULTADO.**
# > Os números abaixo vêm de dados falsos, com efeitos plantados de propósito
# > (`scripts/gerar_dados_sinteticos.py`), e servem só para mostrar que o
# > pipeline funciona (FONTE_DA_VERDADE §2.3 e §17).
#
# Formato: arquivo `.py` com células `# %%`, que abre como notebook no VS Code
# (extensão Python/Jupyter) ou no Jupyter com jupytext, e também roda direto
# com `python notebooks/analise_S02.py`. Escolhido no lugar de `.ipynb` para
# versionar sem saídas embutidas e sem exigir jupyter instalado
# (FONTE_DA_VERDADE §18, D10).
#
# Parâmetros pendentes do professor: **P1** (tempo de abandono/ajuda) e
# **P2** (regra de fechamento) estão nas opções provisórias, marcadas
# "PENDENTE"; as outras variantes aparecem como sensibilidade.
# **P4**: a chave `RQ4_TESTE` desliga o teste da RQ4 se o professor recusar.

# %%
import json
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd()
if not (RAIZ / "scripts").exists():
    RAIZ = RAIZ.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import analise as A  # noqa: E402
import gerar_dados_sinteticos as G  # noqa: E402
import validar_dados as V  # noqa: E402

# Troque para RAIZ / "dados" / "brutos" quando houver coleta real validada.
PASTA_DADOS = RAIZ / "dados" / "sinteticos"
P1 = A.P1_PRIMARIA
P2 = A.P2_PRIMARIA
RQ4_TESTE = True

if not (PASTA_DADOS / "SINTETICO_sessoes.csv").exists() and "sinteticos" in PASTA_DADOS.parts:
    G.gravar(G.gerar(), PASTA_DADOS)

# %% [markdown]
# ## 1. Validação
# Passar aqui não torna o dado "Verificado": exige segunda pessoa (FDV §2.3).

# %%
achados, sintetico = V.validar(PASTA_DADOS)
erros = [a for a in achados if a.nivel == "erro"]
print(f"origem sintética: {sintetico} · erros: {len(erros)} · "
      f"avisos: {sum(a.nivel == 'aviso' for a in achados)}")
for a in achados:
    if a.nivel != "info":
        print(f"[{a.nivel}] {a.tabela}/{a.regra}: {a.mensagem}")
assert not erros, "corrija os erros de validação antes de analisar"

# %% [markdown]
# ## 2. Análise (RQ1–RQ3 com Holm; RQ4 exploratória)

# %%
tabelas, sintetico, origem = A.preparar(PASTA_DADOS)
res = A.analisar(tabelas, origem, p1=P1, p2=P2, rq4_teste=RQ4_TESTE)
print(A.resumo_texto(res))

# %% [markdown]
# ### Amostra e quem ficou fora (P2)

# %%
print(json.dumps(res["amostra"]["fora_da_analise"], ensure_ascii=False, indent=1))

# %% [markdown]
# ### RQ1 — tarefas concluídas (descritiva)

# %%
print(json.dumps(A._jsonavel(res["rq1"]["descritiva"]), ensure_ascii=False, indent=1))
print("diferença média da taxa (celular − computador):", round(res["rq1"]["dif_taxa_media"], 3),
      "IC95 bootstrap:", [round(x, 3) for x in res["rq1"]["dif_taxa_ic95_bootstrap"]])

# %% [markdown]
# ### RQ2 — tempo (teto de 300 s): descritiva e sensibilidades

# %%
print(json.dumps(A._jsonavel(res["rq2"]["descritiva"]["tarefas_no_teto"]), ensure_ascii=False))
print(json.dumps(A._jsonavel(res["rq2"]["sensibilidade"]), ensure_ascii=False, indent=1))
print(json.dumps(A._jsonavel(res["sensibilidades"]["p1"]), ensure_ascii=False, indent=1))

# %% [markdown]
# ### RQ3 — SUS (comparação com 68 só descritiva)

# %%
print(json.dumps(A._jsonavel(res["rq3"]["descritiva"]), ensure_ascii=False, indent=1))

# %% [markdown]
# ### RQ4 — EXPLORATÓRIA (fora do Holm, p sem ajuste, associação e não causa)

# %%
r4 = A._jsonavel(res["rq4"])
for chave in ("n_elegiveis", "excluidos_por_motivo", "media_d_i", "media_d_i_ic95_bootstrap",
              "primario_exploratorio", "sensibilidade_permutacao_sinais", "tabela_2x2"):
    print(chave, "=", json.dumps(r4.get(chave), ensure_ascii=False))

# %% [markdown]
# ### Checagem de ordem (descritiva, poder baixo e não calculado)

# %%
print(json.dumps(A._jsonavel(res["checagem_ordem"]), ensure_ascii=False, indent=1))

# %% [markdown]
# ## 3. Auditoria (Q4, descritiva) e gravação das saídas
# Saídas sintéticas vão para uma pasta temporária; nunca para `resultados/`.

# %%
aud = A.analisar_auditoria(PASTA_DADOS, sintetico)
if aud:
    print(json.dumps(A._jsonavel(aud["top10_regras_wcag"]), ensure_ascii=False, indent=1))
saida = Path(tempfile.mkdtemp(prefix="lab05_sintetico_")) if sintetico else RAIZ / "resultados"
escritos = A.gravar_saidas(res, aud, saida, sintetico)
print(f"{len(escritos)} arquivos em {saida}")
