# -*- coding: utf-8 -*-
"""
Figuras da monografia, padrão ABNT (título acima, fonte abaixo), legíveis em
preto e branco (estilos de linha distintos), 300 dpi, Times New Roman.
Lê ../tratados/T*.csv e grava ../figuras/Figura_N.png.

Uso: python figuras.py
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
TRAT = os.path.join(AQUI, "..", "tratados")
FIG = os.path.join(AQUI, "..", "figuras")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "font.size": 10, "axes.titlesize": 10, "axes.labelsize": 10,
    "legend.fontsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linestyle": ":",
})
# estilos distinguíveis sem cor (cada série = cor + traço + marcador diferentes)
ESTILOS = [
    dict(color="black", ls="-", marker="o", ms=3),
    dict(color="black", ls="--", marker="s", ms=3),
    dict(color="dimgray", ls="-", marker="^", ms=3),
    dict(color="dimgray", ls="-.", marker="D", ms=3),
    dict(color="gray", ls=":", marker="v", ms=3),
    dict(color="black", ls=(0, (1, 1)), marker="x", ms=4),
]


def ler(nome):
    with open(os.path.join(TRAT, nome), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fig1():
    """Figura 1: origens das importações de semicondutores dos EUA (%) e HHI, 1995-2024."""
    t2 = [r for r in ler("T2_eua_origens_share.csv") if r["grupo"] == "SEMICOND"]
    t4 = {(r["grupo"], int(r["ano"])): float(r["HHI"]) for r in ler("T4_eua_hhi_origens.csv")}
    anos = [int(r["ano"]) for r in t2]
    series = [("China", "China_%"), ("Taiwan", "Taiwan_%"), ("Coreia do Sul", "Coreia do Sul_%"),
              ("Malásia", "Malásia_%"), ("Vietnã", "Vietnã_%"), ("Japão", "Japão_%")]

    fig, (a, b) = plt.subplots(2, 1, figsize=(6.3, 7.4), gridspec_kw={"height_ratios": [3, 1.5]})
    for (rotulo, col), st in zip(series, ESTILOS):
        y = [float(r[col]) if r[col] else None for r in t2]
        a.plot(anos, y, label=rotulo, lw=1.3, markevery=3, **st)
    a.axvspan(2018, 2024.4, color="lightgray", alpha=0.35, lw=0)
    a.set_ylabel("Participação (%)")
    a.set_xlim(1995, 2024.4); a.set_ylim(0, 50)
    a.text(2018.3, 48, "pós-2018", fontsize=8, color="dimgray", va="top")
    a.legend(ncol=6, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), handlelength=2.6, columnspacing=1.0)
    a.set_title("(a) Participação por origem nas importações de semicondutores dos EUA", loc="left", fontsize=9, pad=22)

    hs = [t4.get(("SEMICOND", y)) for y in anos]; ht = [t4.get(("TOTAL", y)) for y in anos]
    b.plot(anos, hs, color="black", ls="-", lw=1.3, label="Semicondutores")
    b.plot(anos, ht, color="dimgray", ls="--", lw=1.3, label="Total das importações")
    b.axvspan(2018, 2024.4, color="lightgray", alpha=0.35, lw=0)
    b.set_ylabel("HHI (0 a 10.000)"); b.set_xlabel("Ano"); b.set_xlim(1995, 2024.4); b.set_ylim(bottom=0)
    b.set_ylim(0, 2600)
    b.legend(frameon=False, loc="upper left", ncol=2)
    b.set_title("(b) Concentração da pauta de origem (índice de Herfindahl-Hirschman)", loc="left", fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "Figura_1.png"), dpi=300)
    plt.close(fig)
    print("Figura_1.png gerada")


def fig2():
    """Figura 2: participação do valor adicionado doméstico nas exportações brutas
    da atividade C26 (computadores, eletrônicos e ópticos), TiVA 2025, 2005-2022."""
    t3 = [r for r in ler("T3_tiva_C26.csv") if r["medida"] == "EXGR_DVA" and r["tipo"] == "share_%"]
    series = [("China", "CHN"), ("Taiwan", "TWN"), ("Coreia do Sul", "KOR"),
              ("Vietnã", "VNM"), ("México", "MEX"), ("Estados Unidos", "USA")]
    fig, a = plt.subplots(figsize=(6.3, 4.2))
    for (rotulo, cod), st in zip(series, ESTILOS):
        pts = sorted((int(r["ano"]), float(r["valor"])) for r in t3 if r["economia"] == cod)
        a.plot([x for x, _ in pts], [y for _, y in pts], label=rotulo, lw=1.3, markevery=3, **st)
    a.axvspan(2018, 2022.3, color="lightgray", alpha=0.35, lw=0)
    a.text(2018.2, 98, "pós-2018", fontsize=8, color="dimgray", va="top")
    a.set_xlim(2005, 2022.3); a.set_ylim(30, 100)
    a.set_ylabel("Valor adicionado doméstico (% das exportações brutas)"); a.set_xlabel("Ano")
    a.legend(ncol=3, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), handlelength=2.6, columnspacing=1.2)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "Figura_2.png"), dpi=300)
    plt.close(fig)
    print("Figura_2.png gerada")


if __name__ == "__main__":
    fig1()
    fig2()
