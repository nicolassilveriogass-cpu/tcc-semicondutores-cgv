# Memorial de construção das tabelas e figuras

Monografia: Geopolítica e cadeias globais de valor: a reorganização da produção de semicondutores no Leste Asiático após 2018 (Nicolas Silvério Gass, UFRGS; orientador Prof. Dr. Samuel Costa).

Este arquivo registra, para cada tabela e figura de elaboração própria, de onde vieram os dados, que consulta foi feita, que filtros e transformações foram aplicados, que decisões foram tomadas e por quê, que validações foram feitas e quando cada versão foi gerada. O objetivo é que qualquer leitor, o orientador ou a banca consiga refazer o caminho. O código está em `scripts\` e é a fonte última de verdade sobre o "como"; este memorial explica o "por quê". Regra do projeto: toda vez que uma tabela ou figura for regerada com mudança de regra, a ficha correspondente é atualizada no mesmo dia.

## 1. Estrutura da pasta `10. Dados`

`brutos\comtrade\`: uma resposta da API por arquivo, nomeada `<reporter>_<fluxo>_<código>_<ano>.csv` (ex.: `USA_M_8542_2019.csv`). São 264 arquivos: 2 reporters x 4 códigos x 30 anos (240) mais 2 x 4 subposições x 3 anos (24). Nunca são editados à mão.
`brutos\comtrade_partnerAreas.json`: tabela oficial de códigos de parceiro da Comtrade, usada para dar nome aos parceiros (o modo preview devolve `partnerDesc` vazio).
`brutos\tiva\`: 22 arquivos SDMX da TiVA 2025 (níveis, participações e parceiros).
`brutos\usgs\`: tabela de terras raras do USGS transcrita, com `LEIA-ME.txt` da conferência.
`tratados\`: consolidados (`comtrade_consolidado.csv`, `tiva_consolidado.csv`), as tabelas-base T1 a T4 e `resumo_tabelas.md`. `_antes_correcao_fotovoltaicas\` guarda a T1 gerada antes da exclusão do grupo 8541.4, para registro da diferença.
`figuras\`: PNG 300 dpi das figuras da monografia.
`scripts\`: `comtrade_coleta.py`, `coleta_85414x.py`, `tiva_coleta.py`, `tabelas.py`, `figuras.py` (reproduzidos no Apêndice A).
`log_acessos.csv`: base, URL, data e hora de cada execução de coleta. É de onde saem as datas de acesso das Referências; nunca é preenchido à mão.

Repositório público (espelho desta pasta): https://github.com/nicolassilveriogass-cpu/tcc-semicondutores-cgv (GASS, 2026), citado na seção 2.3 e no Apêndice A da monografia; clone local em `12. Github\tcc-semicondutores-cgv`.

Cadeia de reprodução: `python comtrade_coleta.py` e `python coleta_85414x.py` (cache: só baixam o que falta) -> `python tiva_coleta.py` -> `python tabelas.py` -> `python figuras.py`. Rodar `tabelas.py` e `figuras.py` sem recoletar reproduz exatamente as tabelas e figuras atuais, porque os brutos não mudam.

## 2. Decisões transversais (valem para todas as tabelas de comércio)

Fonte. UN Comtrade Database, API pública v1, modo preview, sem chave (`https://comtradeapi.un.org/public/v1/preview/C/A/HS`). Reporters: China (156) para exportações (fluxo X) e Estados Unidos (842) para importações (fluxo M). Valores em US$ correntes (`primaryValue`), anuais, classificação HS conforme reportada em cada ano.

Por que os Estados Unidos vêm da Comtrade e não do Census. O projeto previa Census Bureau e BEA; durante a execução a API do Census passou a exigir credencial. Os Estados Unidos reportam à ONU importações em base CIF (valor mais frete e seguro), enquanto o Census publica valor aduaneiro. Conferido em 2017: US$ 525,8 bi (Comtrade) contra US$ 505,6 bi (Census), diferença de cerca de 4%. Como o frete incide de forma parecida sobre todas as origens, as participações quase não mudam (China em 2017: 21,9% na Comtrade; 21,6% em Freund et al., 2024, com dados do Census). Consequência: todas as comparações com a literatura são feitas em participações, nunca em níveis.

Definição de semicondutores. Posições HS 8541 (diodos, transistores e dispositivos semicondutores similares; dispositivos fotossensíveis; LEDs) e 8542 (circuitos integrados), menos o grupo 8541.4 (dispositivos fotossensíveis, inclusive células fotovoltaicas montadas ou não em módulos, e LEDs). Motivo: a China é a maior exportadora mundial de painéis solares e o grupo 8541.4 responde por 57% a 82% do valor da posição 8541 nas duas pontas em todo o período recente; sem a exclusão, "semicondutores" seria na prática "painéis solares". A definição fica próxima da usada pela Semiconductor Industry Association, que exclui os produtos solares. Codificação: 854140 até 2021; a revisão HS 2022 desdobrou o grupo em 854141, 854142, 854143 e 854149, coletados para 2022 a 2024 e somados. Em `tabelas.py`, qualquer código que comece com `85414` entra com sinal negativo no grupo SEMICOND. Descoberta em 28/09/2026: a primeira versão das tabelas (25/09) não fazia a exclusão; o efeito está registrado na ficha da T1.

Filtros na leitura da API. Os parâmetros `customsCode` e `motCode` na URL devolvem erro 400 no modo preview, por isso a API é chamada sem eles e o filtro é feito em Python: mantêm-se só as linhas com modo de transporte total (`motCode` 0) e regime aduaneiro total (`customsCode` C00), o que evita dupla contagem. `partner2Code=0` elimina a quebra por segundo parceiro (sem ele o TOTAL ultrapassa o teto de 500 linhas do preview). A chamada é feita sem `partnerCode`, o que devolve todos os parceiros de uma vez; o script avisa se alguma resposta bater no teto de 500 linhas (nenhuma bateu).

Taiwan. Na Comtrade aparece como "Other Asia, nes" (código 490), designação que a base usa para essa economia; os fluxos são atribuídos a Taiwan e a designação é indicada nas tabelas. Na TiVA aparece como "Chinese Taipei" (TWN).

Hong Kong. Aparece como grande destino das exportações chinesas de semicondutores por seu papel de entreposto; parte do fluxo é reexportada e a base não permite separar. Fica registrado como limitação, sem ajuste.

Recorte temporal. Série completa 1995-2024 (coincide com a cobertura da TiVA e a criação da OMC). Nas comparações de antes e depois, 2018 é ano de transição e fica fora dos dois lados: "pré" = média simples de 2013 a 2017; "pós" = média simples de 2019 a 2024. Médias de vários anos reduzem o peso da queda de 2020 e do pico de 2021-2022. Nas séries da TiVA, que terminam em 2022, o "pós" fica restrito a 2019-2022.

Validação dos dados baixados. Nove células foram conferidas por chamada isolada à API (com parceiro explícito na URL, caminho diferente do usado na coleta) e coincidiram com os valores gravados: em 25/09/2026, EUA<-China 8542 2024; EUA<-China TOTAL 2017; China->Vietnã 8542 2023; China->Brasil 8542 2022; EUA<-Malásia 8541 2019; em 28/09/2026, quatro células adicionais após a inclusão do grupo 8541.4. Checagem externa: participação da China nas importações totais dos EUA em 2017 (21,9%) contra Freund et al. (2024): 21,6%.

## 3. Fichas

### T1. Ranking de destinos das exportações da China, pré x pós 2018
Arquivo: `tratados\T1_china_destinos_ranking.csv`. Gerada por `tabelas.py`, função `t1_china_destinos`. Versão atual: 28/09/2026 14h09 (com exclusão do grupo 8541.4).
Pergunta: o lado chinês da sub-hipótese de composição geográfica. Para onde a China passou a exportar, e se o movimento é mais forte em semicondutores do que no total (sub-hipótese de seletividade setorial). Pedido do orientador na conversa de setembro.
Cálculo: para cada grupo (TOTAL e SEMICOND) e cada parceiro, média das exportações em 2013-2017 e em 2019-2024; participação = média do parceiro dividida pela média do Mundo (parceiro 0) no mesmo período; ranking pelo valor médio em cada período; `var_rank` = posição pré menos posição pós (positivo = subiu). Guardados os 30 maiores de cada grupo.
Leitura principal (SEMICOND): Hong Kong cai de 55,6% para 42,6%; Coreia do Sul sobe de 9,3% para 13,1% (3º para 2º); Taiwan 11,8% para 12,8%; Vietnã salta do 8º para o 4º destino (2,0% para 8,8%); Índia do 12º para o 7º; Estados Unidos caem do 6º para o 9º (2,8% para 1,5%); Cingapura cai do 4º para o 6º. No TOTAL as posições quase não mudam (EUA 1º, Hong Kong 2º, Japão 3º), com Vietnã de 6º para 5º.
Efeito da correção das fotovoltaicas (versão de 25/09 em `_antes_correcao_fotovoltaicas`): Brasil e Países Baixos figuravam entre os 12 maiores destinos "de semicondutores" da China; eram painéis solares. Saíram do top 12 depois da exclusão.
Uso na monografia: Tabela 2 do capítulo 3 (seção 3.3.1), em formato compacto (top 12 do SEMICOND com participação e posição nos dois períodos; TOTAL como contraste).

### T2. Participação por origem nas importações dos Estados Unidos, por ano
Arquivo: `tratados\T2_eua_origens_share.csv`. Função `t2_eua_origens`. Versão atual: 28/09/2026 14h09.
Pergunta: o lado americano da composição geográfica, replicando para semicondutores a lógica da Figura 2 de Freund et al. (2024), que trabalha com o total.
Cálculo: para cada grupo e ano de 1995 a 2024, participação de cada origem selecionada = valor da origem dividido pelo valor do Mundo (parceiro 0), em %. Origens: China (156), Taiwan (490), Coreia do Sul (410), Vietnã (704), México (484), Malásia (458), Japão (392), Brasil (76). Malásia entra porque é a maior origem de semicondutores dos EUA (montagem e teste, OSAT); Brasil entra para o adendo e mostra participação nula em semicondutores.
Leitura principal (SEMICOND): China de 9,9% (2017) para 4,2% (2024); Taiwan de 11,3% para 26,2%; Malásia de 35,5% (2017) e pico de 44,5% (2020) para 22,5% (2024); Vietnã sobe até 7,4% (2020) e recua para 3,6%. No TOTAL: China de 21,9% para 13,8%; México de 13,1% para 15,2%; Vietnã de 2,0% para 4,2%; Taiwan de 1,8% para 3,5%.
Uso na monografia: painel (a) da Figura 1 (séries de China, Taiwan, Coreia do Sul, Malásia, Vietnã e Japão) e Tabela 1 do capítulo 3 (médias pré e pós por origem, setor contra total).

### T3. TiVA, atividade C26: exportações brutas e valor adicionado
Arquivo: `tratados\T3_tiva_C26.csv`. Função `t3_tiva`, a partir de `tiva_consolidado.csv` gerado por `tiva_coleta.py`. Coleta em 25/09/2026 17h54; tabela regerada em 28/09 sem mudança de regra.
Fonte: OCDE, Trade in Value Added, edição 2025 (1995-2022), via SDMX no endpoint `sti-public` (o endpoint `public` devolve erro 500 para esses fluxos). Dataflows `DSD_TIVA_MAINLV@DF_MAINLV` (níveis, US$ milhões) e `DSD_TIVA_MAINSH@DF_MAINSH` (participações, % das exportações brutas). Economias coletadas: CHN, KOR, TWN, USA, JPN, VNM, MEX, BRA e Mundo; atividades total, manufatura (C) e C26; medidas EXGR, EXGR_INT, EXGR_FNL, EXGR_DVA, EXGR_FVA, VALU; participação por destino (EXGR_PSH, EXGR_DVA_PSH) em C26 para CHN, KOR, TWN e USA.
Por que C26. É a abertura mais fina em que a TiVA cobre os semicondutores (fabricação de computadores, produtos eletrônicos e ópticos, ISIC rev. 4); não existe C261. Limitação declarada na seção 2.7: os indicadores se referem ao conjunto da eletrônica, no qual os semicondutores são a parte de maior peso para as três economias, mas não a única.
Por que a edição 2025 e não a 2023 do projeto. É a edição vigente e estende a cobertura até 2022, o que inclui três anos do pós-2018. Registrado como ajuste em relação ao projeto.
Filtro da T3: C26, contraparte Mundo, 2005-2022, medidas EXGR, EXGR_DVA, EXGR_FVA e EXGR_INT, para CHN, KOR, TWN, USA, VNM e MEX, em níveis e em participações.
Leitura principal (participação do VA doméstico nas exportações brutas de C26): Taiwan sobe de 53% (2010) para 71% (2022); China e Coreia estáveis em torno de 71-73%; Vietnã e México em torno de 45%, padrão típico de montagem.
Uso na monografia: Figura 2 do capítulo 3 (seção 3.3.2) e apoio ao 4.1 e 4.2.

### T4. Índice de Herfindahl-Hirschman das origens das importações dos EUA
Arquivo: `tratados\T4_eua_hhi_origens.csv`. Função `t4_hhi`. Versão atual: 28/09/2026 14h09.
Pergunta: resumir em um número, ano a ano, quão concentrada é a pauta de origem, para ver se a reorganização diversificou ou concentrou os fornecedores.
Cálculo: para cada grupo e ano, participação de cada parceiro com valor positivo (excluído o Mundo) sobre o total; HHI = 10.000 x soma dos quadrados das participações (escala 0 a 10.000). Grava também a maior participação e o número de origens. Usa todos os parceiros reportados, não só os selecionados da T2.
Leitura principal (SEMICOND): HHI em torno de 900-1.000 nos anos 2000; sobe a ~1.700 em 2016-2017, a ~2.300 em 2019-2021 (concentração na Malásia) e recua a ~1.400 em 2023-2024 (Taiwan cresce, Malásia cai). O TOTAL fica estável entre 750 e 950 no período inteiro.
Uso na monografia: painel (b) da Figura 1 e Tabela 1 do capítulo 3.

### Figura 1. Participação de origens selecionadas nas importações de semicondutores dos EUA e concentração da pauta de origem, 1995-2024
Arquivo: `figuras\Figura_1.png`. Gerada por `figuras.py` em 29/09/2026 11h32, a partir de T2 (painel a) e T4 (painel b). Aprovada pelo Nicolas em 29/09/2026.
Regras gráficas: legível em preto e branco (cada série com cor, traço e marcador distintos); faixa cinza marcando o período posterior a 2018; painel (a) limitado a 0-50% para não achatar as séries; 300 dpi; fonte serifada (Times New Roman quando disponível; na máquina em que foi gerada, Liberation Serif). Título ABNT acima ("Figura 1 – ...") e fonte abaixo ("Fonte: elaboração própria a partir de United Nations (2026)"), com nota sobre a definição de semicondutores e sobre Taiwan.
Uso na monografia: seção 3.3.1.

### Tabela 1 (cap. 3, seção 3.3.1). Participação de origens selecionadas nas importações dos EUA e concentração da pauta de origem, semicondutores e total: médias de 2013-2017 e 2019-2024
Arquivo: `tratados\Tabela1_cap3.csv`. Gerada por `scripts\tabela1_cap3.py` em 29/09/2026 a partir de T2 (participações) e T4 (HHI). Inserida no consolidado de 29/09.
Pergunta: a sub-hipótese de composição geográfica do lado americano, lida junto com a de seletividade setorial: quem perdeu e quem ganhou espaço nas importações de semicondutores dos EUA depois de 2018, e se o movimento foi mais forte no setor do que no total.
Cálculo: para cada origem (China, Taiwan, Coreia do Sul, Malásia, Vietnã, Japão, México) e cada grupo (semicondutores e total), média simples das participações anuais em 2013-2017 e em 2019-2024; variação = diferença entre as duas médias (em pontos percentuais), calculada sobre os valores arredondados para que bata com as colunas impressas. Última linha: média do HHI anual de T4 em cada período; variação em pontos. Optou-se pela média simples das participações anuais, e não pela razão entre médias de valores, porque é a leitura mais direta do que o leitor vê na Figura 1; a diferença entre os dois critérios é de décimos de ponto.
Leitura principal: nos semicondutores, China cai de 8,8% para 6,0% (queda relativa de cerca de um terço) e Japão de 6,0% para 3,7%; Taiwan sobe de 11,7% para 16,5%, Malásia de 29,3% para 34,8%, México de 2,3% para 4,4%; Coreia e Vietnã quase estáveis. No total, China cai de 21,0% para 16,8% (queda relativa de um quinto), México e Vietnã sobem. O HHI dos semicondutores sobe de 1.489 para 1.815 (concentração maior), enquanto o do total recua de 904 para 779. Leitura para a hipótese: a reorganização é mais forte no setor do que no agregado, e no setor ela concentrou (Malásia e Taiwan) em vez de diversificar.
Validação (29/09): recomputada por segundo caminho, com pandas direto do `comtrade_consolidado.csv` (sem passar por T2 e T4): China 8,75 e 6,0; Taiwan 11,7 e 16,5; Malásia 29,3 e 34,8; México 2,3 e 4,4; HHI 1.489 e 1.815. Tudo igual. A média da China no pré é exatamente 8,750, arredondada para 8,8. Para evitar diferenças de arredondamento, T2 passou a gravar as participações com quatro decimais (antes, dois); os valores exibidos não mudam.
Formato na monografia: padrão IBGE/ABNT (sem bordas laterais, linhas horizontais só no topo, abaixo do cabeçalho, antes do HHI e no fim), título acima, fonte e notas abaixo em 10 pt.

### Tabela 2 (cap. 3, seção 3.3.1). Principais destinos das exportações chinesas de semicondutores: posição e participação nas médias de 2013-2017 e 2019-2024
Arquivo: `tratados\Tabela2_cap3.csv`. Gerada por `scripts\tabela2_cap3.py` em 29/09/2026 a partir de T1. Inserida no consolidado de 29/09, logo após a Figura 1.
Pergunta: o lado chinês da composição geográfica, pedido pelo orientador: para onde a China passou a exportar semicondutores depois de 2018 e se o mapa de destinos mudou mais no setor do que no total.
Cálculo: os doze maiores destinos pela média de 2019-2024; para cada um, posição e participação nos dois períodos (participação = média das exportações ao destino no período dividida pela média do total exportado, critério de T1), variação em pontos percentuais sobre os valores arredondados e, como contraste, a posição do mesmo destino nas exportações totais da China em 2019-2024. Nomes traduzidos (Hong Kong, Coreia do Sul, Taiwan, Vietnã, Malásia, Cingapura, Índia, Japão, Estados Unidos, Alemanha, Filipinas, Tailândia).
Observação sobre o critério: Tabela 1 usa média simples das participações anuais e Tabela 2 usa razão entre médias de valores. São critérios próximos (diferença de décimos de ponto) e cada um segue a tabela-base de que deriva (T2 e T1); a nota de fonte de cada tabela diz qual foi usado.
Leitura principal: Hong Kong continua o primeiro destino, mas cai de 55,6% para 42,6%; Coreia do Sul passa de 3º para 2º (9,3% para 13,1%); Taiwan de 2º para 3º (11,8% para 12,8%); Vietnã salta do 8º para o 4º (2,0% para 8,8%), a maior variação positiva; Índia do 12º para o 7º; Cingapura cai do 4º para o 6º; Estados Unidos caem do 6º para o 9º (2,8% para 1,5%), embora sigam o 1º destino no total. O contraste com a última coluna mostra que o mapa de destinos de semicondutores é asiático e diferente do mapa do comércio total.
Validação (29/09): recomputada por segundo caminho com pandas direto do `comtrade_consolidado.csv` (sem passar por T1): os doze destinos, as posições no pré e as participações nos dois períodos coincidem.
Formato na monografia: padrão IBGE/ABNT, título acima, fonte e notas abaixo em 10 pt; começa em página nova para não quebrar.

### Figura 2 (cap. 3, seção 3.3.2). Participação do valor adicionado doméstico nas exportações brutas de computadores, produtos eletrônicos e ópticos (atividade C26), economias selecionadas, 2005-2022
Arquivo: `figuras\Figura_2.png`. Gerada por `figuras.py` (função `fig2`) em 29/09/2026 a partir de T3 (indicador EXGR_DVA em participação, TiVA 2025, contraparte Mundo). Inserida no consolidado de 29/09, seção 3.3.2.
Pergunta: se a realocação do comércio bruto veio acompanhada de mudança em quem captura valor, que é o que a hipótese pede e o comércio bruto não responde. Séries: China, Taiwan, Coreia do Sul, Vietnã, México e, como referência de economia a montante, Estados Unidos.
Regras gráficas: mesmas da Figura 1 (preto e branco, traços e marcadores distintos, faixa cinza pós-2018, 300 dpi, fonte serifada). Eixo vertical de 30% a 100% para acomodar os Estados Unidos sem achatar as demais séries.
Leitura principal: Taiwan sobe de 52,8% (2010) para 71,2% (2022), e a maior parte da subida ocorre depois de 2014, chegando ao patamar de China e Coreia (em torno de 71-73%) justamente no pós-2018; China oscila entre 68% e 73% desde 2010; Coreia entre 63% e 73%, com queda em 2022; Vietnã cai de 53,9% (2010) para 44,2% (2022) e México fica em torno de 45%, o padrão de quem monta insumos importados; Estados Unidos entre 89% e 95%. Leitura para a hipótese: a realocação para Vietnã e México (Tabelas 1 e 2) não veio com aumento de captura de valor nessas economias; nas três do Leste Asiático, quem mais mudou foi Taiwan, que passou a reter mais valor ao mesmo tempo em que ganhou participação nas importações americanas.
Validação (29/09): valores de TWN, CHN e VNM em 2010, 2018 e 2022 conferidos diretamente nos arquivos SDMX brutos (`brutos\tiva\shares_*.csv`, filtro MEASURE=EXGR_DVA, ACTIVITY=C26, COUNTERPART_AREA=W), sem passar por T3: idênticos.
Limite declarado (seção 2.7): C26 é mais amplo que semicondutores; a base termina em 2022.

### Tabela 3 (cap. 4, adendo 4.3). Produção e reservas de terras raras por país, 2024-2025
Arquivo: `tratados\Tabela3_cap4.csv`. Gerada por `scripts\tabela3_cap4.py` em 29/09/2026 a partir da transcrição conferida do USGS (`brutos\usgs\usgs_mcs2026_terras_raras.csv`). Inserida no consolidado de 29/09, seção 4.3.
Pergunta: onde o Brasil está na cadeia de minerais críticos que alimenta os semicondutores e os ímãs, e quão concentrada é a produção, para sustentar o adendo pedido pelo orientador.
Cálculo: países ordenados pelas reservas (decrescente); os sem reserva reportada vêm depois, ordenados pela produção de 2025; participações na produção sobre o total mundial de 2025 (390.000 t) e nas reservas sobre 85.000.000 t. Como a fonte informa as reservas mundiais como "mais de 85 milhões", as participações nas reservas são um teto (o Brasil tem até 24,7%, por exemplo). Nomes traduzidos. Unidade: toneladas de óxidos de terras raras (REO), como na fonte.
Leitura principal: a China produz 69,2% e detém 51,8% das reservas; o Brasil tem a segunda maior reserva (21 milhões de t, 24,7%) e produz 0,5% (2.000 t estimadas em 2025, contra 560 em 2024); Estados Unidos produzem 13,1% com 2,2% das reservas; Mianmar é o terceiro produtor (5,6%) sem reserva reportada; Austrália 7,4% nos dois. O contraste reserva x produção do Brasil é o dado que abre o adendo, e a concentração chinesa na mineração (e, pela CGEE, no refino) é o ponto de estrangulamento no sentido de Farrell e Newman.
Validação (29/09): a transcrição já tinha sido conferida célula a célula contra o PDF em 28/09; as participações batem com o que a CGEE (2026) reporta a partir da mesma família de dados (Brasil com cerca de 25% das reservas, 21 Mt, segunda atrás da China; China com 69% da mineração em 2024), o que serve de segundo caminho.
Ressalva da fonte: reservas de alguns países seguem critérios distintos (Austrália informa 6,3 Mt, mas as reservas no padrão JORC eram 3,3 Mt); a China e Mianmar têm cotas de produção. Registrado na nota da tabela.

### USGS. Produção e reservas de terras raras por país
Arquivo: `brutos\usgs\usgs_mcs2026_terras_raras.csv`, com `LEIA-ME.txt`. Transcrita em 25/09/2026 da tabela "World Mine Production and Reserves" de Johnston (2026), Mineral Commodity Summaries 2026, USGS, em toneladas de óxidos de terras raras. Conferida célula a célula contra o PDF em 28/09/2026: todos os valores batem; os expoentes junto aos números no PDF são chamadas de nota da tabela, não dígitos. Ressalva da própria fonte: as reservas reportadas por alguns países seguem critérios distintos (a Austrália, por exemplo, informa 6,3 Mt, mas as reservas em padrão JORC eram 3,3 Mt).
Uso na monografia: tabela do adendo 4.3 (Brasil como segunda maior reserva; China dominante na produção).

## 4. Tabelas e figuras ainda a construir (a partir das bases acima)
Todas as peças previstas para os capítulos 3 e 4 estão geradas. Novas peças, se surgirem na redação, ganham ficha aqui no dia em que forem geradas.

## 5. Histórico de versões
25/09/2026: coleta Comtrade 2013-2024 (TOTAL, 8541, 8542); TiVA 2025; USGS transcrito; T1, T2 e T3 v1; validação de cinco células.
28/09/2026: coleta estendida a 1995-2024; descoberta de que o grupo 8541.4 (fotovoltaicas e LEDs) é 57-82% da posição 8541; coleta de 854140 e de 854141/42/43/49; regra SEMICOND = 8541 + 8542 menos 8541.4; T1 a T4 regeradas; USGS conferido célula a célula; quatro células adicionais validadas; versão anterior da T1 arquivada.
29/09/2026: Figura 1 gerada e aprovada; este memorial criado; Tabelas 1 e 2 e Figura 2 do cap. 3 geradas, validadas por segundo caminho e aprovadas pelo Nicolas; Tabela 3 (terras raras, adendo 4.3) gerada; T2 regerada com quatro decimais (sem mudança de regra).
