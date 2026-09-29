# -*- coding: utf-8 -*-
"""
Monta as tabelas-base da monografia a partir dos dados coletados
(comtrade_coleta.py, tiva_coleta.py, USGS transcrito).

Tabelas geradas em ../tratados:
  T1_china_destinos_ranking.csv   ranking de destinos das exportações da China,
                                  média 2013-2017 x média 2019-2024, TOTAL e HS 8541+8542
  T2_eua_origens_share.csv        participação por origem nas importações dos EUA,
                                  por ano, TOTAL e HS 8541+8542 (replica a lógica de
                                  Freund et al. 2024 só para semicondutores)
  T3_tiva_C26.csv                 TiVA: exportações brutas, VA doméstico e estrangeiro
                                  em C26, CHN/KOR/TWN/USA, 2005-2022, níveis e shares
  resumo_tabelas.md               leitura rápida dos resultados

Convenções: valores da Comtrade em US$ correntes; Taiwan = "Other Asia, nes"
(código 490) na Comtrade e "Chinese Taipei" (TWN) na TiVA. Semicondutores =
HS 8541 + 8542 menos o grupo 8541.4 (fotossensíveis/fotovoltaicas/LEDs; 854140 até
2021, 854141-49 desde 2022).
"""
import csv, os, sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
TRAT = os.path.join(AQUI, "..", "tratados")
PRE, POS = range(2013, 2018), range(2019, 2025)   # 2018 é o ano de transição, fica fora
NOMES = {490: "Taiwan (Other Asia, nes)", 0: "Mundo"}


def carregar_comtrade():
    arq = os.path.join(TRAT, "comtrade_consolidado.csv")
    if not os.path.exists(arq):
        sys.exit("rode comtrade_coleta.py antes")
    d = defaultdict(float)   # (reporter, flow, grupo, ano, partnerCode) -> valor
    nomes = {}
    for r in csv.DictReader(open(arq, encoding="utf-8")):
        # SEMICOND = 8541 + 8542 menos o grupo 8541.4 (dispositivos fotossensíveis,
        # células fotovoltaicas e LEDs): 854140 até 2021 e 854141/42/43/49 desde a
        # revisão HS 2022. Exclusão consistente no tempo; próxima da definição da SIA.
        cmd = r["cmdCode"]
        if cmd == "TOTAL":
            grupo, sinal = "TOTAL", 1.0
        elif cmd.startswith("85414"):
            grupo, sinal = "SEMICOND", -1.0
        else:
            grupo, sinal = "SEMICOND", 1.0
        p = int(r["partnerCode"]); nomes[p] = NOMES.get(p, r["partnerDesc"])
        try:
            d[(r["reporterCode"], r["flowCode"], grupo, int(r["refYear"]), p)] += sinal * float(r["primaryValue"] or 0)
        except ValueError:
            pass
    return d, nomes


def media(d, rep, flow, grupo, anos, p):
    vals = [d.get((rep, flow, grupo, a, p)) for a in anos]
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def t1_china_destinos(d, nomes):
    """Ranking de destinos das exportações chinesas, pré x pós 2018."""
    saida = []
    for grupo in ("TOTAL", "SEMICOND"):
        parceiros = {p for (rep, fl, g, a, p) in d if rep == "156" and fl == "X" and g == grupo and p != 0}
        mundo_pre = media(d, "156", "X", grupo, PRE, 0); mundo_pos = media(d, "156", "X", grupo, POS, 0)
        linhas = []
        for p in parceiros:
            pre = media(d, "156", "X", grupo, PRE, p); pos = media(d, "156", "X", grupo, POS, p)
            if pre is None and pos is None:
                continue
            linhas.append({"grupo": grupo, "partnerCode": p, "destino": nomes.get(p, p),
                           "media_2013_17_usd": pre, "media_2019_24_usd": pos,
                           "share_pre_%": 100 * pre / mundo_pre if pre and mundo_pre else None,
                           "share_pos_%": 100 * pos / mundo_pos if pos and mundo_pos else None})
        linhas.sort(key=lambda x: -(x["media_2013_17_usd"] or 0))
        for i, l in enumerate(linhas, 1): l["rank_pre"] = i
        linhas.sort(key=lambda x: -(x["media_2019_24_usd"] or 0))
        for i, l in enumerate(linhas, 1): l["rank_pos"] = i; l["var_rank"] = l["rank_pre"] - i
        saida += linhas[:30]
    campos = ["grupo", "rank_pos", "rank_pre", "var_rank", "destino", "partnerCode",
              "media_2013_17_usd", "media_2019_24_usd", "share_pre_%", "share_pos_%"]
    with open(os.path.join(TRAT, "T1_china_destinos_ranking.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(saida)
    return saida


def t2_eua_origens(d, nomes):
    """Participação de origens selecionadas nas importações dos EUA, por ano."""
    origens = {156: "China", 490: "Taiwan", 410: "Coreia do Sul", 704: "Vietnã", 484: "México",
               458: "Malásia", 392: "Japão", 76: "Brasil"}
    saida = []
    for grupo in ("TOTAL", "SEMICOND"):
        for ano in range(1995, 2025):
            mundo = d.get(("842", "M", grupo, ano, 0))
            if not mundo:
                continue
            linha = {"grupo": grupo, "ano": ano, "mundo_usd": mundo}
            for p, n in origens.items():
                v = d.get(("842", "M", grupo, ano, p))
                linha[f"{n}_%"] = round(100 * v / mundo, 4) if v else None
            saida.append(linha)
    campos = ["grupo", "ano", "mundo_usd"] + [f"{n}_%" for n in origens.values()]
    with open(os.path.join(TRAT, "T2_eua_origens_share.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(saida)
    return saida


def t4_hhi(d):
    """Índice de Herfindahl-Hirschman das origens das importações dos EUA (0-10.000),
    calculado sobre as participações de todos os parceiros, por ano e grupo."""
    saida = []
    for grupo in ("TOTAL", "SEMICOND"):
        for ano in range(1995, 2025):
            mundo = d.get(("842", "M", grupo, ano, 0))
            if not mundo:
                continue
            shares = [v / mundo for (rep, fl, g, a, p), v in d.items()
                      if rep == "842" and fl == "M" and g == grupo and a == ano and p != 0 and v > 0]
            hhi = 10000 * sum(s * s for s in shares)
            top1 = max(shares) * 100 if shares else None
            saida.append({"grupo": grupo, "ano": ano, "HHI": round(hhi, 0), "maior_origem_%": round(top1, 1), "n_origens": len(shares)})
    with open(os.path.join(TRAT, "T4_eua_hhi_origens.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["grupo", "ano", "HHI", "maior_origem_%", "n_origens"]); w.writeheader(); w.writerows(saida)
    return saida


def t3_tiva():
    arq = os.path.join(TRAT, "tiva_consolidado.csv")
    if not os.path.exists(arq):
        return []
    saida = []
    for r in csv.DictReader(open(arq, encoding="utf-8")):
        if r["ACTIVITY"] == "C26" and r["REF_AREA"] in ("CHN", "KOR", "TWN", "USA", "VNM", "MEX") \
           and r["COUNTERPART_AREA"] == "W" and r["TIME_PERIOD"] >= "2005" \
           and r["MEASURE"] in ("EXGR", "EXGR_DVA", "EXGR_FVA", "EXGR_INT"):
            saida.append({"economia": r["REF_AREA"], "ano": r["TIME_PERIOD"], "medida": r["MEASURE"],
                          "tipo": "share_%" if r["arquivo"].startswith("shares") else "nivel_usd_mi",
                          "valor": r["OBS_VALUE"]})
    saida.sort(key=lambda x: (x["economia"], x["medida"], x["tipo"], x["ano"]))
    with open(os.path.join(TRAT, "T3_tiva_C26.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["economia", "ano", "medida", "tipo", "valor"]); w.writeheader(); w.writerows(saida)
    return saida


def resumo(t1, t2, t3, t4):
    L = ["# Leitura rápida das tabelas (gerado por tabelas.py)\n"]
    for grupo in ("TOTAL", "SEMICOND"):
        L.append(f"\n## T1. Destinos das exportações da China, {grupo}: top 12 no pós-2018 (média 2019-24) e variação de posição\n")
        L.append("| rank pós | rank pré | destino | share pré % | share pós % |\n|---|---|---|---|---|")
        for l in [x for x in t1 if x["grupo"] == grupo][:12]:
            L.append(f"| {l['rank_pos']} | {l['rank_pre']} | {l['destino']} | {l['share_pre_%']:.1f} | {l['share_pos_%']:.1f} |" if l['share_pre_%'] and l['share_pos_%'] else f"| {l['rank_pos']} | {l['rank_pre']} | {l['destino']} | | |")
    for grupo in ("TOTAL", "SEMICOND"):
        L.append(f"\n## T2. Importações dos EUA, {grupo}: participação por origem (%)\n")
        cols = [k for k in t2[0].keys() if k.endswith("_%")] if t2 else []
        L.append("| ano | " + " | ".join(c[:-2] for c in cols) + " |\n|" + "---|" * (len(cols) + 1))
        for l in [x for x in t2 if x["grupo"] == grupo and x["ano"] >= 2013]:
            L.append(f"| {l['ano']} | " + " | ".join("" if l[c] is None else f"{l[c]:.1f}" for c in cols) + " |")
    if t4:
        L.append("\n## T4. HHI das origens das importações dos EUA (0 a 10.000) e maior origem (%)\n")
        L.append("| ano | HHI total | maior origem total % | HHI semicond. | maior origem semicond. % |\n|---|---|---|---|---|")
        tot = {x["ano"]: x for x in t4 if x["grupo"] == "TOTAL"}; sem = {x["ano"]: x for x in t4 if x["grupo"] == "SEMICOND"}
        for a in sorted(tot):
            s = sem.get(a, {})
            L.append(f"| {a} | {tot[a]['HHI']:.0f} | {tot[a]['maior_origem_%']} | {s.get('HHI', ''):.0f} | {s.get('maior_origem_%', '')} |" if s else f"| {a} | {tot[a]['HHI']:.0f} | {tot[a]['maior_origem_%']} | | |")
    if t3:
        L.append("\n## T3. TiVA C26: participação do VA doméstico nas exportações brutas (%)\n")
        anos = ["2010", "2015", "2018", "2020", "2022"]
        L.append("| economia | " + " | ".join(anos) + " |\n|" + "---|" * (len(anos) + 1))
        for e in ("CHN", "KOR", "TWN", "USA", "VNM", "MEX"):
            v = {x["ano"]: x["valor"] for x in t3 if x["economia"] == e and x["medida"] == "EXGR_DVA" and x["tipo"] == "share_%"}
            L.append(f"| {e} | " + " | ".join(v.get(a, "") for a in anos) + " |")
    open(os.path.join(TRAT, "resumo_tabelas.md"), "w", encoding="utf-8").write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    d, nomes = carregar_comtrade()
    resumo(t1_china_destinos(d, nomes), t2_eua_origens(d, nomes), t3_tiva(), t4_hhi(d))
