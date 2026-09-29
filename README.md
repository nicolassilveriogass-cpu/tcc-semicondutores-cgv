# Geopolítica e cadeias globais de valor: dados e rotinas da monografia

Material de reprodutibilidade da monografia **"Geopolítica e cadeias globais de valor: a reorganização da produção de semicondutores no Leste Asiático após 2018"**, de Nicolas Silvério Gass (Ciências Econômicas, Faculdade de Ciências Econômicas, UFRGS, 2026), orientada pelo Prof. Dr. Samuel Costa.

Este repositório contém tudo o que é preciso para refazer as tabelas e figuras do trabalho: os dados brutos exatamente como foram baixados das fontes, as rotinas de coleta e tratamento, as tabelas tratadas, as figuras e um memorial com o racional de cada peça.

## Estrutura

| Pasta ou arquivo | Conteúdo |
|---|---|
| `scripts/` | Rotinas em Python (coleta na UN Comtrade e na OCDE TiVA, montagem das tabelas-base, tabelas do capítulo 3, figuras) |
| `brutos/comtrade/` | Uma resposta da API pública da Comtrade por arquivo: `<reporter>_<fluxo>_<código>_<ano>.csv` (264 arquivos) |
| `brutos/tiva/` | Extrações SDMX da OCDE TiVA, edição 2025 (níveis, participações, parceiros) |
| `brutos/usgs/` | Tabela de terras raras do USGS Mineral Commodity Summaries 2026, transcrita e conferida |
| `tratados/` | Consolidados, tabelas-base T1 a T4 e as tabelas do capítulo 3 |
| `figuras/` | Figuras da monografia em PNG, 300 dpi |
| `MEMORIAL_TABELAS.md` | Ficha de cada tabela e figura: pergunta, fonte, consulta, filtros, decisões, validações e histórico de versões |
| `log_acessos.csv` | Base, URL, data e hora de cada execução de coleta (origem das datas de acesso nas Referências) |

## Como reproduzir

Requisitos: Python 3.10 ou superior e as bibliotecas em `requirements.txt` (`pip install -r requirements.txt`). Os scripts usam só a biblioteca padrão para coleta e tratamento; `matplotlib` é necessário apenas para as figuras.

```bash
cd scripts
python comtrade_coleta.py    # só baixa o que ainda não está em brutos/comtrade (cache)
python coleta_85414x.py      # subposições 854141 a 854149 (HS 2022), 2022 a 2024
python tiva_coleta.py        # OCDE TiVA 2025 via SDMX
python tabelas.py            # T1 a T4 e resumo_tabelas.md
python tabela1_cap3.py       # Tabela 1 do capítulo 3
python tabela2_cap3.py       # Tabela 2 do capítulo 3
python figuras.py            # Figuras 1 e 2
```

Como os dados brutos já estão no repositório, rodar `tabelas.py` e os scripts seguintes reproduz exatamente as tabelas e figuras da monografia sem nenhuma nova chamada às APIs.

## Definições que valem para todas as tabelas

Semicondutores = posições 8541 e 8542 do Sistema Harmonizado, excluído o grupo 8541.4 (dispositivos fotossensíveis, inclusive células fotovoltaicas, e LEDs): código 854140 até 2021 e 854141, 854142, 854143 e 854149 desde a revisão HS 2022. Nas comparações de antes e depois, o período anterior é a média de 2013 a 2017 e o posterior a média de 2019 a 2024; 2018 fica fora como ano de transição. Taiwan aparece na Comtrade como "Other Asia, nes" (código 490) e na TiVA como "Chinese Taipei" (TWN). O detalhamento e as validações estão no `MEMORIAL_TABELAS.md`.

## Fontes dos dados

- UNITED NATIONS. UN Comtrade Database. United Nations Statistics Division. https://comtradeplus.un.org/ (API pública v1, modo preview).
- OCDE. Trade in Value Added (TiVA) database, edição 2025. https://www.oecd.org/en/topics/sub-issues/trade-in-value-added.html
- JOHNSTON, S. N. Rare earths. In: U.S. GEOLOGICAL SURVEY. Mineral commodity summaries 2026. https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-rare-earths.pdf

Os dados pertencem às respectivas fontes e são redistribuídos aqui apenas para fins acadêmicos de reprodutibilidade, nas condições de uso de cada uma. O código está sob licença MIT.

## Como citar

GASS, Nicolas Silvério. Geopolítica e cadeias globais de valor: dados e rotinas da monografia. 2026. Repositório GitHub. Disponível em: [endereço do repositório]. Acesso em: [data].
