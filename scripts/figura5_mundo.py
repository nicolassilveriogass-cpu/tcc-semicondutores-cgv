# -*- coding: utf-8 -*-
"""
Figura 5 da monografia: participação dos principais exportadores nas exportações
mundiais de semicondutores, ano a ano (2013-2023), e HHI da oferta mundial.
Série anual por trás da Tabela 1. 2024 fica fora porque vários declarantes ainda
não haviam reportado o ano no momento da coleta (mesmo critério da Tabela 1).

Lê tratados/T5_mundo_exportadores_share.csv (gerado por tabela_mundial.py).
Grava figuras/Figura_5_mundo.png (300 dpi, preto e branco). Uso: python figura5_mundo.py
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figuras import ESTILOS, TRAT, FIG   # mesmo padrão visual das Figuras 3 e 4

ANO_FIM = 2023


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(TRAT, "T5_mundo_exportadores_share.csv"), encoding="utf-8"), delimiter=";")
            if int(r["ano"]) <= ANO_FIM]
    f = lambda v: float(v.replace(",", "."))
    anos = [int(r["ano"]) for r in rows]
    series = ["Taiwan", "Hong Kong", "China", "Cingapura", "Coreia do Sul", "Malásia", "Estados Unidos", "Japão", "Vietnã"]
    estilos = ESTILOS + [dict(color="gray", ls="--", marker="P", ms=3), dict(color="black", ls="-.", marker="*", ms=4), dict(color="dimgray", ls=":", marker="+", ms=5)]

    fig = plt.figure(figsize=(6.3, 7.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[2.6, 1.3])
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1])
    for nome, st in zip(series, estilos):
        a.plot(anos, [f(r[nome]) for r in rows], label=nome, lw=1.3, **st)
    a.axvspan(2018, ANO_FIM + 0.3, color="lightgray", alpha=0.35, lw=0)
    a.text(2018.15, 29, "pós-2018", fontsize=8, color="dimgray", va="top")
    a.set_xlim(2013, ANO_FIM + 0.3); a.set_ylim(0, 30)
    a.set_ylabel("Participação nas exportações mundiais (%)"); a.set_xlabel("Ano")
    a.set_title("(a) Participação dos principais exportadores", loc="left", fontsize=9)
    a.legend(ncol=3, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.02), handlelength=2.6, columnspacing=1.0)

    b.plot(anos, [f(r["HHI"]) for r in rows], color="black", lw=1.3, marker="o", ms=3)
    b.axvspan(2018, ANO_FIM + 0.3, color="lightgray", alpha=0.35, lw=0)
    b.set_xlim(2013, ANO_FIM + 0.3); b.set_ylim(1000, 1600)
    b.set_ylabel("HHI (0 a 10.000)"); b.set_xlabel("Ano")
    b.set_title("(b) Concentração da oferta mundial (índice de Herfindahl-Hirschman)", loc="left", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "Figura_5_mundo.png"), dpi=300)
    plt.close(fig)
    print("Figura_5_mundo.png gerada;", [(a_, f(r["HHI"])) for a_, r in zip(anos, rows)])


if __name__ == "__main__":
    main()
