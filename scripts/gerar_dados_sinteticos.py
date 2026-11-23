"""Gerador de dados SINTÉTICOS do LAB05 (issue #25).

ATENÇÃO: tudo o que este script produz é FALSO. Serve só para exercitar o
validador, a análise e o notebook antes da coleta. Nada aqui é resultado
(FONTE_DA_VERDADE §2.3 e §17).

Marcas obrigatórias dos dados sintéticos:
- arquivos com prefixo ``SINTETICO_``;
- coluna ``origem = sintetico`` em todas as tabelas (e no JSON da auditoria);
- URLs no domínio reservado ``.invalid`` (nunca o Portal real);
- gravação só em ``dados/sinteticos/`` (ou pasta indicada), nunca em ``resultados/``.

Efeitos PLANTADOS (conhecidos, para conferir se a análise os detecta):
- RQ1: probabilidade de concluir 0,92 no computador e 0,65 no celular;
- RQ2: log-tempo +0,35 no celular (razão geométrica ≈ 1,42), antes do teto;
- RQ3: SUS −10 pontos no celular;
- RQ4: taxa de erro por passo alcançado 0,45 (com violação) × 0,12 (sem).

Uso::

    python scripts/gerar_dados_sinteticos.py            # grava em dados/sinteticos/
    python scripts/gerar_dados_sinteticos.py --saida /tmp/x --semente 1
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import esquema as E  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
PASTA_PADRAO = RAIZ / "dados" / "sinteticos"

EFEITOS_PLANTADOS = {
    "p_conclusao": {"computador": 0.92, "celular": 0.65},
    "log_tempo_celular": 0.35,
    "sus_celular": -10.0,
    "taxa_erro_passo": {"com_violacao": 0.45, "sem_violacao_detectada": 0.12,
                        "indeterminado": 0.25},
}

TAREFAS = [f"{c}{i}" for c in E.CONJUNTOS for i in (1, 2, 3)]
PASSOS = ["p1", "p2", "p3", "p4"]
REGRAS_EXEMPLO = [
    ("color-contrast", "serious", ["cat.color", "wcag2aa", "wcag143"]),
    ("label", "critical", ["cat.forms", "wcag2a", "wcag412"]),
    ("link-name", "serious", ["cat.name-role-value", "wcag2a", "wcag244"]),
    ("button-name", "critical", ["cat.name-role-value", "wcag2a", "wcag412"]),
    ("target-size", "serious", ["cat.sensory-and-visual-cues", "wcag22aa", "wcag258"]),
    ("image-alt", "critical", ["cat.text-alternatives", "wcag2a", "wcag111"]),
    ("region", "moderate", ["cat.keyboard", "best-practice"]),
    ("heading-order", "moderate", ["cat.semantics", "best-practice"]),
]


def _pagina(tarefa: str, passo: str) -> str:
    if passo == "p1":
        return "https://sintetico.invalid/inicio"
    return f"https://sintetico.invalid/servico-{tarefa}"


def gerar_catalogo(rng: np.random.Generator) -> pd.DataFrame:
    linhas = []
    for t in TAREFAS:
        for d in E.DISPOSITIVOS:
            for k, passo in enumerate(PASSOS):
                if k == 0:
                    rot = "sem_violacao_detectada"
                else:
                    rot = rng.choice(E.ROTULOS_WCAG, p=[0.40, 0.50, 0.10])
                regras = ""
                if rot == "com_violacao":
                    r = REGRAS_EXEMPLO[rng.integers(0, 6)][0]
                    regras = r
                linhas.append({
                    "tarefa_id": t, "passo_id": passo, "dispositivo": d,
                    "pagina_url": _pagina(t, passo),
                    "elemento": f"elemento-sintetico-{t}-{passo}",
                    "rotulo_wcag": rot, "regras_axe": regras,
                    "motivo_indeterminado": ("elemento não identificável (sintético)"
                                             if rot == "indeterminado" else ""),
                    "origem": "sintetico",
                })
    return pd.DataFrame(linhas, columns=E.COLUNAS["catalogo_passos"])


def gerar_participantes(rng: np.random.Generator) -> pd.DataFrame:
    """3 piloto + 8 blocos de 4 + 2 reposições + 1 excedente na sequência 1."""
    linhas = []
    ordem = 0

    def novo(seq, bloco, piloto=False, valida=True, motivo=""):
        nonlocal ordem
        ordem += 1
        linhas.append({
            "participante": f"P{ordem:02d}", "sequencia": seq, "bloco": bloco,
            "ordem_realizacao": ordem,
            "data": str(pd.Timestamp("2026-12-01") + pd.Timedelta(days=ordem // 4))[:10],
            "faixa_etaria": rng.choice(E.FAIXAS_ETARIAS, p=[.4, .3, .15, .1, .05]),
            "uso_previo_portal": rng.choice(E.USO_PREVIO),
            "familiaridade_digital": str(rng.integers(2, 6)),
            "valida": int(valida), "motivo_invalida": motivo, "reposto_por": "",
            "piloto": int(piloto), "hash_ui_package": "SINTETICO-hash-0000",
            "versao_chrome": "000.0.0.0-sintetico", "versao_portal_obs": "sintetico",
            "o_que_mais_atrapalhou": "texto sintético", "notas_moderador": "",
            "origem": "sintetico",
        })
        return linhas[-1]

    for s in (1, 2, 3):
        novo(s, 0, piloto=True)
    invalidos = {(2, 3), (5, 2)}  # (bloco, sequência) com falha técnica
    pendentes = []
    for b in range(1, 9):
        for s in rng.permutation([1, 2, 3, 4]):
            s = int(s)
            if (b, s) in invalidos:
                pendentes.append(novo(s, b, valida=False,
                                      motivo="falha técnica (sintética)"))
            else:
                novo(s, b)
        for lin in list(pendentes):  # reposição na mesma sequência e bloco
            rep = novo(lin["sequencia"], lin["bloco"])
            lin["reposto_por"] = rep["participante"]
            pendentes.remove(lin)
    novo(1, 9)  # excedente: 9º analisável da sequência 1 (fora da análise primária)
    df = pd.DataFrame(linhas, columns=E.COLUNAS["participantes"])
    df.loc[df["piloto"] == 1, "bloco"] = 1
    return df


def _sus_itens(rng, alvo: float) -> list[int]:
    alvo = float(np.clip(alvo, 0, 100)) / 100
    itens = []
    for i in range(1, 11):
        if i % 2:  # ímpar: concordar = bom
            x = 1 + 4 * alvo + rng.normal(0, 0.6)
        else:
            x = 5 - 4 * alvo + rng.normal(0, 0.6)
        itens.append(int(np.clip(round(x), 1, 5)))
    return itens


def gerar_sessoes(rng, participantes, catalogo):
    ef = EFEITOS_PLANTADOS
    rot = catalogo.set_index(["tarefa_id", "passo_id", "dispositivo"])["rotulo_wcag"]
    efeito_tarefa = dict(zip(TAREFAS, rng.normal(0, 0.15, len(TAREFAS))))
    ses, sus, pas = [], [], []
    for _, p in participantes.iterrows():
        seq = E.SEQUENCIAS[int(p["sequencia"])]
        u_tempo = rng.normal(0, 0.35)
        u_sus = rng.normal(0, 10)
        ordem_disp = [seq["primeiro"]] + [d for d in E.DISPOSITIVOS if d != seq["primeiro"]]
        for periodo, disp in enumerate(ordem_disp, start=1):
            if not p["valida"] and periodo == 2:
                break  # sessão inválida interrompida no 1º dispositivo
            conj = seq[disp]
            tarefas = rng.permutation([f"{conj}{i}" for i in (1, 2, 3)])
            for ordem, t in enumerate(tarefas, start=1):
                t = str(t)
                falha = (not p["valida"]) and ordem == 3
                mu = (np.log(90) + u_tempo + efeito_tarefa[t] - 0.05 * (periodo - 1)
                      + (ef["log_tempo_celular"] if disp == "celular" else 0))
                tempo = float(np.exp(mu + rng.normal(0, 0.4)))
                conclui = rng.random() < ef["p_conclusao"][disp]
                if falha:
                    motivo, tempo = "falha_tecnica", round(min(tempo, 299.0) * 0.5, 1)
                elif conclui and tempo < E.TETO_S:
                    motivo, tempo = "concluida", round(tempo, 1)
                else:
                    motivo = rng.choice(["teto", "abandono", "ajuda"], p=[.6, .25, .15])
                    if tempo >= E.TETO_S:
                        motivo = "teto"
                    if motivo == "teto":
                        tempo = E.TETO_S
                    else:
                        tempo = round(min(tempo, 299.0) * rng.uniform(0.5, 1.0), 1)
                motivo = str(motivo)
                concluida = motivo == "concluida"
                n_alc = 4 if concluida else int(rng.integers(1, 5))
                erros_tarefa = 0
                for k, passo in enumerate(PASSOS):
                    alc = k < n_alc
                    taxa = ef["taxa_erro_passo"][rot[(t, passo, disp)]]
                    taxa *= 1.3 if disp == "celular" else 1.0
                    ne = int(rng.poisson(taxa)) if alc else 0
                    erros_tarefa += ne
                    pas.append({"participante": p["participante"], "dispositivo": disp,
                                "tarefa_id": t, "passo_id": passo, "alcancado": int(alc),
                                "n_erros": ne, "origem": "sintetico"})
                fora = int(rng.poisson(0.15))
                if fora:
                    erros_tarefa += fora
                    pas.append({"participante": p["participante"], "dispositivo": disp,
                                "tarefa_id": t, "passo_id": E.PASSO_FORA, "alcancado": 1,
                                "n_erros": fora, "origem": "sintetico"})
                seq_val = 6 - 0.8 * (disp == "celular") - 2 * (not concluida) + rng.normal(0, 1)
                ses.append({
                    "participante": p["participante"], "dispositivo": disp,
                    "conjunto": conj, "periodo": periodo, "tarefa_id": t,
                    "ordem_tarefa": ordem, "concluida": int(concluida),
                    "tempo_s": tempo, "motivo_fim": motivo,
                    "pediu_ajuda": int(motivo == "ajuda"), "erros": erros_tarefa,
                    "seq": int(np.clip(round(seq_val), 1, 7)), "origem": "sintetico",
                })
            if p["valida"]:
                alvo = 75 + u_sus + (ef["sus_celular"] if disp == "celular" else 0)
                itens = _sus_itens(rng, alvo)
                sus.append({"participante": p["participante"], "dispositivo": disp,
                            **{f"item_{i}": v for i, v in enumerate(itens, start=1)},
                            "origem": "sintetico"})
    return (pd.DataFrame(ses, columns=E.COLUNAS["sessoes"]),
            pd.DataFrame(sus, columns=E.COLUNAS["sus"]),
            pd.DataFrame(pas, columns=E.COLUNAS["passos"]))


def gerar_auditoria(rng, catalogo) -> tuple[pd.DataFrame, dict[str, dict]]:
    """JSONs no formato axe-core e Lighthouse (sintéticos) e o índice."""
    paginas = sorted(catalogo["pagina_url"].unique())
    indice, arquivos = [], {}
    for j, url in enumerate(paginas):
        slug = url.rsplit("/", 1)[-1]
        for modo in E.MODOS_AUDITORIA:
            k = int(rng.integers(1, 5))
            escolhidas = rng.choice(len(REGRAS_EXEMPLO), size=k, replace=False)
            viol = [{"id": REGRAS_EXEMPLO[i][0], "impact": REGRAS_EXEMPLO[i][1],
                     "tags": REGRAS_EXEMPLO[i][2],
                     "nodes": [{"target": [f"#sintetico-{n}"]}
                               for n in range(int(rng.integers(1, 6)))]}
                    for i in escolhidas]
            nome = f"axe/{E.PREFIXO_SINTETICO}axe_{slug}_{modo}.json"
            arquivos[nome] = {"origem": "sintetico", "aviso": "DADO SINTÉTICO",
                              "testEngine": {"name": "axe-core", "version": "0.0.0-sintetico"},
                              "url": url, "violations": viol}
            indice.append({"arquivo": nome, "pagina_url": url, "data": "2026-12-01",
                           "versao_chrome": "000.0.0.0-sintetico", "ferramenta": "axe",
                           "modo": modo, "execucao": 1, "origem": "sintetico"})
            for ex in (1, 2, 3):
                nome = f"lighthouse/{E.PREFIXO_SINTETICO}lh_{slug}_{modo}_{ex}.json"
                arquivos[nome] = {
                    "origem": "sintetico", "aviso": "DADO SINTÉTICO",
                    "lighthouseVersion": "0.0.0-sintetico", "requestedUrl": url,
                    "configSettings": {"formFactor": modo},
                    "categories": {"accessibility": {"score": round(float(rng.uniform(0.6, 0.98)), 2)}},
                    "audits": {
                        "largest-contentful-paint": {"numericValue": float(rng.lognormal(np.log(2800), 0.3))},
                        "cumulative-layout-shift": {"numericValue": float(rng.uniform(0, 0.3))},
                    },
                }
                indice.append({"arquivo": nome, "pagina_url": url, "data": "2026-12-01",
                               "versao_chrome": "000.0.0.0-sintetico", "ferramenta": "lighthouse",
                               "modo": modo, "execucao": ex, "origem": "sintetico"})
    return pd.DataFrame(indice, columns=E.COLUNAS_INDICE_AUDITORIA), arquivos


def gerar(semente: int = E.SEMENTE) -> dict:
    """Gera todas as tabelas sintéticas em memória (função pura, usada nos testes)."""
    rng = np.random.default_rng(semente)
    catalogo = gerar_catalogo(rng)
    participantes = gerar_participantes(rng)
    sessoes, sus, passos = gerar_sessoes(rng, participantes, catalogo)
    indice, jsons = gerar_auditoria(rng, catalogo)
    return {"participantes": participantes, "sessoes": sessoes, "sus": sus,
            "catalogo_passos": catalogo, "passos": passos,
            "_indice_auditoria": indice, "_jsons_auditoria": jsons}


def gravar(dados: dict, pasta: Path) -> list[Path]:
    """Grava o conjunto sintético. Recusa qualquer caminho dentro de resultados/."""
    pasta = Path(pasta).resolve()
    if "resultados" in pasta.parts:
        raise E.ErroDeDados("Dados sintéticos nunca são gravados em resultados/.")
    pasta.mkdir(parents=True, exist_ok=True)
    escritos = []
    for t in E.TABELAS_CSV:
        arq = pasta / E.nome_arquivo(t, sintetico=True)
        dados[t].to_csv(arq, index=False, lineterminator="\n")
        escritos.append(arq)
    aud = E.pasta_auditoria(pasta)
    for nome, conteudo in dados["_jsons_auditoria"].items():
        f = aud / nome
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(conteudo, ensure_ascii=False, indent=1), encoding="utf-8")
        escritos.append(f)
    idx = aud / f"{E.PREFIXO_SINTETICO}indice.csv"
    dados["_indice_auditoria"].to_csv(idx, index=False, lineterminator="\n")
    escritos.append(idx)
    # checksums (exercita a checagem de integridade do validador)
    from validar_dados import sha256  # import tardio evita ciclo

    linhas = [f"{sha256(f)}  {f.relative_to(pasta).as_posix()}" for f in escritos]
    (pasta / f"{E.PREFIXO_SINTETICO}CHECKSUMS.sha256").write_text(
        "\n".join(linhas) + "\n", encoding="utf-8")
    return escritos


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Gera dados SINTÉTICOS (falsos) do LAB05")
    ap.add_argument("--saida", type=Path, default=PASTA_PADRAO)
    ap.add_argument("--semente", type=int, default=E.SEMENTE)
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    escritos = gravar(gerar(args.semente), args.saida)
    print(f"{len(escritos)} arquivos SINTÉTICOS gravados em {args.saida} "
          f"(semente {args.semente}). Nada disso é resultado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
