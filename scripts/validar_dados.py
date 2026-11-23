"""Validador dos dados do LAB05 (issue #25).

Confere esquema, domínios e regras de coerência descritos em
``dados/dicionario_de_dados.md`` (PROPOSTA, a confirmar com o papel B).

Uso::

    python scripts/validar_dados.py dados/brutos
    python scripts/validar_dados.py dados/sinteticos --relatorio saida.md

Código de saída 0 = nenhum erro; 1 = há erros. Avisos não reprovam.

Importante (FONTE_DA_VERDADE §2.3): passar neste script NÃO torna o dado
"Verificado". "Verificado" exige conferência por segunda pessoa, com registro.
O script só automatiza checagens mecânicas.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import esquema as E  # noqa: E402


@dataclass(frozen=True)
class Achado:
    nivel: str  # "erro" | "aviso" | "info"
    tabela: str
    regra: str
    mensagem: str


def _erro(tabela, regra, msg):
    return Achado("erro", tabela, regra, msg)


def _aviso(tabela, regra, msg):
    return Achado("aviso", tabela, regra, msg)


def _info(tabela, regra, msg):
    return Achado("info", tabela, regra, msg)


def _amostra(valores, k=5) -> str:
    v = list(valores)
    txt = ", ".join(str(x) for x in v[:k])
    return txt + (f" … (+{len(v) - k})" if len(v) > k else "")


# ---------------------------------------------------------------------------
# Checagens genéricas
# ---------------------------------------------------------------------------

RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
RE_TELEFONE = re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b")


def checar_colunas(nome: str, df: pd.DataFrame, colunas: list[str]) -> list[Achado]:
    """Presença das colunas obrigatórias e ausência de colunas de dado pessoal."""
    out = []
    if df.attrs.get("ausente"):
        return [_erro(nome, "arquivo", "tabela ausente")]
    faltam = [c for c in colunas if c not in df.columns]
    if faltam:
        out.append(_erro(nome, "esquema", f"colunas ausentes: {faltam}"))
    for c in df.columns:
        cl = c.lower()
        if any(t in cl for t in E.TRECHOS_COLUNA_PROIBIDA):
            out.append(_erro(nome, "dado_pessoal",
                             f"coluna proibida (possível dado pessoal): '{c}'"))
    extras = [c for c in df.columns if c not in colunas]
    if extras:
        out.append(_aviso(nome, "esquema", f"colunas não previstas: {extras}"))
    return out


def checar_dominio(nome, df, coluna, permitidos, regra="dominio",
                   vazio_ok=False) -> list[Achado]:
    if coluna not in df.columns:
        return []
    v = df[coluna].astype(str).str.strip()
    mask = ~v.isin([str(p) for p in permitidos])
    if vazio_ok:
        mask &= v != ""
    if mask.any():
        return [_erro(nome, regra, f"'{coluna}' fora do domínio "
                      f"{list(permitidos)}: {_amostra(sorted(set(v[mask])))}")]
    return []


def checar_inteiro(nome, df, coluna, minimo=None, maximo=None) -> list[Achado]:
    if coluna not in df.columns:
        return []
    num = pd.to_numeric(df[coluna], errors="coerce")
    ruim = num.isna() | (num != num.round())
    if minimo is not None:
        ruim |= num < minimo
    if maximo is not None:
        ruim |= num > maximo
    if ruim.any():
        return [_erro(nome, "dominio", f"'{coluna}' deve ser inteiro em "
                      f"[{minimo}, {maximo}]: {_amostra(df.loc[ruim, coluna])}")]
    return []


def checar_origem(tabelas: dict[str, pd.DataFrame], sintetico: bool) -> list[Achado]:
    """Origem única em todas as tabelas e coerente com o nome dos arquivos."""
    try:
        E.exigir_origem_unica(tabelas, sintetico)
    except E.ErroDeDados as exc:
        return [_erro("*", "origem", str(exc))]
    return []


def checar_texto_livre(nome, df, colunas) -> list[Achado]:
    """Triagem de dado pessoal em texto livre (e-mail, CPF, telefone)."""
    out = []
    for c in colunas:
        if c not in df.columns:
            continue
        for i, txt in df[c].astype(str).items():
            for rot, rex in (("e-mail", RE_EMAIL), ("CPF", RE_CPF),
                             ("telefone", RE_TELEFONE)):
                if rex.search(txt):
                    out.append(_erro(nome, "dado_pessoal",
                                     f"linha {i + 2}, '{c}': padrão de {rot}"))
    return out


# ---------------------------------------------------------------------------
# Checagens por tabela
# ---------------------------------------------------------------------------

def checar_participantes(p: pd.DataFrame) -> list[Achado]:
    n = "participantes"
    out = []
    if "participante" in p.columns:
        ids = p["participante"].astype(str)
        ruins = ids[~ids.str.fullmatch(r"P\d{2}")]
        if len(ruins):
            out.append(_erro(n, "dominio", f"código fora de P\\d\\d: {_amostra(ruins)}"))
        dup = ids[ids.duplicated()]
        if len(dup):
            out.append(_erro(n, "unicidade", f"participante repetido: {_amostra(dup)}"))
    out += checar_dominio(n, p, "sequencia", [1, 2, 3, 4])
    out += checar_inteiro(n, p, "bloco", 1, None)
    out += checar_inteiro(n, p, "ordem_realizacao", 1, None)
    if "ordem_realizacao" in p.columns and p["ordem_realizacao"].duplicated().any():
        out.append(_erro(n, "unicidade", "ordem_realizacao repetida"))
    out += checar_dominio(n, p, "valida", ["0", "1"])
    out += checar_dominio(n, p, "piloto", ["0", "1"])
    out += checar_dominio(n, p, "faixa_etaria", E.FAIXAS_ETARIAS, vazio_ok=True)
    out += checar_dominio(n, p, "uso_previo_portal", E.USO_PREVIO, vazio_ok=True)
    out += checar_dominio(n, p, "familiaridade_digital", E.FAMILIARIDADE, vazio_ok=True)
    if "data" in p.columns:
        d = pd.to_datetime(p["data"], format="%Y-%m-%d", errors="coerce")
        if d.isna().any():
            out.append(_erro(n, "dominio", "data fora do formato AAAA-MM-DD: "
                             + _amostra(p.loc[d.isna(), "data"])))
    if {"valida", "motivo_invalida"} <= set(p.columns):
        sem_motivo = p[(p["valida"] == "0") & (p["motivo_invalida"].str.strip() == "")]
        if len(sem_motivo):
            out.append(_erro(n, "coerencia", "sessão inválida sem motivo_invalida: "
                             + _amostra(sem_motivo["participante"])))
    if {"reposto_por", "participante"} <= set(p.columns):
        ids = set(p["participante"])
        alvo = p["reposto_por"].str.strip()
        ruins = alvo[(alvo != "") & ~alvo.isin(ids)]
        if len(ruins):
            out.append(_erro(n, "referencia", f"reposto_por inexistente: {_amostra(ruins)}"))
        if {"sequencia", "valida"} <= set(p.columns):
            seq = dict(zip(p["participante"], p["sequencia"]))
            for _, lin in p[(alvo != "") & alvo.isin(ids)].iterrows():
                if seq[lin["reposto_por"]] != lin["sequencia"]:
                    out.append(_erro(n, "reposicao", f"{lin['participante']} reposto "
                                     f"por {lin['reposto_por']} em outra sequência"))
                if lin["valida"] != "0":
                    out.append(_aviso(n, "reposicao", f"{lin['participante']} tem "
                                      "reposto_por, mas está marcado como válido"))
    out += checar_texto_livre(n, p, ["o_que_mais_atrapalhou", "notas_moderador",
                                      "motivo_invalida"])
    return out


def contagem_por_sequencia(p: pd.DataFrame) -> list[Achado]:
    """Analisáveis (válidos, fora do piloto) por sequência, contra a meta de 8."""
    if not {"sequencia", "valida", "piloto"} <= set(p.columns):
        return []
    ok = p[(p["valida"] == "1") & (p["piloto"] == "0")]
    cont = ok["sequencia"].astype(str).value_counts().reindex(
        ["1", "2", "3", "4"], fill_value=0)
    txt = ", ".join(f"seq {s}: {c}" for s, c in cont.items())
    out = [_info("participantes", "contagem", f"analisáveis por sequência: {txt} "
                 f"(meta {E.META_POR_SEQUENCIA})")]
    abaixo = cont[cont < E.META_POR_SEQUENCIA]
    acima = cont[cont > E.META_POR_SEQUENCIA]
    if len(abaixo):
        out.append(_aviso("participantes", "contagem",
                          f"sequências abaixo da meta: { {k: int(v) for k, v in abaixo.items()} } (regra P2, item 4)"))
    if len(acima):
        out.append(_aviso("participantes", "contagem",
                          f"sequências com excedentes: { {k: int(v) for k, v in acima.items()} } (regra P2, item 3)"))
    return out


def checar_sessoes(s: pd.DataFrame, p: pd.DataFrame) -> list[Achado]:
    n = "sessoes"
    out = []
    out += checar_dominio(n, s, "dispositivo", E.DISPOSITIVOS)
    out += checar_dominio(n, s, "conjunto", E.CONJUNTOS)
    out += checar_dominio(n, s, "periodo", [1, 2])
    out += checar_dominio(n, s, "ordem_tarefa", [1, 2, 3])
    out += checar_dominio(n, s, "concluida", ["0", "1"])
    out += checar_dominio(n, s, "pediu_ajuda", ["0", "1"])
    out += checar_dominio(n, s, "motivo_fim", E.MOTIVOS_FIM)
    out += checar_inteiro(n, s, "erros", 0, None)
    out += checar_inteiro(n, s, "seq", 1, 7)
    if any(r.nivel == "erro" for r in out) or s.empty:
        return out  # sem domínio válido, as regras abaixo não fazem sentido

    t = pd.to_numeric(s["tempo_s"], errors="coerce")
    ruim = t.isna() | (t <= 0) | (t > E.TETO_S)
    if ruim.any():
        out.append(_erro(n, "tempo", f"tempo_s fora de (0, 300]: {_amostra(s.loc[ruim, 'tempo_s'])}"))
    teto = s["motivo_fim"] == "teto"
    no_teto = t == E.TETO_S
    if (teto != no_teto).any():
        lin = s[teto != no_teto]
        out.append(_erro(n, "teto", "tempo_s = 300 deve ocorrer se e somente se "
                         f"motivo_fim = teto: {_amostra(lin['participante'] + '/' + lin['tarefa_id'])}"))
    conc = s["concluida"] == "1"
    if (conc != (s["motivo_fim"] == "concluida")).any():
        out.append(_erro(n, "conclusao", "concluida = 1 se e somente se motivo_fim = concluida"))
    ajuda = s["pediu_ajuda"] == "1"
    if (ajuda & conc).any():
        out.append(_erro(n, "ajuda", "pedido de ajuda implica não conclusão"))
    if ((s["motivo_fim"] == "ajuda") & ~ajuda).any():
        out.append(_erro(n, "ajuda", "motivo_fim = ajuda exige pediu_ajuda = 1"))

    # tarefa_id: conjunto + número (A1..A3, B1..B3) e coerente com 'conjunto'
    ruim_id = ~s["tarefa_id"].str.fullmatch(r"[AB][1-3]")
    if ruim_id.any():
        out.append(_erro(n, "dominio", f"tarefa_id fora de [AB][1-3]: {_amostra(s.loc[ruim_id, 'tarefa_id'])}"))
    elif (s["tarefa_id"].str[0] != s["conjunto"]).any():
        out.append(_erro(n, "coerencia", "tarefa_id não pertence ao conjunto informado"))

    if p.empty or not {"participante", "sequencia", "valida"} <= set(p.columns):
        return out
    info = p.set_index("participante")
    desconhecidos = sorted(set(s["participante"]) - set(info.index))
    if desconhecidos:
        out.append(_erro(n, "referencia", f"participante sem cadastro: {_amostra(desconhecidos)}"))
        return out

    # sequência coerente com conjunto, dispositivo e período
    seq = s["participante"].map(info["sequencia"]).astype(int)
    conj_esp = [E.SEQUENCIAS[q][d] for q, d in zip(seq, s["dispositivo"])]
    per_esp = [1 if E.SEQUENCIAS[q]["primeiro"] == d else 2
               for q, d in zip(seq, s["dispositivo"])]
    ruim_c = s["conjunto"].to_numpy() != pd.Series(conj_esp).to_numpy()
    ruim_p = s["periodo"].astype(int).to_numpy() != pd.Series(per_esp).to_numpy()
    if ruim_c.any() or ruim_p.any():
        lin = s[ruim_c | ruim_p]
        out.append(_erro(n, "sequencia", "conjunto/período incoerente com a sequência: "
                         + _amostra(lin["participante"].unique())))

    valida = s["participante"].map(info["valida"]) == "1"
    falha = s["motivo_fim"] == "falha_tecnica"
    if (falha & valida).any():
        out.append(_erro(n, "falha_tecnica", "falha técnica em participante marcado "
                         "como válido (sessão deve ser inválida e reposta, P2 item 1): "
                         + _amostra(s.loc[falha & valida, "participante"].unique())))

    # completude: 3 tarefas distintas por dispositivo, ordens 1-3, 2 dispositivos
    sv = s[valida]
    for (part, disp), g in sv.groupby(["participante", "dispositivo"]):
        if (len(g) != E.N_TAREFAS_POR_DISPOSITIVO or g["tarefa_id"].nunique() != 3
                or sorted(g["ordem_tarefa"].astype(int)) != [1, 2, 3]):
            out.append(_erro(n, "completude", f"{part}/{disp}: são exigidas 3 tarefas "
                             "distintas com ordem_tarefa 1, 2 e 3"))
    disp_por_part = sv.groupby("participante")["dispositivo"].nunique()
    faltando = sorted(set(info.index[info["valida"] == "1"])
                      - set(disp_por_part[disp_por_part == 2].index))
    if faltando:
        out.append(_erro(n, "completude", f"válidos sem os dois dispositivos: {_amostra(faltando)}"))
    return out


def checar_sus(u: pd.DataFrame, p: pd.DataFrame) -> list[Achado]:
    n = "sus"
    out = checar_dominio(n, u, "dispositivo", E.DISPOSITIVOS)
    for i in range(1, 11):
        out += checar_dominio(n, u, f"item_{i}", ["1", "2", "3", "4", "5"])
    if u.duplicated(["participante", "dispositivo"]).any():
        out.append(_erro(n, "unicidade", "mais de um SUS por participante e dispositivo"))
    if not p.empty and {"participante", "valida"} <= set(p.columns):
        validos = set(p.loc[p["valida"] == "1", "participante"])
        cont = u[u["participante"].isin(validos)].groupby("participante").size()
        falt = sorted(v for v in validos if cont.get(v, 0) != 2)
        if falt:
            out.append(_erro(n, "completude", f"válidos sem 2 SUS: {_amostra(falt)}"))
        desconhecidos = sorted(set(u["participante"]) - set(p["participante"]))
        if desconhecidos:
            out.append(_erro(n, "referencia", f"participante sem cadastro: {_amostra(desconhecidos)}"))
    return out


def checar_catalogo(c: pd.DataFrame) -> list[Achado]:
    n = "catalogo_passos"
    out = checar_dominio(n, c, "dispositivo", E.DISPOSITIVOS)
    out += checar_dominio(n, c, "rotulo_wcag", E.ROTULOS_WCAG)
    if c.empty:
        return out
    if c.duplicated(["tarefa_id", "passo_id", "dispositivo"]).any():
        out.append(_erro(n, "unicidade", "passo repetido (tarefa_id, passo_id, dispositivo)"))
    if (c["passo_id"] == E.PASSO_FORA).any():
        out.append(_erro(n, "dominio", f"'{E.PASSO_FORA}' é reservado e não entra no catálogo"))
    ind = c["rotulo_wcag"] == "indeterminado"
    if (ind & (c["motivo_indeterminado"].str.strip() == "")).any():
        out.append(_erro(n, "coerencia", "passo indeterminado sem motivo_indeterminado"))
    com = c["rotulo_wcag"] == "com_violacao"
    if (com & (c["regras_axe"].str.strip() == "")).any():
        out.append(_erro(n, "coerencia", "passo com violação sem regras_axe "
                         "(use 'manual:<critério>' para violação do checklist)"))
    return out


def checar_passos(ps: pd.DataFrame, c: pd.DataFrame, s: pd.DataFrame) -> list[Achado]:
    n = "passos"
    out = checar_dominio(n, ps, "dispositivo", E.DISPOSITIVOS)
    out += checar_dominio(n, ps, "alcancado", ["0", "1"])
    out += checar_inteiro(n, ps, "n_erros", 0, None)
    if any(r.nivel == "erro" for r in out) or ps.empty:
        return out
    chave = ["tarefa_id", "passo_id", "dispositivo"]
    dentro = ps[ps["passo_id"] != E.PASSO_FORA]
    if not c.empty:
        cat = set(map(tuple, c[chave].to_numpy()))
        faltam = [k for k in map(tuple, dentro[chave].to_numpy()) if k not in cat]
        if faltam:
            out.append(_erro(n, "catalogo", f"passos fora do catálogo: {_amostra(sorted(set(faltam)))}"))
    if ps.duplicated(["participante"] + chave).any():
        out.append(_erro(n, "unicidade", "linha repetida (participante, tarefa, passo, dispositivo)"))
    erro_sem_alc = (ps["alcancado"] == "0") & (pd.to_numeric(ps["n_erros"]) > 0)
    if erro_sem_alc.any():
        out.append(_erro(n, "coerencia", "erro registrado em passo não alcançado"))
    if not s.empty:
        k = ["participante", "dispositivo", "tarefa_id"]
        soma = ps.assign(n_erros=pd.to_numeric(ps["n_erros"])).groupby(k)["n_erros"].sum()
        ses = s.assign(erros=pd.to_numeric(s["erros"])).set_index(k)["erros"]
        comp = pd.concat([soma.rename("passos"), ses.rename("sessao")], axis=1).fillna(0)
        dif = comp[comp["passos"] != comp["sessao"]]
        if len(dif):
            out.append(_erro(n, "soma_erros", "soma de n_erros dos passos ≠ erros da tarefa "
                             f"em {len(dif)} tarefa(s): {_amostra(['/'.join(i) for i in dif.index])}"))
    return out


def checar_auditoria(pasta: Path, sintetico: bool) -> list[Achado]:
    n = "auditoria"
    idx = E.carregar_indice_auditoria(pasta, sintetico)
    if idx is None:
        return [_aviso(n, "arquivo", "auditoria/indice.csv ausente (auditoria pendente, P12)")]
    out = checar_colunas(n, idx, E.COLUNAS_INDICE_AUDITORIA)
    out += checar_dominio(n, idx, "ferramenta", E.FERRAMENTAS_AUDITORIA)
    out += checar_dominio(n, idx, "modo", E.MODOS_AUDITORIA)
    out += checar_dominio(n, idx, "execucao", [1, 2, 3])
    esperado = "sintetico" if sintetico else "real"
    if "origem" in idx.columns and set(idx["origem"]) != {esperado}:
        out.append(_erro(n, "origem", f"origem do índice ≠ '{esperado}'"))
    base = E.pasta_auditoria(pasta)
    for arq in idx.get("arquivo", []):
        f = base / arq
        if not f.exists():
            out.append(_erro(n, "arquivo", f"JSON listado no índice não existe: {arq}"))
            continue
        if sintetico != Path(arq).name.startswith(E.PREFIXO_SINTETICO):
            out.append(_erro(n, "origem", f"nome do JSON incoerente com a origem: {arq}"))
        try:
            conteudo = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            out.append(_erro(n, "json", f"{arq}: JSON inválido ({exc})"))
            continue
        if sintetico and isinstance(conteudo, dict) and conteudo.get("origem") != "sintetico":
            out.append(_erro(n, "origem", f"{arq}: JSON sintético sem origem=sintetico"))
    return out


# ---------------------------------------------------------------------------
# Checksums dos brutos
# ---------------------------------------------------------------------------

def sha256(arq: Path) -> str:
    h = hashlib.sha256()
    with open(arq, "rb") as fh:
        for bloco in iter(lambda: fh.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def localizar_checksums(pasta: Path) -> Path | None:
    pasta = Path(pasta)
    for cand in (pasta / "CHECKSUMS.sha256",
                 pasta / f"{E.PREFIXO_SINTETICO}CHECKSUMS.sha256",
                 pasta.parent / "CHECKSUMS.sha256"):
        if cand.exists():
            return cand
    return None


def checar_checksums(pasta: Path, sintetico: bool) -> list[Achado]:
    """Formato ``<sha256>  <caminho relativo à pasta do arquivo de checksums>``."""
    n = "checksums"
    arq = localizar_checksums(pasta)
    if arq is None:
        if sintetico:
            return [_aviso(n, "arquivo", "sem arquivo de checksums")]
        return [_erro(n, "arquivo", "dados/CHECKSUMS.sha256 ausente: brutos sem "
                      "registro de integridade")]
    out = []
    linhas = [l for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
    for l in linhas:
        partes = l.split(maxsplit=1)
        if len(partes) != 2:
            out.append(_erro(n, "formato", f"linha inválida: {l!r}"))
            continue
        esperado, rel = partes[0], partes[1].lstrip("*").strip()
        f = arq.parent / rel
        if not f.exists():
            out.append(_erro(n, "arquivo", f"arquivo listado não existe: {rel}"))
        elif sha256(f) != esperado:
            out.append(_erro(n, "integridade", f"checksum diferente (bruto alterado?): {rel}"))
    if not out:
        out.append(_info(n, "integridade", f"{len(linhas)} arquivo(s) conferidos em {arq.name}"))
    return out


# ---------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------

def validar_tabelas(tabelas: dict[str, pd.DataFrame], sintetico: bool) -> list[Achado]:
    """Checagens que dependem só das tabelas (função pura, usada nos testes)."""
    out = []
    for nome, cols in E.COLUNAS.items():
        out += checar_colunas(nome, tabelas[nome], cols)
    if any(a.nivel == "erro" and a.regra in ("esquema", "arquivo") for a in out):
        return out
    out += checar_origem(tabelas, sintetico)
    p = tabelas["participantes"]
    out += checar_participantes(p)
    out += contagem_por_sequencia(p)
    out += checar_sessoes(tabelas["sessoes"], p)
    out += checar_sus(tabelas["sus"], p)
    out += checar_catalogo(tabelas["catalogo_passos"])
    out += checar_passos(tabelas["passos"], tabelas["catalogo_passos"], tabelas["sessoes"])
    cat = tabelas["catalogo_passos"]
    if not cat.empty:
        h = hashlib.sha256(cat.to_csv(index=False).encode("utf-8")).hexdigest()[:16]
        out.append(_info("catalogo_passos", "congelamento",
                         f"hash do catálogo (registrar no commit de congelamento): {h}"))
    return out


def validar(pasta: Path) -> tuple[list[Achado], bool]:
    pasta = Path(pasta)
    try:
        tabelas, sintetico = E.carregar_tabelas(pasta)
    except E.ErroDeDados as exc:
        return [_erro("*", "origem", str(exc))], False
    out = validar_tabelas(tabelas, sintetico)
    out += checar_auditoria(pasta, sintetico)
    out += checar_checksums(pasta, sintetico)
    return out, sintetico


def formatar_relatorio(achados: list[Achado], pasta: Path, sintetico: bool) -> str:
    n_err = sum(a.nivel == "erro" for a in achados)
    n_av = sum(a.nivel == "aviso" for a in achados)
    linhas = [
        "# Relatório de validação dos dados — LAB05",
        "",
        f"Pasta: `{pasta}` · origem: **{'SINTÉTICA' if sintetico else 'real'}**",
        "",
    ]
    if sintetico:
        linhas += ["> DADOS SINTÉTICOS. Nada aqui é resultado.", ""]
    linhas += [
        "> Passar nesta validação não torna o dado \"Verificado\" "
        "(FONTE_DA_VERDADE §2.3): é preciso conferência por segunda pessoa.",
        "",
        f"Erros: **{n_err}** · avisos: **{n_av}**",
        "",
        "| Nível | Tabela | Regra | Mensagem |",
        "|---|---|---|---|",
    ]
    for a in sorted(achados, key=lambda a: ("erro", "aviso", "info").index(a.nivel)):
        msg = a.mensagem.replace("|", "\\|")
        linhas.append(f"| {a.nivel} | {a.tabela} | {a.regra} | {msg} |")
    return "\n".join(linhas) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pasta", type=Path, help="pasta com as tabelas (dados/brutos ou dados/sinteticos)")
    ap.add_argument("--relatorio", type=Path, help="grava o relatório em Markdown neste caminho")
    args = ap.parse_args(argv)
    achados, sintetico = validar(args.pasta)
    rel = formatar_relatorio(achados, args.pasta, sintetico)
    if args.relatorio:
        args.relatorio.parent.mkdir(parents=True, exist_ok=True)
        args.relatorio.write_text(rel, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(rel)
    return 1 if any(a.nivel == "erro" for a in achados) else 0


if __name__ == "__main__":
    raise SystemExit(main())
