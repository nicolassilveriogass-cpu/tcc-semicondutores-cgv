# -*- coding: utf-8 -*-
"""
Tabela 1 do capítulo 3: participação de origens selecionadas nas importações
dos Estados Unidos, semicondutores e total, médias dos períodos pré (2013-2017)
e pós (2019-2024), com a variação em pontos percentuais e o HHI médio de cada
período. Lê ../tratados/T2_eua_origens_share.csv e T4_eua_hhi_origens.csv
(gerados por tabelas.py) e grava ../tratados/Tabela1_cap3.csv.

Convenção: média simples das participações anuais de cada período (não a razão
entre médias de valores). 2018 fica fora por ser o ano de transição.

Uso: python tabela1_cap3.py
"""
import csv, os

AQUI = os.path.dirname(os.path.abspath(__file__))
TRAT = os.path.join(AQUI, "..", "tratados")
PRE, POS = range(2013, 2018), range(2019, 2025)
ORIGENS = ["China", "Taiwan", "Coreia do Sul", "Malásia", "Vietnã", "Japão", "México"]


def media(vals):
    vals = [v for v in vals if v not in (None, "")]
    return sum(float(v) for v in vals) / len(vals) if vals else None


def main():
    t2 = list(csv.DictReader(open(os.path.join(TRAT, "T2_eua_origens_share.csv"), encoding="utf-8")))
    t4 = list(csv.DictReader(open(os.path.join(TRAT, "T4_eua_hhi_origens.csv"), encoding="utf-8")))
    linhas = []
    for origem in ORIGENS:
        linha = {"linha": origem}
        for grupo, rot in (("SEMICOND", "semicond"), ("TOTAL", "total")):
            pre = media([r[f"{origem}_%"] for r in t2 if r["grupo"] == grupo and int(r["ano"]) in PRE])
            pos = media([r[f"{origem}_%"] for r in t2 if r["grupo"] == grupo and int(r["ano"]) in POS])
            # variação calculada sobre os valores arredondados, para bater com as colunas impressas
            linha[f"{rot}_pre"] = round(pre, 1); linha[f"{rot}_pos"] = round(pos, 1)
            linha[f"{rot}_var_pp"] = round(linha[f"{rot}_pos"] - linha[f"{rot}_pre"], 1)
        linhas.append(linha)
    linha = {"linha": "HHI (0 a 10.000)"}
    for grupo, rot in (("SEMICOND", "semicond"), ("TOTAL", "total")):
        pre = media([r["HHI"] for r in t4 if r["grupo"] == grupo and int(r["ano"]) in PRE])
        pos = media([r["HHI"] for r in t4 if r["grupo"] == grupo and int(r["ano"]) in POS])
        linha[f"{rot}_pre"] = round(pre); linha[f"{rot}_pos"] = round(pos); linha[f"{rot}_var_pp"] = round(pos - pre)
    linhas.append(linha)
    campos = ["linha", "semicond_pre", "semicond_pos", "semicond_var_pp", "total_pre", "total_pos", "total_var_pp"]
    with open(os.path.join(TRAT, "Tabela1_cap3.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(linhas)
    for l in linhas:
        print(" | ".join(str(l[c]) for c in campos))


if __name__ == "__main__":
    main()
