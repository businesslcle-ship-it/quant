"""
Dual Momentum (Gary Antonacci) — replicacao fiel ao livro (baseline)
--------------------------------------------------------------------
As regras do livro (GEM), aplicadas ao mesmo universo de 3 ativos:
  1. RELATIVO : no fim de cada mes, ranqueia pelos retornos de 12 meses.
  2. ABSOLUTO : o lider so entra se o retorno de 12m superar o CDI acumulado
                dos MESMOS 12 meses (analogo do T-bill do livro).
  3. ALOCACAO : 100% no lider, ou 100% em caixa a CDI. Sem fracoes, sem vol target.
Long-only, shift(1) (sem look-ahead), custo por ordem. Serve de baseline para
comparar contra a Rotacao v2 (ver comparativo.py).
"""
import pandas as pd
import numpy as np

ATIVOS      = ["PRIO3", "ITUB3", "ABEV3"]
LOOKBACK    = 12          # meses (o padrao do livro)
CUSTO_ORDEM = 0.0020      # 20 bps por perna (troca de acao = 2 pernas)
CDI_POR_ANO = {2008: 0.1238, 2009: 0.0988, 2010: 0.0975, 2011: 0.1160, 2012: 0.0841,
               2013: 0.0806, 2014: 0.1081, 2015: 0.1324, 2016: 0.1400, 2017: 0.0993,
               2018: 0.0642, 2019: 0.0596, 2020: 0.0276, 2021: 0.0442, 2022: 0.1239,
               2023: 0.1304, 2024: 0.1088, 2025: 0.1350, 2026: 0.1500}

# ============================ 1) DADOS: preco mensal (fim de mes) ============================
precos = pd.concat({a: pd.read_csv(f"dados/{a}.csv", parse_dates=["date"]).set_index("date")["adjustedClose"]
                    for a in ATIVOS}, axis=1, sort=True).loc["2008":]
# janela comum: onde os 3 ativos + 12m de historico existem (a PRIO entra em 2015)
INICIO = (precos.dropna().index[0] + pd.Timedelta(days=370)).strftime("%Y-%m")
precos_mensais = precos.resample("ME").last()
retorno_mensal = precos_mensais.pct_change()
cdi_mensal = (1 + pd.Series(precos_mensais.index.year, index=precos_mensais.index)
              .map(CDI_POR_ANO)) ** (1 / 12) - 1

# ============================ 2) A BARREIRA: CDI acumulado dos mesmos 12 meses ============================
cdi_12m = (1 + cdi_mensal).rolling(LOOKBACK).apply(np.prod, raw=True) - 1

# ============================ 3) SINAIS: as duas pernas do livro ============================
momentum_12m  = precos_mensais.pct_change(LOOKBACK)
lider         = momentum_12m.dropna(how="all").idxmax(axis=1).reindex(momentum_12m.index)
investe       = momentum_12m.max(axis=1) > cdi_12m           # perna absoluta

peso = pd.DataFrame(0.0, index=precos_mensais.index, columns=ATIVOS)
for t in peso.index[LOOKBACK:]:
    if investe.loc[t]:
        peso.loc[t, lider.loc[t]] = 1.0                      # perna relativa: 100% no lider
caixa = 1 - peso.sum(axis=1)

# ============================ 4) RETORNO (sinal do mes t paga no mes t+1) ============================
ret_acao  = (peso.shift(1) * retorno_mensal).sum(axis=1)
ret_caixa = caixa.shift(1) * cdi_mensal
giro      = peso.diff().abs().sum(axis=1)
liquido   = (ret_acao + ret_caixa - giro * CUSTO_ORDEM).iloc[LOOKBACK + 1:].loc[INICIO:]

# ============================ 5) RESULTADOS ============================
patrimonio = (1 + liquido).cumprod()
drawdown   = (patrimonio / patrimonio.cummax() - 1)
sharpe     = liquido.mean() / liquido.std() * np.sqrt(12)
print("=== Dual Momentum fiel (mensal, 12m, filtro vs CDI, 20 bps) ===")
print(f"Periodo:        {liquido.index[0]:%Y-%m} a {liquido.index[-1]:%Y-%m}  (janela dos 3 ativos)")
print(f"Sharpe:         {sharpe:.2f}")
print(f"Max Drawdown:   {drawdown.min():.0%}   (regua mensal; na diaria e mais fundo — ver comparativo.py)")
print(f"Retorno total:  {patrimonio.iloc[-1] - 1:.0%}")
print(f"Tempo em caixa: {(caixa.loc[INICIO:] == 1).mean():.0%} dos meses  |  "
      f"concentracao: 100% em 1 ativo quando investido")
