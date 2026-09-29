# -*- coding: utf-8 -*-
"""
Tabela 2 do capítulo 3: os doze maiores destinos das exportações chinesas de
semicondutores no pós-2018 (média 2019-2024), com posição e participação nos
dois períodos, variação em pontos percentuais e, como contraste, a posição do
mesmo destino nas exportações totais da China no pós-2018.
Lê ../tratados/T1_china_destinos_ranking.csv (gerado por tabelas.py) e grava
../tratados/Tabela2_cap3.csv.

Convenção (herdada de T1): participação = média dos valores exportados ao
destino no período dividida pela média do total exportado (parceiro Mundo).
2018 fica fora. Nomes dos destinos traduzidos; Taiwan aparece na base como
"Other Asia, nes".

Uso: python tabela2_cap3.py
"""
import csv, os

AQUI = os.path.dirname(os.path.abspath(__file__))
TRAT = os.path.join(AQUI, "..", "tratados")
NOMES = {"China, Hong Kong SAR": "Hong Kong", "Rep. of Korea": "Coreia do Sul",
         "Taiwan (Other Asia, nes)": "Taiwan", "Viet Nam": "Vietnã", "Malaysia": "Malásia",
         "Singapore": "Cingapura", "India": "Índia", "Japan": "Japão", "USA": "Estados Unidos",
         "Germany": "Alemanha", "Philippines": "Filipinas", "Thailand": "Tailândia",
         "Brazil": "Brasil", "Netherlands": "Países Baixos", "Mexico": "México"}
TOP = 12


def main():
    t1 = list(csv.DictReader(open(os.path.join(TRAT, "T1_china_destinos_ranking.csv"), encoding="utf-8")))
    total_pos = {r["partnerCode"]: int(r["rank_pos"]) for r in t1 if r["grupo"] == "TOTAL"}
    semi = sorted([r for r in t1 if r["grupo"] == "SEMICOND"], key=lambda r: int(r["rank_pos"]))[:TOP]
    saida = []
    for r in semi:
        pre, pos = round(float(r["share_pre_%"]), 1), round(float(r["share_pos_%"]), 1)
        saida.append({"destino": NOMES.get(r["destino"], r["destino"]),
                      "pos_pre": int(r["rank_pre"]), "pos_pos": int(r["rank_pos"]),
                      "share_pre": pre, "share_pos": pos, "var_pp": round(pos - pre, 1),
                      "pos_total_pos": total_pos.get(r["partnerCode"], "")})
    campos = ["destino", "pos_pre", "pos_pos", "share_pre", "share_pos", "var_pp", "pos_total_pos"]
    with open(os.path.join(TRAT, "Tabela2_cap3.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(saida)
    for l in saida:
        print(" | ".join(str(l[c]) for c in campos))


if __name__ == "__main__":
    main()
