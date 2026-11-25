"""Pipeline completo do LAB05: coleta → tratamento → análise → gráficos.

Um comando reproduz tudo, sem participantes e sem planilhas manuais::

    python scripts/pipeline.py

Variações:

    python scripts/pipeline.py --cache-dir ~/.cache/lab05   # guarda os CSVs (fora do repo)
    python scripts/pipeline.py --entrada ~/csvs_pbh         # usa CSVs já baixados, sem rede
    python scripts/pipeline.py --base dados/processados/solicitacoes_analiticas.csv.gz
                                                            # só análise, a partir da base pronta

Os CSVs originais têm logradouro, número e coordenadas: ficam sempre fora do
repositório (pasta temporária apagada ao final, ou ``--cache-dir`` externo).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import coleta  # noqa: E402
import config as C  # noqa: E402
import estatistica as E  # noqa: E402
import impacto as IMP  # noqa: E402
import tratamento as T  # noqa: E402
import visualizacao as V  # noqa: E402

NOME_BASE = "solicitacoes_analiticas.csv.gz"

# Tabelas da estimativa de impacto (issue #29): chave em ``r`` -> nome do CSV
NOMES_TABELAS_IMPACTO = {
    "volume_anual_por_canal": "volume_anual_por_canal",
    "impacto_por_servico": "impacto_por_servico_par",
    "impacto_por_par": "impacto_por_par",
}


def _jsonavel(x):
    if isinstance(x, dict):
        return {str(k): _jsonavel(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonavel(v) for v in x]
    if isinstance(x, pd.DataFrame):
        return _jsonavel(x.to_dict(orient="records"))
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return None if (math.isnan(x) or math.isinf(x)) else float(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (pd.Timestamp,)):
        return str(x.date())
    if x is pd.NA or x is pd.NaT:
        return None
    return x


def gravar_tabelas(r: dict, pasta: Path) -> list[Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    nomes = {
        "funil": "funil_elegibilidade", "status_por_canal": "status_por_canal",
        "por_canal": "metricas_por_canal", "servico_canal": "servico_x_canal",
        "pares_por_servico": "pares_por_servico", "omnibus_por_servico": "omnibus_por_servico",
        "estratificado_por_par": "pares_ajustados_por_servico",
        "sensibilidade_horizonte": "sensibilidade_horizonte",
    }
    nomes.update(NOMES_TABELAS_IMPACTO)
    saidas = []
    for chave, nome in nomes.items():
        df = r[chave]
        if isinstance(df, pd.DataFrame) and not df.empty:
            caminho = pasta / f"{nome}.csv"
            df.to_csv(caminho, index=False, float_format="%.6g")
            saidas.append(caminho)
    for chave, df in r["ranking_servicos"].items():
        if len(df):
            caminho = pasta / f"ranking_servicos_{chave}.csv"
            df.to_csv(caminho, index=False, float_format="%.6g")
            saidas.append(caminho)
    return saidas


def resumo_markdown(r: dict, q: dict) -> str:
    """Texto gerado dos números calculados (nada digitado à mão)."""
    p = r["parametros"]
    h = p["horizonte_dias"]
    pc = r["por_canal"]
    L = [f"# Resumo dos resultados (gerado por `scripts/pipeline.py`)\n",
         "> Gerado automaticamente a partir da base processada. Estudo observacional: "
         "associação, não causa.\n",
         f"- Período de criação: {q.get('periodo_criacao', ['?', '?'])[0]} a "
         f"{q.get('periodo_criacao', ['?', '?'])[1]}",
         f"- Parâmetros: horizonte = {h} dias; mínimo por célula = {p['min_celula']}; "
         f"α = {p['alfa']}\n", "## Funil de elegibilidade\n",
         "| Etapa | Registros |", "|---|---:|"]
    L += [f"| {a} | {V._fmt(b)} |" for a, b in zip(r["funil"]["etapa"], r["funil"]["registros"])]
    L += ["", "## Métricas por canal (população elegível)\n",
          f"| Canal | Solicitações | % encerrada (corte) | % encerrada ≤ {h} d | Mediana (d) | "
          "Q1–Q3 | P90 | Mediana KM (d) |", "|---|---:|---:|---:|---:|---|---:|---:|"]
    for _, x in pc.iterrows():
        km = "n/d" if pd.isna(x["mediana_km_dias"]) else f"{x['mediana_km_dias']:.0f}"
        L.append(f"| {x['rotulo']} | {V._fmt(x['solicitacoes'])} | "
                 f"{V._pct(x['taxa_encerramento_corte'])} | "
                 f"{V._pct(x[f'taxa_encerramento_{h}d'])} | {x['mediana_dias']:.0f} | "
                 f"{x['q1_dias']:.0f}–{x['q3_dias']:.0f} | {x['p90_dias']:.0f} | {km} |")
    L += ["", "n/d = a curva de Kaplan–Meier não chega a 50% (menos da metade encerrou).\n",
          "## Pares de canais ajustados por serviço\n",
          "A = primeiro canal. OR de Mantel–Haenszel > 1: A encerra mais em "
          f"{h} d. Delta de Cliff > 0: A mais lento. p com correção de Holm (6 pares).\n",
          "| Par (A × B) | Serviços (prop.) | OR MH [IC 95%] | p (CMH, Holm) | I² | "
          "Serviços (tempo) | Delta combinado [IC 95%] | Magnitude | "
          "Delta (ponderação alternativa) | Sinal consistente (D14) | p (van Elteren, Holm) |",
          "|---|---:|---|---|---:|---:|---|---|---:|---|---|"]
    for _, x in r["estratificado_por_par"].iterrows():
        par = f"{C.ROTULO_CANAL[x['canal_a']]} × {C.ROTULO_CANAL[x['canal_b']]}"
        orr = ("n/d" if pd.isna(x.get("or_mh")) else
               f"{x['or_mh']:.2f} [{x['or_ic_lo']:.2f}; {x['or_ic_hi']:.2f}]")
        dl = ("n/d" if pd.isna(x.get("delta_combinado")) else
              f"{x['delta_combinado']:.3f} [{x['delta_ic_lo']:.3f}; {x['delta_ic_hi']:.3f}]")
        harm = ("n/d" if pd.isna(x.get("delta_combinado_harmonico")) else
                f"{x['delta_combinado_harmonico']:.3f}")
        sc = x.get("delta_sinal_consistente")
        sinais = "n/d" if pd.isna(sc) else ("sim" if bool(sc) else "**inconclusivo**")
        L.append(f"| {par} | {int(x['servicos_prop'])} | {orr} | {V._p(x.get('p_cmh_holm'))} | "
                 f"{V._n(x.get('heterogeneidade_i2'))} | {int(x['servicos_tempo'])} | {dl} | "
                 f"{x.get('delta_magnitude', 'n/d')} | {harm} | {sinais} | "
                 f"{V._p(x.get('p_van_elteren_holm'))} |")
    L += ["", V.texto_robustez(r["estratificado_por_par"])]
    par = r["pares_por_servico"]
    if len(par):
        L += ["", "## Testes por serviço e par\n",
              f"- Pares (serviço × par de canais) testados: {len(par)}",
              f"- Proporção com p ajustado (Holm) < {p['alfa']}: {int(par['sig_prop'].sum())}",
              f"- Tempo com p ajustado (Holm) < {p['alfa']}: {int(par['sig_tempo'].sum())}",
              f"- Testes de proporção usados: {r['pressupostos']['testes_proporcao_por_servico']}",
              f"- Mediana da proporção de empates nos tempos: "
              f"{V._n(r['pressupostos']['empates_tempo_mediana_p_empate'], 3)}"]
    L += resumo_impacto(r)
    return "\n".join(L) + "\n"


def resumo_impacto(r: dict) -> list[str]:
    """Seção "Impacto estimado" do resumo (issue #29). Vazia se não há par de impacto."""
    return V.linhas_markdown_impacto(r) if "impacto_por_par" in r else []


def calcular_impacto(r: dict, params: C.Parametros) -> dict:
    """Estimativa de impacto (issue #29) a partir do resultado de ``analisar``."""
    el = r["elegiveis"]
    anos = IMP.anos_coorte(el)
    datas = pd.to_datetime(el["data_criacao"])
    por_servico = IMP.impacto_por_servico(r["pares_por_servico"], anos)
    return {
        "coorte": {"inicio": str(datas.min().date()), "fim": str(datas.max().date()),
                   "anos": float(anos)},
        "volume_anual_por_canal": IMP.volume_anual_por_canal(el),
        "impacto_por_servico": por_servico,
        "impacto_por_par": IMP.impacto_por_par(por_servico, params.semente),
    }


def executar(args: argparse.Namespace, log=print) -> dict:
    dados_dir = Path(args.dados_dir)
    saida = Path(args.saida)
    params = C.Parametros(horizonte_dias=args.horizonte_dias, min_celula=args.min_celula)
    tmp = None
    manifesto, qualidade = {}, {}

    if args.base:
        log(f"[1-2/4] Usando a base já processada: {args.base}")
        base = T.ler_base(Path(args.base))
        qpath = dados_dir / "qualidade_dados.json"
        if qpath.exists():
            qualidade = json.loads(qpath.read_text(encoding="utf-8"))
    else:
        if args.entrada:
            log(f"[1/4] Usando CSVs locais: {args.entrada}")
            caminhos, manifesto = coleta.descrever_arquivos_locais(Path(args.entrada))
        else:
            if args.cache_dir:
                destino = Path(args.cache_dir)
            else:
                tmp = tempfile.TemporaryDirectory(prefix="lab05_")
                destino = Path(tmp.name)
            log(f"[1/4] Coletando do CKAN da PBH para {destino}")
            caminhos, manifesto = coleta.coletar(destino, log=log)
        try:
            log("[2/4] Tratando (colunas de endereço descartadas na leitura)")
            base, qualidade = T.processar(caminhos, log=log)
        finally:
            if tmp is not None:
                tmp.cleanup()  # apaga os CSVs brutos
                log("      CSVs brutos apagados.")
        destino_base = dados_dir / "processados" / NOME_BASE
        T.gravar_base(base, destino_base)
        log(f"      base anonimizada: {destino_base} ({len(base):,} linhas)".replace(",", "."))
        manifesto["gerado_em_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        manifesto["sha256_base_analitica"] = coleta.sha256_arquivo(destino_base)
        dados_dir.mkdir(parents=True, exist_ok=True)
        (dados_dir / "manifesto_coleta.json").write_text(
            json.dumps(_jsonavel(manifesto), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (dados_dir / "qualidade_dados.json").write_text(
            json.dumps(_jsonavel(qualidade), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    log("[3/4] Analisando")
    r = E.analisar(base, params)
    r.update(calcular_impacto(r, params))
    tabelas = gravar_tabelas(r, saida / "tabelas")
    resumo = {k: _jsonavel(v) for k, v in r.items()
              if k not in ("elegiveis", "celulas", "servico_canal", "pares_por_servico",
                           "omnibus_por_servico")}
    resumo.pop("impacto_por_servico", None)  # granular: já sai em CSV (como pares_por_servico)
    (saida / "resultados.json").parent.mkdir(parents=True, exist_ok=True)
    (saida / "resultados.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (saida / "resumo.md").write_text(resumo_markdown(r, qualidade), encoding="utf-8")

    log("[4/4] Gerando gráficos e painel")
    figuras = V.gerar_figuras(r, saida / "figuras")
    painel = V.gerar_painel(r, figuras, qualidade, saida / "painel.html")
    log(f"Pronto. Painel: {painel}")
    return {"resultado": r, "base": base, "tabelas": tabelas, "figuras": figuras,
            "painel": painel}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    fonte = ap.add_mutually_exclusive_group()
    fonte.add_argument("--cache-dir", help="pasta FORA do repositório para guardar os CSVs baixados")
    fonte.add_argument("--entrada", help="pasta com CSVs já baixados (sem acessar a rede)")
    fonte.add_argument("--base", help="base analítica já gerada (.csv.gz): só a análise")
    ap.add_argument("--horizonte-dias", type=int, default=C.Parametros.horizonte_dias)
    ap.add_argument("--min-celula", type=int, default=C.Parametros.min_celula)
    ap.add_argument("--dados-dir", default=str(C.RAIZ / "dados"))
    ap.add_argument("--saida", default=str(C.RAIZ / "resultados"))
    args = ap.parse_args(argv)
    try:
        executar(args)
    except (coleta.ErroDeColeta, T.ErroDeDados) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
