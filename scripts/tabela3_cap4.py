# -*- coding: utf-8 -*-
"""
Tabela 3 (adendo 4.3): produção e reservas de terras raras por país, a partir da
transcrição conferida do USGS Mineral Commodity Summaries 2026 (Johnston, 2026),
em toneladas de óxidos de terras raras (REO). Lê ../brutos/usgs/usgs_mcs2026_terras_raras.csv
e grava ../tratados/Tabela3_cap4.csv.

Regras: países ordenados pelas reservas (decrescente); os que não têm reserva
reportada (NA) vêm depois, ordenados pela produção de 2025; participações
calculadas sobre o total mundial da própria fonte (produção 390.000 t em 2025;
reservas "mais de 85 milhões" de t, usadas como 85.000.000, o que faz as
participações nas reservas serem um teto).

Uso: python tabela3_cap4.py
"""
import csv, os

AQUI = os.path.dirname(os.path.abspath(__file__))
BRUTO = os.path.join(AQUI, "..", "brutos", "usgs", "usgs_mcs2026_terras_raras.csv")
SAIDA = os.path.join(AQUI, "..", "tratados", "Tabela3_cap4.csv")
NOMES = {"Australia": "Austrália", "Canada": "Canadá", "Groenlandia": "Groenlândia", "India": "Índia",
         "Malasia": "Malásia", "Nigeria": "Nigéria", "Russia": "Rússia", "Africa do Sul": "África do Sul",
         "Tanzania": "Tanzânia", "Tailandia": "Tailândia", "Vietna": "Vietnã"}


def num(x):
    x = (x or "").strip().replace(">", "")
    return float(x) if x and x != "NA" else None


def main():
    rows = list(csv.DictReader(open(BRUTO, encoding="utf-8")))
    total = [r for r in rows if r["pais"] == "Total mundial"][0]
    tot_p25, tot_res = num(total["producao_2025e_t_REO"]), num(total["reservas_t_REO"])
    paises = [r for r in rows if r["pais"] != "Total mundial"]
    com = sorted([r for r in paises if num(r["reservas_t_REO"]) is not None], key=lambda r: -num(r["reservas_t_REO"]))
    sem = sorted([r for r in paises if num(r["reservas_t_REO"]) is None], key=lambda r: -(num(r["producao_2025e_t_REO"]) or 0))
    saida = []
    for r in com + sem + [total]:
        p24, p25, res = num(r["producao_2024_t_REO"]), num(r["producao_2025e_t_REO"]), num(r["reservas_t_REO"])
        saida.append({"pais": NOMES.get(r["pais"], r["pais"]),
                      "producao_2024_t": p24, "producao_2025_t": p25,
                      "share_producao_2025_%": round(100 * p25 / tot_p25, 1) if p25 else None,
                      "reservas_t": res,
                      "share_reservas_%": round(100 * res / tot_res, 1) if res else None,
                      "reservas_nd": "n.d." if res is None and r["pais"] != "Total mundial" else ""})
    campos = ["pais", "producao_2024_t", "producao_2025_t", "share_producao_2025_%", "reservas_t", "share_reservas_%", "reservas_nd"]
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(saida)
    for l in saida:
        print(" | ".join("" if l[c] is None else str(l[c]) for c in campos))


if __name__ == "__main__":
    main()
