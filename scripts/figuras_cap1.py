"""
figuras_cap1.py: gera as duas figuras conceituais do capítulo 1 da monografia,
redesenhadas a partir de Hermida (2016, p. 48 e 52) e Baldwin (2016).

Saída (300 dpi, preto e branco, Times):
  figuras/Figura_1_cap1_fragmentacao.png   matriz localização x relação entre firmas
  figuras/Figura_2_cap1_linha_tempo.png    linha do tempo dos dois desmembramentos

Uso: python figuras_cap1.py   (executar a partir de 10. Dados\scripts)
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Liberation Serif"],
    "font.size": 10,
})

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figuras")
os.makedirs(OUT, exist_ok=True)


def figura_1():
    """Matriz 2x2: linhas = relação entre firmas; colunas = localização."""
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    ax.text(7.05, 5.85, "Localização", ha="center", va="center", fontsize=9.5, fontweight="bold")
    ax.text(5.2, 5.25, "Nacional", ha="center", va="center", fontsize=9)
    ax.text(8.9, 5.25, "Internacional", ha="center", va="center", fontsize=9)
    ax.text(0.6, 2.65, "Relação\nentre\nfirmas", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(2.2, 3.8, "Entre firmas\n(terceirização)", ha="center", va="center", fontsize=8)
    ax.text(2.2, 1.5, "Uma única\nfirma", ha="center", va="center", fontsize=8)

    w, h = 3.5, 2.1
    celulas = [
        (3.45, 2.75, "Outsourcing doméstico\n(compra de firmas\nterceiras no país)", "white"),
        (7.15, 2.75, "Outsourcing internacional\n(compra de firmas\nestrangeiras)", "#d9d9d9"),
        (3.45, 0.45, "Fornecimento doméstico\n(empresa verticalizada\nem um único país)", "white"),
        (7.15, 0.45, "Insourcing internacional\n(produção em filiais\nno exterior, via IDE)", "#d9d9d9"),
    ]
    for x, y, txt, cor in celulas:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=cor, edgecolor="black", linewidth=0.8))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=8)

    xb = 10.9
    ax.plot([xb, xb], [0.6, 4.7], color="black", lw=0.9)
    ax.plot([xb - 0.12, xb], [0.6, 0.6], color="black", lw=0.9)
    ax.plot([xb - 0.12, xb], [4.7, 4.7], color="black", lw=0.9)
    ax.plot([xb, xb + 0.25], [2.65, 2.65], color="black", lw=0.9)
    ax.text(xb + 0.35, 2.65, "Offshoring\n(fragmentação\ninternacional)", ha="left", va="center", fontsize=8.5, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "Figura_1_cap1_fragmentacao.png"), dpi=300, facecolor="white")
    plt.close(fig)


def figura_2():
    """Linha do tempo (eixo categórico) com os dois desmembramentos e os fatos estilizados."""
    fig, ax = plt.subplots(figsize=(6.5, 4.6))
    ax.set_xlim(-0.6, 6.9)
    ax.set_ylim(-3.6, 3.2)
    ax.axis("off")

    rotulos = ["1770-80", "1830", "1870", "1940", "1980", "1990", "2000..."]
    xs = list(range(7))
    ax.annotate("", xy=(6.75, 0), xytext=(-0.5, 0), arrowprops=dict(arrowstyle="-|>", lw=1.2, color="black"))
    for x, r in zip(xs, rotulos):
        if r != "2000...":
            ax.plot(x, 0, "o", color="black", ms=5)
        ax.text(x, -0.3, r, ha="center", va="top", fontsize=8)

    cima = [
        (0, 1.2, "Primeiras tecnologias\nmecanizadas"),
        (1.5, 2.4, "1ª e 2ª Revolução Industrial\n(vapor, ferrovias, navios)"),
        (3, 1.2, "Máquinas elétricas e\nengenharia pesada"),
        (4.5, 2.4, "3ª Revolução Industrial\n(novas tecnologias\nde informação e comunicação)"),
    ]
    for x, y, t in cima:
        ax.text(x, y, t, ha="center", va="center", fontsize=7.5,
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="black", lw=0.7))
        ax.annotate("", xy=(x, 0.12), xytext=(x, y - 0.5), arrowprops=dict(arrowstyle="-|>", lw=0.7, color="black"))

    chaves = [
        (1, 3, "Primeiro desmembramento",
         "industrialização do Norte e\ndesindustrialização do Sul;\n"
         "divergência de rendas Norte-Sul;\naglomeração local da produção\n(clusters e distritos industriais)"),
        (4, 6, "Segundo desmembramento",
         "dispersão global da produção;\nreversão da divergência de rendas;\n"
         "industrialização do Sul e\ndesindustrialização do Norte;\nCGV como nova via de industrialização"),
    ]
    for x0, x1, titulo, fatos in chaves:
        y = -0.95
        ax.plot([x0, x1], [y, y], color="black", lw=0.9)
        ax.plot([x0, x0], [y, y + 0.25], color="black", lw=0.9)
        ax.plot([x1, x1], [y, y + 0.25], color="black", lw=0.9)
        xm = (x0 + x1) / 2
        ax.text(xm, y - 0.2, titulo, ha="center", va="top", fontsize=8, fontweight="bold")
        ax.text(xm, y - 0.75, fatos, ha="center", va="top", fontsize=7,
                bbox=dict(boxstyle="square,pad=0.35", facecolor="#eeeeee", edgecolor="black", lw=0.6))

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "Figura_2_cap1_linha_tempo.png"), dpi=300, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    figura_1()
    figura_2()
    print("Figuras geradas em", os.path.abspath(OUT))
