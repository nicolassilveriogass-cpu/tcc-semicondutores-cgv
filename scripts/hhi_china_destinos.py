# -*- coding: utf-8 -*-
"""
HHI dos destinos das exportações chinesas (0 a 10.000), por ano, para TOTAL e
SEMICOND (8541 + 8542 menos o grupo 8541.4), e médias pré (2013-2017) e pós
(2019-2024). Fecha o teste da seletividade setorial no ângulo chinês, prometido
no capítulo 2: se a pauta de destinos dos chips se concentra mais do que a do
comércio total, a reorganização é específica do setor.

Lê tratados/comtrade_consolidado.csv (mesma base das Tabelas 2 e 3) via
tabelas.carregar_comtrade(). Grava:
  tratados/T6_china_hhi_destinos.csv        (ano a ano)
  tratados/Tabela2_cap3.csv                 (acrescenta as linhas HHI à Tabela 3 da monografia)

Uso: python hhi_china_destinos.py
"""
import csv, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from tabelas import carregar_comtrade, TRAT, PRE, POS


def hhi_por_ano(d, rep="156", flow="X"):
    saida = []
    for grupo in ("TOTAL", "SEMICOND"):
        for ano in range(1995, 2025):
            mundo = d.get((rep, flow, grupo, ano, 0))
            if not mundo:
                continue
            shares = [v / mundo for (r, f, g, a, p), v in d.items()
                      if r == rep and f == flow and g == grupo and a == ano and p != 0 and v > 0]
            saida.append({"grupo": grupo, "ano": ano, "HHI": round(10000 * sum(s * s for s in shares)),
                          "maior_destino_%": round(100 * max(shares), 1), "n_destinos": len(shares)})
    return saida


def media(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def main():
    d, _ = carregar_comtrade()
    t6 = hhi_por_ano(d)
    with open(os.path.join(TRAT, "T6_china_hhi_destinos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["grupo", "ano", "HHI", "maior_destino_%", "n_destinos"]); w.writeheader(); w.writerows(t6)

    # linhas HHI para a Tabela 3 da monografia (arquivo Tabela2_cap3.csv, nome histórico)
    arq = os.path.join(TRAT, "Tabela2_cap3.csv")
    linhas = [r for r in csv.DictReader(open(arq, encoding="utf-8")) if not r["destino"].startswith("HHI")]
    campos = list(linhas[0].keys())
    for grupo, rot in (("SEMICOND", "HHI semicondutores"), ("TOTAL", "HHI comércio total")):
        pre = media([x["HHI"] for x in t6 if x["grupo"] == grupo and x["ano"] in PRE])
        pos = media([x["HHI"] for x in t6 if x["grupo"] == grupo and x["ano"] in POS])
        linhas.append({"destino": rot, "pos_pre": "", "pos_pos": "", "share_pre": round(pre), "share_pos": round(pos),
                       "var_pp": round(pos - pre), "pos_total_pos": ""})
    with open(arq, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(linhas)
    for l in linhas[-2:]:
        print(l)
    print("ano a ano (SEMICOND):", [(x["ano"], x["HHI"]) for x in t6 if x["grupo"] == "SEMICOND" and x["ano"] >= 2013])
    print("ano a ano (TOTAL):   ", [(x["ano"], x["HHI"]) for x in t6 if x["grupo"] == "TOTAL" and x["ano"] >= 2013])


if __name__ == "__main__":
    main()
