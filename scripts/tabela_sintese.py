# -*- coding: utf-8 -*-
"""
Tabela-síntese da hipótese: variação, em pontos percentuais, da participação de
cada economia nos três ângulos da monografia, entre as médias de 2013-2017 e
2019-2024 (2019-2023 no ângulo mundial):
  (1) exportações mundiais de semicondutores      -> tratados/Tabela1_cap3_mundial.csv
  (2) importações de semicondutores dos EUA        -> tratados/Tabela1_cap3.csv
  (3) destinos das exportações chinesas de chips   -> tratados/Tabela2_cap3.csv
Nenhum dado novo: só reúne as três tabelas já tratadas. Economias fora dos doze
maiores destinos chineses ficam como "n.d." no ângulo (3).

Grava tratados/Tabela6_cap3_sintese.csv.  Uso: python tabela_sintese.py
"""
import csv, os
AQUI = os.path.dirname(os.path.abspath(__file__))
TRAT = os.path.join(AQUI, "..", "tratados")

ECONOMIAS = ["China", "Taiwan", "Coreia do Sul", "Malásia", "Vietnã", "Índia", "México", "Japão", "Estados Unidos"]
# nomes como aparecem em cada arquivo
NOME_MUNDO = {"Coreia do Sul": "Coreia do Sul", "Estados Unidos": "Estados Unidos"}
NOME_EUA = {}
NOME_CHN = {}


def f(v):
    return float(str(v).replace(",", ".")) if v not in ("", None) else None


def main():
    mundo = {r[4]: f(r[3]) for r in csv.reader(open(os.path.join(TRAT, "Tabela1_cap3_mundial.csv"), encoding="utf-8"), delimiter=";") if len(r) == 5 and r[0] != "pais"}
    eua = {r["linha"]: f(r["semicond_var_pp"]) for r in csv.DictReader(open(os.path.join(TRAT, "Tabela1_cap3.csv"), encoding="utf-8"))}
    chn = {r["destino"]: f(r["var_pp"]) for r in csv.DictReader(open(os.path.join(TRAT, "Tabela2_cap3.csv"), encoding="utf-8")) if not r["destino"].startswith("HHI")}
    linhas = []
    for e in ECONOMIAS:
        linhas.append({"economia": e,
                       "mundo_var_pp": mundo.get(NOME_MUNDO.get(e, e)),
                       "eua_var_pp": eua.get(NOME_EUA.get(e, e)),
                       "china_var_pp": chn.get(NOME_CHN.get(e, e))})
    with open(os.path.join(TRAT, "Tabela6_cap3_sintese.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["economia", "mundo_var_pp", "eua_var_pp", "china_var_pp"]); w.writeheader(); w.writerows(linhas)
    for l in linhas:
        print(l)


if __name__ == "__main__":
    main()
