"""
Tabela 3 (participacao mundial): exportacoes de semicondutores (HS 8541 + 8542 - 8541.4)
por pais exportador, 2013-2024, a partir do UN Comtrade (API publica "preview").

Metodo:
  - Exportacoes declaradas (flowCode=X, partnerCode=0 "World") de TODOS os declarantes,
    um arquivo por (ano, codigo HS). Sem reporterCode a API devolve todos os declarantes.
  - Taiwan (codigo 490, "Other Asia, nes") NAO declara ao Comtrade. Para Taiwan usa-se o
    dado-espelho: soma das importacoes que todos os declarantes informam ter origem em 490.
    Limite conhecido: espelho e CIF e pode contar duas vezes reexportacoes via Hong Kong.
  - Denominador "mundo" = soma das exportacoes declaradas + espelho de Taiwan.
  - HHI calculado sobre a distribuicao completa de exportadores (shares em %, somados ao quadrado).
  - Medias: pre = 2013-2017; pos = 2019-2024; 2018 fica de fora (ano de transicao).

  - Pos desta tabela = 2019-2023 (e nao 2019-2024, como nas tabelas dos EUA e da China), porque
    em nov/2026 varios declarantes (Vietna, Paises Baixos, entre outros) ainda nao haviam
    informado 2024 ao Comtrade; a serie anual completa (ate 2024) fica gravada para conferencia.

Saidas (pasta 10. Dados):
  brutos/comtrade_mundo/       um JSON por consulta, com data e hora de acesso no nome;
                               se o JSON da consulta ja existe, e reaproveitado (nao baixa de novo)
  tratados/T5_mundo_exportadores_share.csv   participacao (%) por exportador e ano, HHI e total mundial
  tratados/Tabela1_cap3_mundial.csv          medias pre (2013-17) e pos (2019-23), variacao em p.p., HHI
  brutos/comtrade_mundo/log_tabela_mundial.txt   registro das consultas

Uso: python scripts/tabela_mundial.py   (a partir da pasta 10. Dados ou do clone do GitHub)
"""
import os, sys, json, time, datetime as dt
import requests
import pandas as pd

URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
ANOS = list(range(2013, 2025))
CMDS = ["8541", "8542", "854140"]
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pasta 10. Dados
BRUTOS = os.path.join(RAIZ, "brutos", "comtrade_mundo")
TRATADOS = os.path.join(RAIZ, "tratados")
os.makedirs(BRUTOS, exist_ok=True); os.makedirs(TRATADOS, exist_ok=True)
LOG = open(os.path.join(BRUTOS, "log_tabela_mundial.txt"), "a", encoding="utf-8")
PRE, POS = (2013, 2017), (2019, 2023)

NOMES = {156: "China", 344: "Hong Kong", 410: "Coreia do Sul", 490: "Taiwan", 458: "Malásia",
         704: "Vietnã", 702: "Singapura", 392: "Japão", 842: "Estados Unidos", 608: "Filipinas",
         276: "Alemanha", 764: "Tailândia", 699: "Índia", 484: "México", 528: "Países Baixos",
         372: "Irlanda", 36: "Austrália", 76: "Brasil", 757: "Suíça", 376: "Israel", 251: "França"}

def consulta(params, nome):
    """Baixa uma consulta, grava o JSON bruto com carimbo de tempo e devolve a lista de registros.
    Se ja existe um bruto desta consulta, reaproveita (reprodutibilidade sem depender da API)."""
    import glob
    ja = sorted(glob.glob(os.path.join(BRUTOS, f"{nome}_*.json")))
    if ja:
        with open(ja[-1], encoding="utf-8") as f:
            return json.load(f).get("data", [])
    for tent in range(4):
        try:
            r = requests.get(URL, params=params, timeout=120)
            if r.status_code == 200:
                j = r.json()
                carimbo = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                with open(os.path.join(BRUTOS, f"{nome}_{carimbo}.json"), "w", encoding="utf-8") as f:
                    json.dump(j, f)
                LOG.write(f"{carimbo}\t{nome}\tcount={j.get('count')}\t{r.url}\n"); LOG.flush()
                if j.get("count", 0) >= 500:
                    print("AVISO: 500 registros, pode haver truncamento:", nome)
                return j.get("data", [])
            print("HTTP", r.status_code, nome, r.text[:120]); time.sleep(5 + 5 * tent)
        except Exception as e:
            print("erro", nome, e); time.sleep(5 + 5 * tent)
    sys.exit(f"falha definitiva em {nome}")

base = dict(motCode=0, partner2Code=0, customsCode="C00")
reg = []  # (ano, reporter, cmd, valor)
for ano in ANOS:
    for cmd in CMDS:
        # exportacoes declaradas, todos os declarantes, parceiro Mundo
        for d in consulta(dict(base, partnerCode=0, flowCode="X", cmdCode=cmd, period=ano), f"X_all_W_{cmd}_{ano}"):
            if d["reporterCode"] not in (0, 490) and d["partnerCode"] == 0:
                reg.append((ano, d["reporterCode"], cmd, d["primaryValue"]))
        # espelho de Taiwan: importacoes de todos os declarantes com origem 490
        tw = sum(d["primaryValue"] for d in consulta(dict(base, partnerCode=490, flowCode="M", cmdCode=cmd, period=ano), f"M_all_TW_{cmd}_{ano}")
                 if d["reporterCode"] != 0)
        reg.append((ano, 490, cmd, tw))
        time.sleep(0.3)

df = pd.DataFrame(reg, columns=["ano", "pais", "cmd", "valor"])
piv = df.pivot_table(index=["ano", "pais"], columns="cmd", values="valor", aggfunc="sum").fillna(0)
piv["semi"] = piv["8541"] + piv["8542"] - piv["854140"]
semi = piv["semi"].unstack("pais").fillna(0)
mundo = semi.sum(axis=1)
share = semi.div(mundo, axis=0) * 100
hhi = (share ** 2).sum(axis=1)

# tabela anual dos principais
top = share.loc[ANOS].mean().sort_values(ascending=False).head(15).index
anual = share[top].rename(columns=lambda c: NOMES.get(c, str(c))).round(2)
anual["HHI"] = hhi.round(0)
anual["Mundo (US$ bi)"] = (mundo / 1e9).round(1)
anual.to_csv(os.path.join(TRATADOS, "T5_mundo_exportadores_share.csv"), sep=";", decimal=",")

pre = share.loc[PRE[0]:PRE[1]].mean(); pos = share.loc[POS[0]:POS[1]].mean()
tab = pd.DataFrame({"pre_2013_17": pre, "pos_2019_23": pos})
tab["var_pp"] = tab["pos_2019_23"] - tab["pre_2013_17"]
tab["pais"] = [NOMES.get(c, str(c)) for c in tab.index]
tab = tab.sort_values("pos_2019_23", ascending=False).round(2)
tab.loc["HHI"] = [hhi.loc[PRE[0]:PRE[1]].mean().round(0), hhi.loc[POS[0]:POS[1]].mean().round(0),
                  (hhi.loc[POS[0]:POS[1]].mean() - hhi.loc[PRE[0]:PRE[1]].mean()).round(0), "HHI (todos os exportadores)"]
tab.loc["Mundo_USD_bi"] = [(mundo.loc[PRE[0]:PRE[1]].mean() / 1e9).round(1), (mundo.loc[POS[0]:POS[1]].mean() / 1e9).round(1), float("nan"), "exportações mundiais, US$ bi/ano"]
tab.to_csv(os.path.join(TRATADOS, "Tabela1_cap3_mundial.csv"), sep=";", decimal=",")
print(tab.head(16).to_string())
print("HHI anual:\n", hhi.round(0).to_string())
