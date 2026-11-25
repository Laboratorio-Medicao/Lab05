"""Gráficos e painel HTML do LAB05 (todos os números vêm de ``estatistica.analisar``).

Paleta categórica de 4 posições (azul, laranja, verde-água, amarelo), validada
com o validador do método de dataviz (ΔE de CVD ≥ 8). Como duas cores têm
contraste < 3:1 sobre fundo claro, todo gráfico tem rótulos diretos e o painel
traz as tabelas correspondentes.
"""

from __future__ import annotations

import base64
import html
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import config as C  # noqa: E402

COR = {"portal_servicos": "#2a78d6", "pbh_app": "#eb6834",
       "telefone_156": "#1baf7a", "presencial": "#eda100"}
TINTA, TINTA2, GRADE = "#0b0b0b", "#52514e", "#e3e2de"

plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
    "axes.edgecolor": GRADE, "axes.labelcolor": TINTA2, "xtick.color": TINTA2,
    "ytick.color": TINTA2, "text.color": TINTA, "axes.spines.top": False,
    "axes.spines.right": False, "font.size": 10, "axes.titlesize": 12,
    "axes.titleweight": "bold", "axes.titlelocation": "left", "figure.dpi": 110,
})

ROT = C.ROTULO_CANAL


def _fmt(n: float) -> str:
    return f"{n:,.0f}".replace(",", ".")


def _pct(x: float, casas: int = 1) -> str:
    return f"{100 * x:.{casas}f}".replace(".", ",") + "%"


def _salvar(fig, caminho: Path) -> Path:
    fig.savefig(caminho, bbox_inches="tight")
    plt.close(fig)
    return caminho


def _fonte(fig, texto: str, y: float = -0.02) -> None:
    fig.text(0.01, y, texto, fontsize=8, color=TINTA2, ha="left", va="top")


def _nota(r: dict) -> str:
    p = r["parametros"]
    return (f"Fonte: dados abertos da PBH (CKAN), solicitações criadas de mai/2020 a jul/2023. "
            f"Coorte madura: seguimento ≥ {p['horizonte_dias']} dias; canais comparáveis; "
            f"sem registros inconsistentes.")


def fig_solicitacoes(r: dict, pasta: Path) -> Path:
    d = r["por_canal"].sort_values("solicitacoes")
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    ax.barh(d["rotulo"], d["solicitacoes"], color=[COR[c] for c in d["canal"]], height=0.6)
    for y, v in enumerate(d["solicitacoes"]):
        ax.text(v, y, f"  {_fmt(v)}", va="center", fontsize=9)
    ax.set_xlim(0, d["solicitacoes"].max() * 1.18)
    ax.set_xlabel("Solicitações elegíveis (nº de registros)")
    ax.set_title("Solicitações por canal de atendimento")
    ax.xaxis.set_major_formatter(lambda v, _: _fmt(v))
    ax.grid(axis="x", color=GRADE)
    ax.set_axisbelow(True)
    _fonte(fig, _nota(r))
    return _salvar(fig, pasta / "01_solicitacoes_por_canal.png")


def fig_taxa(r: dict, pasta: Path) -> Path:
    h = r["parametros"]["horizonte_dias"]
    d = r["por_canal"].iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    y = np.arange(len(d))
    col = f"taxa_encerramento_{h}d"
    ax.barh(y + 0.19, d["taxa_encerramento_corte"] * 100, height=0.34, color="#c9c8c2",
            label="Encerrada até o corte (qualquer prazo)")
    ax.barh(y - 0.19, d[col] * 100, height=0.34, color=[COR[c] for c in d["canal"]],
            label=f"Encerrada em até {h} dias")
    ax.errorbar(d[col] * 100, y - 0.19,
                xerr=[(d[col] - d["taxa_ic_lo"]) * 100, (d["taxa_ic_hi"] - d[col]) * 100],
                fmt="none", ecolor=TINTA, lw=1, capsize=2)
    for i, row in d.iterrows():
        ax.text(row["taxa_encerramento_corte"] * 100 + 1, i + 0.19,
                _pct(row["taxa_encerramento_corte"]), va="center", fontsize=8, color=TINTA2)
        ax.text(row[col] * 100 + 1, i - 0.19, _pct(row[col]), va="center", fontsize=9,
                fontweight="bold")
    ax.set_yticks(y, d["rotulo"])
    ax.set_xlim(0, 112)
    ax.set_xlabel("% das solicitações elegíveis (barras de erro: IC de 95% de Wilson)")
    ax.set_title("Taxa de encerramento por canal (sem controlar o serviço)")
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    ax.grid(axis="x", color=GRADE)
    ax.set_axisbelow(True)
    _fonte(fig, _nota(r))
    return _salvar(fig, pasta / "02_taxa_encerramento_por_canal.png")


def fig_mediana(r: dict, pasta: Path) -> Path:
    d = r["por_canal"].iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    for i, row in d.iterrows():
        c = COR[row["canal"]]
        ax.plot([row["q1_dias"], row["q3_dias"]], [i, i], color=c, lw=5, solid_capstyle="round",
                alpha=0.55)
        ax.plot(row["mediana_dias"], i, "o", color=c, ms=9, mec="#fcfcfb", mew=2)
        ax.text(row["q3_dias"] + 1.5, i,
                f"mediana {row['mediana_dias']:.0f} d (IQR {row['q1_dias']:.0f}–{row['q3_dias']:.0f})",
                va="center", fontsize=9)
    ax.set_yticks(range(len(d)), d["rotulo"])
    ax.set_xlim(0, max(d["q3_dias"].max() * 1.9, 10))
    ax.set_xlabel("Dias entre criação e encerramento (somente solicitações encerradas)")
    ax.set_title("Tempo de encerramento por canal: mediana e intervalo interquartil")
    ax.grid(axis="x", color=GRADE)
    ax.set_axisbelow(True)
    _fonte(fig, _nota(r) + " Mediana entre encerradas: condicional a ter encerrado.")
    return _salvar(fig, pasta / "03_tempo_mediano_por_canal.png")


def fig_distribuicao(r: dict, pasta: Path, limite: int = 180) -> Path:
    h = r["parametros"]["horizonte_dias"]
    el = r["elegiveis"]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    estilos = {"portal_servicos": "-", "pbh_app": "--", "telefone_156": "-.", "presencial": ":"}
    finais = []
    for canal in C.CANAIS_COMPARAVEIS:
        t = np.sort(el.loc[(el["canal"] == canal) & el["encerrada"], "tempo_dias"].to_numpy())
        if t.size == 0:
            continue
        x = np.arange(0, limite + 1)
        y = np.searchsorted(t, x, side="right") / t.size * 100
        ax.plot(x, y, color=COR[canal], ls=estilos[canal], lw=2)
        finais.append((y[-1], canal))
    # rótulos diretos no fim das curvas, espaçados para não se sobreporem
    finais.sort(reverse=True)
    pos, prox = [], 101.0
    for yv, canal in finais:
        prox = min(prox, yv + 3) if not pos else min(pos[-1] - 5, yv + 3)
        pos.append(prox)
    for (yv, canal), yt in zip(finais, pos):
        ax.annotate(ROT[canal], xy=(limite, yv), xytext=(limite + 6, yt), fontsize=8.5,
                    va="center", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color=COR[canal], lw=0.8))
    ax.axvline(h, color=TINTA2, lw=0.8)
    ax.text(h + 1, 3, f"{h} d", fontsize=8, color=TINTA2)
    ax.set_xlim(0, limite)
    ax.set_ylim(0, 102)
    ax.set_xlabel("Dias até o encerramento")
    ax.set_ylabel("% das encerradas já encerradas")
    ax.set_title("Distribuição acumulada do tempo de encerramento (ECDF)")
    ax.grid(color=GRADE)
    ax.set_axisbelow(True)
    _fonte(fig, _nota(r) + f" Eixo cortado em {limite} dias.")
    return _salvar(fig, pasta / "04_distribuicao_tempos.png")


def _top_servicos(r: dict) -> list[str]:
    """Maiores serviços (por volume) com ≥ 2 canais de célula válida."""
    sc = r["servico_canal"]
    v = sc[sc["celula_valida_proporcao"]]
    multi = v.groupby("servico_chave")["canal"].nunique()
    chaves = multi[multi >= 2].index
    vol = v[v["servico_chave"].isin(chaves)].groupby("servico_chave")["solicitacoes"].sum()
    return list(vol.sort_values(ascending=False).head(r["parametros"]["top_servicos"]).index)


def fig_servico_canal(r: dict, pasta: Path) -> Path:
    h = r["parametros"]["horizonte_dias"]
    sc = r["servico_canal"]
    chaves = _top_servicos(r)
    nomes = (sc.drop_duplicates("servico_chave").set_index("servico_chave")["servico"])
    canais = list(C.CANAIS_COMPARAVEIS)
    taxa = np.full((len(chaves), 4), np.nan)
    med = np.full((len(chaves), 4), np.nan)
    for i, k in enumerate(chaves):
        for j, c in enumerate(canais):
            lin = sc[(sc["servico_chave"] == k) & (sc["canal"] == c)]
            if lin.empty:
                continue
            lin = lin.iloc[0]
            if lin["celula_valida_proporcao"]:
                taxa[i, j] = 100 * lin[f"taxa_encerramento_{h}d"]
            if lin["celula_valida_tempo"]:
                med[i, j] = lin["mediana_dias"]
    # o "?" é o travessão perdido na própria fonte (ver config.chave_texto); só no rótulo
    limpos = {k: nomes[k].replace(" ? ", " – ") for k in chaves}
    rotulos = [(limpos[k][:46] + "…") if len(limpos[k]) > 47 else limpos[k] for k in chaves]
    fig, axs = plt.subplots(1, 2, figsize=(12, 0.42 * len(chaves) + 2.2), sharey=True)
    for ax, mat, titulo, fmt, cmap in (
            (axs[0], taxa, f"Encerradas em ≤ {h} dias (%)", "{:.0f}", "Blues"),
            (axs[1], med, "Mediana do tempo (dias)", "{:.0f}", "Blues")):
        ax.imshow(mat, aspect="auto", cmap=cmap, vmin=0,
                  vmax=100 if mat is taxa else np.nanmax(med) * 1.1)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = mat[i, j]
                if np.isnan(v):
                    ax.text(j, i, "–", ha="center", va="center", color=TINTA2, fontsize=9)
                else:
                    claro = v > (50 if mat is taxa else np.nanmax(med) * 0.55)
                    ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=8.5,
                            color="white" if claro else TINTA)
        ax.set_xticks(range(4), [ROT[c].replace(" (BH Resolve)", "") for c in canais],
                      rotation=20, ha="right")
        ax.set_title(titulo, fontsize=11)
        for s in ax.spines.values():
            s.set_visible(False)
    axs[0].set_yticks(range(len(chaves)), rotulos)
    axs[1].tick_params(left=False)
    fig.suptitle("Mesmo serviço, canais diferentes: os 15 maiores serviços com ≥ 2 canais comparáveis",
                 x=0.01, ha="left", fontsize=12, fontweight="bold")
    _fonte(fig, _nota(r) + f" '–' = menos de {r['parametros']['min_celula']} registros na célula.")
    return _salvar(fig, pasta / "05_servico_x_canal.png")


def fig_floresta(r: dict, pasta: Path) -> Path:
    e = r["estratificado_por_par"]
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.2), sharey=True)
    rot = [f"{ROT[a].replace(' (BH Resolve)', '')} × {ROT[b].replace(' (BH Resolve)', '')}"
           for a, b in zip(e["canal_a"], e["canal_b"])]
    y = np.arange(len(e))[::-1]
    ax = axs[0]
    ok = e["delta_combinado"].notna()
    ax.errorbar(e["delta_combinado"][ok], y[ok.to_numpy()],
                xerr=[(e["delta_combinado"] - e["delta_ic_lo"])[ok],
                      (e["delta_ic_hi"] - e["delta_combinado"])[ok]],
                fmt="o", color=COR["portal_servicos"], capsize=3, ms=6)
    ax.axvline(0, color=TINTA2, lw=0.8)
    for xv in (-0.147, 0.147):
        ax.axvline(xv, color=GRADE, lw=0.8, ls="--")
    ax.set_xlim(-1, 1)
    ax.set_xlabel("Delta de Cliff combinado (IC 95%)\n← A mais rápido    A mais lento →")
    ax.set_title("Tempo, dentro do mesmo serviço", fontsize=11)
    ax.set_yticks(y, rot)
    ax = axs[1]
    ok = e["or_mh"].notna()
    ax.errorbar(e["or_mh"][ok], y[ok.to_numpy()],
                xerr=[(e["or_mh"] - e["or_ic_lo"])[ok], (e["or_ic_hi"] - e["or_mh"])[ok]],
                fmt="o", color=COR["pbh_app"], capsize=3, ms=6)
    ax.axvline(1, color=TINTA2, lw=0.8)
    ax.set_xscale("log")
    ax.set_xlabel("Razão de chances de Mantel–Haenszel (IC 95%)\n← A encerra menos    A encerra mais →")
    ax.set_title(f"Encerrada em ≤ {r['parametros']['horizonte_dias']} dias, dentro do mesmo serviço",
                 fontsize=11)
    for a in axs:
        a.grid(axis="x", color=GRADE)
        a.set_axisbelow(True)
    fig.suptitle("Comparação entre pares de canais, ajustada por serviço (A × B)",
                 x=0.01, y=1.03, ha="left", fontsize=12, fontweight="bold")
    fig.subplots_adjust(wspace=0.08)
    _fonte(fig, _nota(r) + "\nLinhas tracejadas: limite de efeito desprezível (|delta| = 0,147).", y=-0.12)
    return _salvar(fig, pasta / "06_comparacao_pares_ajustada.png")


# ---------------------------------------------------------------------------
# Impacto estimado (issue #29): figura 07, tabela, texto do painel e do resumo
# ---------------------------------------------------------------------------

AVISO_IMPACTO = (
    "Estimativa de contrafactual hipotético: o que mudaria se os pedidos do segundo canal (B) "
    "tivessem o desempenho do primeiro (A) no mesmo serviço. É associação, não causa: o cidadão "
    "escolhe o canal e encerrar não significa resolver.")


def _par_rotulo(a: str, b: str) -> str:
    return f"{ROT[a].replace(' (BH Resolve)', '')} × {ROT[b].replace(' (BH Resolve)', '')}"


def _com_ic(x, lo, hi, f) -> str:
    return "–" if pd.isna(x) else f"{f(x)} [{f(lo)}; {f(hi)}]"


def tabela_impacto(r: dict) -> pd.DataFrame:
    """Tabela do impacto por par, já formatada em texto (painel e resumo)."""
    h = r["parametros"]["horizonte_dias"]
    d = r["impacto_por_par"]
    col_dif = "Diferença de mediana ponderada (dias)"
    col_dias = "Dias de espera por ano (B − A)"
    col_enc = f"Encerradas em ≤ {h} d a mais por ano"
    linhas = []
    for _, x in d.iterrows():
        linhas.append({
            "Par (A × B)": _par_rotulo(x["canal_a"], x["canal_b"]),
            "Serviços": int(x["servicos"]),
            "Pedidos de B por ano": _fmt(x["vol_b_ano_total"]),
            col_dif: _com_ic(x["dif_mediana_ponderada_dias"], x["dif_mediana_ponderada_dias_ic_lo"],
                             x["dif_mediana_ponderada_dias_ic_hi"], lambda v: _n(v, 2)),
            col_dias: _com_ic(x["dias_solicitacao_ano"], x["dias_solicitacao_ano_ic_lo"],
                              x["dias_solicitacao_ano_ic_hi"], _fmt),
            col_enc: _com_ic(x["encerradas_90d_ano"], x["encerradas_90d_ano_ic_lo"],
                             x["encerradas_90d_ano_ic_hi"], _fmt),
        })
    return pd.DataFrame(linhas)


def sentidos_impacto(r: dict) -> list[str]:
    """Para cada par, diz se tempo e taxa apontam no mesmo sentido ou em sentidos opostos."""
    h = r["parametros"]["horizonte_dias"]
    frases = []
    comparados = 0
    for _, x in r["impacto_por_par"].iterrows():
        dias, enc = x["dias_solicitacao_ano"], x["encerradas_90d_ano"]
        if pd.isna(dias) or pd.isna(enc) or dias == 0 or enc == 0:
            continue
        comparados += 1
        a, b = ROT[x["canal_a"]].replace(" (BH Resolve)", ""), ROT[x["canal_b"]].replace(" (BH Resolve)", "")
        if (dias > 0) != (enc > 0):
            frases.append(
                f"No par {a} × {b}, tempo e taxa apontam em sentidos opostos: {b} é "
                f"{'mais lento' if dias > 0 else 'mais rápido'} que {a} no tempo, mas encerra "
                f"{'menos' if enc > 0 else 'mais'} em até {h} dias. As duas medidas não são "
                "somadas numa conclusão só.")
    if comparados and not frases:
        onde = f"nos {comparados} pares comparados" if comparados > 1 else "no único par comparado"
        frases.append(f"Nas estimativas pontuais, tempo e taxa apontam no mesmo sentido {onde}, "
                      "mas cada medida tem o próprio IC e deve ser lida separadamente.")
    return frases


def _exemplo_sinal_impacto(r: dict) -> str:
    """Frase com o sinal do tempo no primeiro par (derivada dos dados); vazia se não houver."""
    d = r["impacto_por_par"]
    if d.empty:
        return ""
    x = d.iloc[0]
    dias = x["dias_solicitacao_ano"]
    if pd.isna(dias) or dias == 0:
        return ""
    a, b = ROT[x["canal_a"]].replace(" (BH Resolve)", ""), ROT[x["canal_b"]].replace(" (BH Resolve)", "")
    return (f" (neste resultado, em {a} × {b} o valor de tempo é {'positivo' if dias > 0 else 'negativo'}: "
            f"{b} é {'mais lento' if dias > 0 else 'mais rápido'} que {a} no mesmo serviço)")


def _texto_leitura_impacto(r: dict) -> str:
    co = r.get("coorte", {})
    h = r["parametros"]["horizonte_dias"]
    return (f"Coorte de {co.get('inicio', '?')} a {co.get('fim', '?')} "
            f"({_n(co.get('anos', float('nan')), 2)} anos). A = primeiro canal do par. As duas "
            "medidas têm sinais próprios. Tempo (diferença de mediana e dias de espera por ano): "
            "valor positivo = B mais lento que A no mesmo serviço; valor negativo = B mais rápido"
            + _exemplo_sinal_impacto(r) + ". "
            f"Taxa (encerradas em ≤ {h} d a mais por ano): valor positivo = B encerra menos que A "
            f"(seriam encerradas mais solicitações de B em até {h} dias com o desempenho de A); "
            "valor negativo = B encerra mais que A. IC de 95% por bootstrap reamostrando serviços. "
            + " ".join(sentidos_impacto(r)))


TEXTO_LIMITES_IMPACTO = (
    "Pares com Presencial ficam de fora (resultado inconclusivo) e não se usam as medianas "
    "globais. Não há conversão em horas do cidadão (P5): dias de espera até o encerramento "
    "não são horas de esforço.")


def linhas_markdown_impacto(r: dict) -> list[str]:
    """Seção "Impacto estimado" do resumo em Markdown."""
    L = ["", "## Impacto estimado (associação, não causa)\n", AVISO_IMPACTO + "\n",
         _texto_leitura_impacto(r) + "\n"]
    t = tabela_impacto(r) if len(r["impacto_por_par"]) else pd.DataFrame()
    if t.empty:
        L += ["Nenhum par de canais com serviços em comum suficientes para estimar o impacto.\n"]
    else:
        L += ["| " + " | ".join(t.columns) + " |",
              "|---|" + "---:|" * (len(t.columns) - 1)]
        L += ["| " + " | ".join(str(v) for v in lin) + " |" for lin in t.itertuples(index=False)]
        L += [""]
    L += [TEXTO_LIMITES_IMPACTO]
    return L


def secao_impacto_html(r: dict) -> str:
    """Seção "Impacto estimado" do painel."""
    t = tabela_impacto(r) if len(r["impacto_por_par"]) else pd.DataFrame()
    tab = (f'<div class="rolagem">{_tabela(t)}</div>' if not t.empty else
           "<p>Nenhum par de canais com serviços em comum suficientes para estimar o impacto.</p>")
    return (f"<h2>Impacto estimado (associação, não causa)</h2>\n"
            '<p class="aviso">' + html.escape(AVISO_IMPACTO) + '</p>\n'
            f"<p>{html.escape(_texto_leitura_impacto(r))}</p>\n{tab}\n"
            f"<p>{html.escape(TEXTO_LIMITES_IMPACTO)}</p>")


def fig_impacto(r: dict, pasta: Path) -> Path:
    d = r["impacto_por_par"].iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9.5, 3.2))
    if d.empty:
        ax.text(0.5, 0.5, "Nenhum par de canais com serviços em comum suficientes",
                ha="center", va="center", transform=ax.transAxes, color=TINTA2)
        ax.set_axis_off()
    else:
        y = np.arange(len(d))
        v = d["dif_mediana_ponderada_dias"]
        ax.barh(y, v, height=0.5, color=COR["portal_servicos"], alpha=0.85)
        ax.errorbar(v, y, xerr=[(v - d["dif_mediana_ponderada_dias_ic_lo"]).clip(lower=0),
                                (d["dif_mediana_ponderada_dias_ic_hi"] - v).clip(lower=0)],
                    fmt="none", ecolor=TINTA, lw=1, capsize=3)
        ax.axvline(0, color=TINTA2, lw=0.8)
        for i, row in d.iterrows():
            dias = _com_ic(row["dias_solicitacao_ano"], row["dias_solicitacao_ano_ic_lo"],
                           row["dias_solicitacao_ano_ic_hi"], _fmt)
            ax.text(1.02, i, f"{dias} dias de espera somados/ano", transform=ax.get_yaxis_transform(),
                    va="center", fontsize=8.5)
        ax.set_yticks(y, [f"{_par_rotulo(a, b)} ({int(n)} serv.)"
                          for a, b, n in zip(d["canal_a"], d["canal_b"], d["servicos"])])
        ax.margins(x=0.15)
        ax.grid(axis="x", color=GRADE)
        ax.set_axisbelow(True)
    ax.set_xlabel("Diferença de mediana (B − A) por serviço, média ponderada pelo volume de B "
                  "(dias; IC 95%)\n"
                  "← B mais rápido    B mais lento →")
    ax.set_title("Impacto estimado: diferença de tempo entre canais (A × B)")
    _fonte(fig, "Contrafactual hipotético (se B tivesse o desempenho de A no mesmo serviço); "
                "associação, não causa. À direita: dias de espera somados por ano (B − A).\n"
                + _nota(r), y=-0.18)
    return _salvar(fig, pasta / "07_impacto_por_par.png")


def gerar_figuras(r: dict, pasta: Path) -> list[Path]:
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    return [fig_solicitacoes(r, pasta), fig_taxa(r, pasta), fig_mediana(r, pasta),
            fig_distribuicao(r, pasta), fig_servico_canal(r, pasta), fig_floresta(r, pasta),
            fig_impacto(r, pasta)]


# ---------------------------------------------------------------------------
# Painel HTML (autocontido)
# ---------------------------------------------------------------------------

def _tabela(df: pd.DataFrame, formatos: dict | None = None) -> str:
    formatos = formatos or {}
    df = df.copy()
    for col, f in formatos.items():
        if col in df:
            df[col] = df[col].map(lambda v, f=f: "–" if pd.isna(v) else f(v))
    return df.to_html(index=False, escape=True, border=0, classes="tabela")


def _p(v) -> str:
    if pd.isna(v):
        return "–"
    return "< 0,0001" if v < 1e-4 else f"{v:.4f}".replace(".", ",")


def _n(v, c=2) -> str:
    return "–" if pd.isna(v) else f"{v:.{c}f}".replace(".", ",")


def gerar_painel(r: dict, figuras: list[Path], qualidade: dict, caminho: Path) -> Path:
    p = r["parametros"]
    h = p["horizonte_dias"]
    img = ""
    legendas = {
        "01": "Quantidade de solicitações elegíveis em cada canal.",
        "02": "Parcela encerrada. Atenção: não controla o serviço (ver gráfico 5 e 6).",
        "03": "Mediana e quartis do tempo, só entre encerradas.",
        "04": "Fração das encerradas que já tinham encerrado em cada prazo.",
        "05": "Comparação direta entre canais para o mesmo serviço.",
        "06": "Efeito combinado entre serviços para cada par de canais.",
        "07": "Impacto estimado por par (contrafactual hipotético; associação, não causa).",
    }
    for f in figuras:
        b64 = base64.b64encode(Path(f).read_bytes()).decode()
        img += (f'<figure><img alt="{html.escape(Path(f).stem)}" '
                f'src="data:image/png;base64,{b64}"><figcaption>'
                f'{legendas.get(Path(f).name[:2], "")}</figcaption></figure>\n')
    pc = r["por_canal"][["rotulo", "solicitacoes", "encerradas", "abertas",
                         "taxa_encerramento_corte", f"taxa_encerramento_{h}d", "mediana_dias",
                         "q1_dias", "q3_dias", "p90_dias", "mediana_km_dias"]].rename(columns={
        "rotulo": "Canal", "solicitacoes": "Solicitações", "encerradas": "Encerradas",
        "abertas": "Abertas", "taxa_encerramento_corte": "% encerrada (corte)",
        f"taxa_encerramento_{h}d": f"% encerrada ≤ {h} d", "mediana_dias": "Mediana (d)",
        "q1_dias": "Q1", "q3_dias": "Q3", "p90_dias": "P90",
        "mediana_km_dias": "Mediana Kaplan–Meier (d)"})
    est = r["estratificado_por_par"].copy()
    est["Par (A × B)"] = [f"{C.ROTULO_CANAL[a]} × {C.ROTULO_CANAL[b]}"
                          for a, b in zip(est["canal_a"], est["canal_b"])]
    est_t = est[["Par (A × B)", "servicos_prop", "or_mh", "or_ic_lo", "or_ic_hi", "p_cmh_holm",
                 "heterogeneidade_i2", "servicos_a_encerra_mais", "servicos_b_encerra_mais",
                 "servicos_tempo", "delta_combinado", "delta_ic_lo", "delta_ic_hi",
                 "delta_magnitude", "p_van_elteren_holm", "servicos_a_mais_lento",
                 "servicos_b_mais_lento"]]
    ing = r["comparacao_ingenua"]
    nao = (f"Qui-quadrado (4 canais): χ² = {_n(ing['proporcao']['chi2'], 0)}, "
           f"V de Cramér = {_n(ing['proporcao']['cramer_v'])}, p {_p(ing['proporcao']['p'])}. "
           f"Kruskal–Wallis: H = {_n(ing['tempo']['h'], 0)}, ε² = {_n(ing['tempo']['epsilon2'], 3)}, "
           f"p {_p(ing['tempo']['p'])}.")
    rank = r["ranking_servicos"]
    rt = rank.get("tempo", pd.DataFrame())
    rp = rank.get("proporcao", pd.DataFrame())
    fmt_rank = lambda df: df.assign(  # noqa: E731
        canal_a=df["canal_a"].map(C.ROTULO_CANAL), canal_b=df["canal_b"].map(C.ROTULO_CANAL))
    impacto_html = secao_impacto_html(r)
    corpo = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Canais de atendimento da PBH</title><style>
:root{{--bg:#fcfcfb;--fg:#0b0b0b;--fg2:#52514e;--linha:#e3e2de}}
@media(prefers-color-scheme:dark){{:root{{--bg:#1a1a19;--fg:#f0efec;--fg2:#c3c2b7;--linha:#3a3a38}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0 auto;
max-width:1100px;padding:16px}}h1{{font-size:1.5rem}}h2{{margin-top:2rem;font-size:1.15rem}}
.aviso{{border-left:4px solid #eda100;padding:.4rem .8rem;color:var(--fg2)}}
figure{{margin:1rem 0}}figure img{{max-width:100%;height:auto;border-radius:6px}}
figcaption{{color:var(--fg2);font-size:.85rem}}.rolagem{{overflow-x:auto}}
.tabela{{border-collapse:collapse;font-size:.8rem}}.tabela th,.tabela td{{border-bottom:1px solid var(--linha);
padding:3px 8px;text-align:right}}.tabela td:first-child,.tabela th:first-child{{text-align:left}}
</style></head><body>
<h1>Canais de atendimento da PBH: tempo e taxa de encerramento</h1>
<p class="aviso">Estudo observacional com dados abertos da PBH (mai/2020 a jul/2023). Mostra
associação, não causa. O canal não foi sorteado: o perfil das solicitações pode diferir entre canais.
Encerrar não significa que o problema foi resolvido. Todos os números foram calculados pelo pipeline
a partir da base processada.</p>
<h2>Resumo por canal</h2><div class="rolagem">{_tabela(pc, {
        "Solicitações": _fmt, "Encerradas": _fmt, "Abertas": _fmt,
        "% encerrada (corte)": _pct, f"% encerrada ≤ {h} d": _pct,
        "Mediana (d)": lambda v: _n(v, 0), "Q1": lambda v: _n(v, 0), "Q3": lambda v: _n(v, 0),
        "P90": lambda v: _n(v, 0), "Mediana Kaplan–Meier (d)": lambda v: _n(v, 0)})}</div>
<p>Comparação global, sem controlar o serviço (apenas ilustrativa): {html.escape(nao)}</p>
{img}
<h2>Pares de canais ajustados por serviço (Holm por família)</h2>
<p>A = primeiro canal do par. Razão de chances &gt; 1: A encerra mais em {h} dias. Delta &gt; 0: A leva
mais tempo. I² mede a heterogeneidade entre serviços (alto = efeito varia muito).</p>
<div class="rolagem">{_tabela(est_t, {
        "or_mh": _n, "or_ic_lo": _n, "or_ic_hi": _n, "p_cmh_holm": _p, "heterogeneidade_i2": _n,
        "delta_combinado": lambda v: _n(v, 3), "delta_ic_lo": lambda v: _n(v, 3),
        "delta_ic_hi": lambda v: _n(v, 3), "p_van_elteren_holm": _p})}</div>
{impacto_html}
<h2>Serviços com maior diferença de tempo entre canais</h2><div class="rolagem">{
        _tabela(fmt_rank(rt), {"delta_cliff": lambda v: _n(v, 3), "delta_ic_lo": lambda v: _n(v, 3),
                               "delta_ic_hi": lambda v: _n(v, 3), "p_tempo_holm": _p,
                               "mediana_a": lambda v: _n(v, 0), "mediana_b": lambda v: _n(v, 0)})
        if len(rt) else "<p>Sem dados.</p>"}</div>
<h2>Serviços com maior diferença na taxa de encerramento</h2><div class="rolagem">{
        _tabela(fmt_rank(rp), {"taxa_a": _pct, "taxa_b": _pct,
                               "dif_risco_pp": lambda v: _n(v, 1),
                               "dif_risco_ic_lo_pp": lambda v: _n(v, 1),
                               "dif_risco_ic_hi_pp": lambda v: _n(v, 1), "p_prop_holm": _p})
        if len(rp) else "<p>Sem dados.</p>"}</div>
<h2>Parâmetros e população</h2><div class="rolagem">{_tabela(r['funil'], {"registros": _fmt})}</div>
<p>Horizonte = {h} dias; mínimo por célula = {p['min_celula']}; α = {p['alfa']}.
Período de criação: {qualidade.get('periodo_criacao', ['?', '?'])[0]} a
{qualidade.get('periodo_criacao', ['?', '?'])[1]}.</p>
</body></html>"""
    caminho = Path(caminho)
    caminho.write_text(corpo, encoding="utf-8")
    return caminho
