# -*- coding: utf-8 -*-
"""
Coleta de indicadores de valor adicionado na OCDE TiVA (edição 2025) via SDMX.

Fonte: OECD.STI.PIE, dataflows DSD_TIVA_MAINLV@DF_MAINLV (níveis, US$ milhões)
e DSD_TIVA_MAINSH@DF_MAINSH (participações, %). Endpoint público 'sti-public'
(o endpoint 'public' devolve erro 500 para esses fluxos). Sem chave.

Cobertura: 1995-2022, anual. Atividade C26 (computadores, eletrônicos e
ópticos) é a abertura mais fina disponível; não existe C261 na TiVA.
Taiwan aparece como "Chinese Taipei" (código TWN).

O que baixa (por economia, contraparte Mundo):
  níveis: EXGR, EXGR_INT, EXGR_FNL, EXGR_DVA, EXGR_FVA, VALU
  shares: os mesmos códigos no fluxo MAINSH (em % das exportações brutas)
  parceiros: EXGR_PSH e EXGR_DVA_PSH (participação por destino) em C26,
             para CHN, KOR, TWN e USA com todos os parceiros.

Uso: python tiva_coleta.py
Saída: ../brutos/tiva/*.csv, ../tratados/tiva_consolidado.csv, ../log_acessos.csv
"""
import csv, io, os, sys, time, urllib.request, urllib.error
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
BRUTOS = os.path.join(AQUI, "..", "brutos", "tiva")
TRATADOS = os.path.join(AQUI, "..", "tratados")
os.makedirs(BRUTOS, exist_ok=True); os.makedirs(TRATADOS, exist_ok=True)

BASE = "https://sdmx.oecd.org/sti-public/rest/data/OECD.STI.PIE,{df},1.1/{key}?format=csvfilewithlabels"
DF_LV = "DSD_TIVA_MAINLV@DF_MAINLV"
DF_SH = "DSD_TIVA_MAINSH@DF_MAINSH"

AREAS = ["CHN", "KOR", "TWN", "USA", "JPN", "VNM", "MEX", "BRA", "W"]
ATIVIDADES = "_T+C+C26"
MEDIDAS = "EXGR+EXGR_INT+EXGR_FNL+EXGR_DVA+EXGR_FVA+VALU"
MEDIDAS_PSH = "EXGR_PSH+EXGR_DVA_PSH"
PAUSA = 2.0


def registrar_acesso(base, url, obs=""):
    arq = os.path.join(AQUI, "..", "log_acessos.csv")
    novo = not os.path.exists(arq)
    with open(arq, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["base", "url", "data_hora_acesso", "observacao"])
        w.writerow([base, url, datetime.now().strftime("%Y-%m-%d %H:%M"), obs])


def baixar(df, key):
    """Uma consulta SDMX; devolve lista de dicts. Levanta exceção em erro."""
    url = BASE.format(df=df, key=key)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    espera = 5
    for t in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                txt = r.read().decode("utf-8")
            return list(csv.DictReader(io.StringIO(txt)))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return []          # combinação sem dados
            if t < 3:
                time.sleep(espera); espera *= 2; continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if t < 3:
                time.sleep(espera); espera *= 2; continue
            raise


CAMPOS = ["MEASURE", "Measure", "REF_AREA", "Reference area", "ACTIVITY",
          "Economic activity", "COUNTERPART_AREA", "Counterpart area",
          "UNIT_MEASURE", "TIME_PERIOD", "OBS_VALUE", "UNIT_MULT"]


def salvar(nome, linhas):
    arq = os.path.join(BRUTOS, nome)
    with open(arq, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, extrasaction="ignore")
        w.writeheader(); w.writerows(linhas)
    print(f"ok {nome}: {len(linhas)} obs")


def main():
    registrar_acesso("OECD TiVA 2025 edition (SDMX, sti-public)",
                     "https://sdmx.oecd.org/sti-public/rest/data/OECD.STI.PIE",
                     f"fluxos {DF_LV} e {DF_SH}; áreas {AREAS}; atividades {ATIVIDADES}")
    tarefas = []
    for a in AREAS:
        tarefas.append((f"niveis_{a}.csv", DF_LV, f"{MEDIDAS}.{a}.{ATIVIDADES}.W..A"))
        tarefas.append((f"shares_{a}.csv", DF_SH, f"{MEDIDAS}.{a}.{ATIVIDADES}.W..A"))
    for a in ["CHN", "KOR", "TWN", "USA"]:
        tarefas.append((f"parceiros_C26_{a}.csv", DF_SH, f"{MEDIDAS_PSH}.{a}.C26...A"))

    falhas = []
    for nome, df, key in tarefas:
        arq = os.path.join(BRUTOS, nome)
        if os.path.exists(arq) and os.path.getsize(arq) > 200:
            continue
        try:
            salvar(nome, baixar(df, key))
        except Exception as e:
            print(f"FALHA {nome}: {e}", file=sys.stderr); falhas.append(nome)
        time.sleep(PAUSA)

    cons = os.path.join(TRATADOS, "tiva_consolidado.csv")
    with open(cons, "w", newline="", encoding="utf-8") as out:
        w = csv.DictWriter(out, fieldnames=["arquivo"] + CAMPOS); w.writeheader()
        for a in sorted(os.listdir(BRUTOS)):
            if a.endswith(".csv"):
                for r in csv.DictReader(open(os.path.join(BRUTOS, a), encoding="utf-8")):
                    r["arquivo"] = a; w.writerow(r)
    print(f"\nConsolidado: {cons}. Falhas: {falhas}")


if __name__ == "__main__":
    main()
