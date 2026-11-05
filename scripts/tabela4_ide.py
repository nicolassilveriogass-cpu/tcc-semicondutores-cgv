# -*- coding: utf-8 -*-
"""
Tabela 4 (cap. 3, seção 3.3.2): investimento direto greenfield anunciado em setores estratégicos,
2020-2025, a partir da transcrição conferida do UNCTAD Trade and Development Report 2026
(figuras III.6 e III.7.B e totais de texto, p. 107-108). Lê ../brutos/unctad/unctad_tdr2026_greenfield_estrategico.csv
e grava ../tratados/Tabela4_cap3_ide.csv em duas partes: (A) participação de economias desenvolvidas e em
desenvolvimento por setor; (B) participação das dez economias asiáticas em desenvolvimento no total mundial.

Decisão: versão simples (sem coleta própria de IDE bilateral), como combinado com o orientador em 13/10/2026.
Uso: python tabela4_ide.py
"""
import csv, os

AQUI = os.path.dirname(os.path.abspath(__file__))
BRUTO = os.path.join(AQUI, "..", "brutos", "unctad", "unctad_tdr2026_greenfield_estrategico.csv")
SAIDA = os.path.join(AQUI, "..", "tratados", "Tabela4_cap3_ide.csv")


def main():
    rows = list(csv.DictReader(open(BRUTO, encoding="utf-8")))
    saida = []
    # Parte A: uma linha por setor, duas colunas
    setores = {}
    for r in rows:
        if r["bloco"] != "A_participacao_por_setor":
            continue
        setor, grupo = r["item"].rsplit(":", 1)
        setores.setdefault(setor.strip(), {})[grupo.strip()] = float(r["valor"])
    for setor, v in setores.items():
        saida.append({"parte": "A", "linha": setor, "desenvolvidas_%": v.get("economias desenvolvidas", v.get("desenvolvidas")),
                      "em_desenvolvimento_%": v.get("economias em desenvolvimento", v.get("em desenvolvimento")), "fonte": "UNCTAD (2026), fig. III.6, p. 107"})
    # Parte B: economias asiáticas
    for r in rows:
        if r["bloco"] == "B_asia_em_desenvolvimento":
            saida.append({"parte": "B", "linha": r["item"], "desenvolvidas_%": "", "em_desenvolvimento_%": float(r["valor"]),
                          "fonte": "UNCTAD (2026), fig. III.7.B, p. 108 (participação no valor mundial dos projetos em setores estratégicos)"})
    campos = ["parte", "linha", "desenvolvidas_%", "em_desenvolvimento_%", "fonte"]
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(saida)
    for l in saida:
        print(" | ".join(str(l[c]) for c in campos[:4]))


if __name__ == "__main__":
    main()
