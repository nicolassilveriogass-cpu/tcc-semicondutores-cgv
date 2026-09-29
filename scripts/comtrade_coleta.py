# -*- coding: utf-8 -*-
"""
Coleta de comércio bilateral na UN Comtrade (API pública, modo preview, sem chave).

O que baixa
-----------
1. Exportações da China (reporter 156) por parceiro, anuais, para:
   - TOTAL (todos os produtos)
   - HS 8541 (diodos, transistores, semicondutores fotossensíveis)
   - HS 8542 (circuitos integrados)
   - HS 854140 (dispositivos fotossensíveis, incl. células fotovoltaicas): a subposição
     é coletada para ser SUBTRAÍDA de 8541, porque painéis solares não são
     "semicondutores" no sentido da SIA (que usa 8541 exceto solar + 8542).
2. Importações dos EUA (reporter 842) por parceiro, para os mesmos códigos.

Período: 1995 a 2024 (recorte do projeto aprovado; foco pós-2018).

Limites do modo preview: 500 registros por chamada e limite de chamadas por hora.
Por isso cada chamada cobre um (reporter, ano, código) e o resultado é gravado
em CSV; chamadas já feitas são puladas na execução seguinte (cache).

Atenção metodológica: na Comtrade, Taiwan aparece como "Other Asia, nes"
(código de parceiro 490). Isso é documentado na coluna 'partner_desc'.

Uso: python comtrade_coleta.py
Saída: ../brutos/comtrade/<reporter>_<flow>_<cmd>_<ano>.csv e um consolidado
       ../tratados/comtrade_consolidado.csv
"""
import csv, json, os, sys, time, urllib.request, urllib.error
from datetime import datetime

BASE = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
AQUI = os.path.dirname(os.path.abspath(__file__))
BRUTOS = os.path.join(AQUI, "..", "brutos", "comtrade")
TRATADOS = os.path.join(AQUI, "..", "tratados")
os.makedirs(BRUTOS, exist_ok=True); os.makedirs(TRATADOS, exist_ok=True)

ANOS = list(range(1995, 2025))
CODIGOS = ["TOTAL", "8541", "8542", "854140"]   # 854140 = células fotovoltaicas, dentro de 8541; coletada para ser SUBTRAÍDA
CONSULTAS = [  # (reporter, nome, flow)
    (156, "CHN", "X"),   # exportações da China
    (842, "USA", "M"),   # importações dos EUA
]
PAUSA = 5.0      # segundos entre chamadas, para não bater no limite (429)
TENTATIVAS = 4


def baixar(reporter, flow, cmd, ano):
    """Uma chamada à API. Devolve lista de dicts ou levanta exceção."""
    # Sem partnerCode a API devolve todos os parceiros. partner2Code=0 elimina
    # a quebra por segundo parceiro (sem ele o TOTAL estoura o teto de 500).
    # customsCode e motCode na URL causam erro 400 no modo preview, por isso
    # o filtro de modo de transporte/aduana é feito depois, em Python.
    url = (f"{BASE}?reporterCode={reporter}&period={ano}&cmdCode={cmd}"
           f"&flowCode={flow}&partner2Code=0")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    espera = 5
    for t in range(1, TENTATIVAS + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read().decode())
            if "data" not in d:
                raise ValueError(f"resposta sem 'data': {str(d)[:200]}")
            if d.get("count", 0) >= 500:
                print(f"  AVISO: {reporter} {flow} {cmd} {ano} bateu no teto de 500 linhas; "
                      "parceiros podem estar faltando.", file=sys.stderr)
            # mantém só o agregado por parceiro (todos os modos, aduana total)
            return [r for r in d["data"]
                    if r.get("motCode") in (0, "0") and r.get("customsCode") in ("C00", None)]
        except urllib.error.HTTPError as e:
            if e.code == 429 and t < TENTATIVAS:   # limite de taxa
                print(f"  429 (limite). Esperando {espera}s...", file=sys.stderr)
                time.sleep(espera); espera *= 2; continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            if t < TENTATIVAS:
                time.sleep(espera); espera *= 2; continue
            raise


CAMPOS = ["reporterCode", "reporterISO", "flowCode", "cmdCode", "refYear",
          "partnerCode", "partnerISO", "partnerDesc", "primaryValue", "netWgt"]
# partnerDesc vem vazio no preview; o nome é resolvido pelo partnerCode com a
# tabela de referência da própria Comtrade (baixada uma vez em ../brutos).


def tabela_parceiros():
    """Baixa (uma vez) a tabela código -> nome de parceiro da Comtrade."""
    arq = os.path.join(BRUTOS, "..", "comtrade_partnerAreas.json")
    if not os.path.exists(arq):
        u = "https://comtradeapi.un.org/files/v1/app/reference/partnerAreas.json"
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
            open(arq, "wb").write(r.read())
    ref = json.load(open(arq, encoding="utf-8"))
    return {int(x["id"]): x["text"] for x in ref["results"]}


def registrar_acesso(base, url, obs=""):
    """Grava base, URL e data/hora do acesso em ../log_acessos.csv (para a
    data de acesso das Referências ABNT)."""
    arq = os.path.join(AQUI, "..", "log_acessos.csv")
    novo = not os.path.exists(arq)
    with open(arq, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["base", "url", "data_hora_acesso", "observacao"])
        w.writerow([base, url, datetime.now().strftime("%Y-%m-%d %H:%M"), obs])


def main():
    feitos, falhas = 0, []
    nomes = tabela_parceiros()
    registrar_acesso("UN Comtrade (API pública v1 preview)", BASE,
                     f"reporters {[c[1] for c in CONSULTAS]}, códigos {CODIGOS}, anos {ANOS[0]}-{ANOS[-1]}")
    for reporter, nome, flow in CONSULTAS:
        for cmd in CODIGOS:
            for ano in ANOS:
                arq = os.path.join(BRUTOS, f"{nome}_{flow}_{cmd}_{ano}.csv")
                if os.path.exists(arq) and os.path.getsize(arq) > 100:
                    continue  # cache
                try:
                    linhas = baixar(reporter, flow, cmd, ano)
                except Exception as e:
                    print(f"FALHA {nome} {flow} {cmd} {ano}: {e}", file=sys.stderr)
                    falhas.append((nome, flow, cmd, ano)); time.sleep(PAUSA); continue
                for r in linhas:  # preenche o nome do parceiro
                    r["partnerDesc"] = nomes.get(int(r.get("partnerCode") or 0), r.get("partnerDesc"))
                with open(arq, "w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=CAMPOS, extrasaction="ignore")
                    w.writeheader(); w.writerows(linhas)
                feitos += 1
                print(f"ok {nome} {flow} {cmd} {ano}: {len(linhas)} linhas")
                time.sleep(PAUSA)

    # consolidado
    cons = os.path.join(TRATADOS, "comtrade_consolidado.csv")
    with open(cons, "w", newline="", encoding="utf-8") as out:
        w = csv.DictWriter(out, fieldnames=CAMPOS); w.writeheader()
        for a in sorted(os.listdir(BRUTOS)):
            if a.endswith(".csv"):
                with open(os.path.join(BRUTOS, a), encoding="utf-8") as f:
                    w.writerows(csv.DictReader(f))
    print(f"\nChamadas novas: {feitos}. Falhas: {len(falhas)}. Consolidado: {cons}")
    if falhas:
        print("Rode de novo para tentar as falhas:", falhas)


if __name__ == "__main__":
    main()
