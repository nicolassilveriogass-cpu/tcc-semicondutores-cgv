# -*- coding: utf-8 -*-
"""Coleta complementar: subposições 854141/42/43/49 (HS 2022) para 2022-2024,
que substituíram a 854140. Reaproveita as funções de comtrade_coleta.py."""
import csv, os, sys, time
import comtrade_coleta as cc
nomes = cc.tabela_parceiros()
cc.registrar_acesso("UN Comtrade (API pública v1 preview)", cc.BASE, "complemento 854141/42/43/49, 2022-2024, CHN X e USA M")
for reporter, nome, flow in cc.CONSULTAS:
    for cmd in ["854141", "854142", "854143", "854149"]:
        for ano in (2022, 2023, 2024):
            arq = os.path.join(cc.BRUTOS, f"{nome}_{flow}_{cmd}_{ano}.csv")
            if os.path.exists(arq) and os.path.getsize(arq) > 100:
                continue
            try:
                linhas = cc.baixar(reporter, flow, cmd, ano)
            except Exception as e:
                print("FALHA", nome, flow, cmd, ano, e, file=sys.stderr); time.sleep(cc.PAUSA); continue
            for r in linhas:
                r["partnerDesc"] = nomes.get(int(r.get("partnerCode") or 0), r.get("partnerDesc"))
            with open(arq, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=cc.CAMPOS, extrasaction="ignore"); w.writeheader(); w.writerows(linhas)
            print("ok", nome, flow, cmd, ano, len(linhas)); time.sleep(cc.PAUSA)
