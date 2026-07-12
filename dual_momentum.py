# -*- coding: utf-8 -*-
"""
Dual Momentum (Gary Antonacci) — fiel ao livro, na base do timestamp_certo.txt
  1. RELATIVO : fim de cada mes, ranqueia os 3 ativos pelo retorno de 12 meses.
  2. ABSOLUTO : o lider so entra se superar o CDI acumulado dos mesmos 12 meses.
  3. ALOCACAO : 100% no lider, ou 100% em caixa a CDI.
Sem look-ahead (sinal do mes t paga no mes t+1). Custos: 20 bps por perna.
Requer dados/base_plana.csv (gerada pelo montar_base.py).
"""
import pandas as pd
import numpy as np

CUSTO  = 0.0020
ATIVOS = ['PRIO3', 'ITUB3', 'ABEV3']
CDI_POR_ANO = {2016: 0.1400, 2017: 0.0993, 2018: 0.0642, 2019: 0.0596, 2020: 0.0276,
               2021: 0.0442, 2022: 0.1239, 2023: 0.1304, 2024: 0.1088, 2025: 0.1350,
               2026: 0.1500}

# %% 1) Fechamentos diarios (a linha 'dia' da base) -> precos de fim de mes
base = pd.read_csv('dados/base_plana.csv', parse_dates=['data'])
fech = (base[base['hora'] == 'dia'].set_index('data')[[f'{a}_fechamento' for a in ATIVOS]])
fech.columns = ATIVOS
mensal = fech.resample('ME').last()
retorno = mensal.pct_change()
cdi_mensal = (1 + pd.Series(mensal.index.year, index=mensal.index).map(CDI_POR_ANO)) ** (1/12) - 1
cdi_12m    = (1 + cdi_mensal).rolling(12).apply(np.prod, raw=True) - 1

# %% 2) As duas pernas do livro
momentum = mensal.pct_change(12)                                   # 12 meses, por calendario
lider    = momentum.dropna(how='all').idxmax(axis=1).reindex(momentum.index)
investe  = momentum.max(axis=1) > cdi_12m

peso = pd.DataFrame(0.0, index=mensal.index, columns=ATIVOS)
for t in peso.index[12:]:
    if investe.loc[t]:
        peso.loc[t, lider.loc[t]] = 1.0
caixa = 1 - peso.sum(axis=1)

# %% 3) Retorno (sinal de t paga em t+1) e resultados
ret_estrategia = ((peso.shift(1) * retorno).sum(axis=1) + caixa.shift(1) * cdi_mensal
                  - peso.diff().abs().sum(axis=1) * CUSTO).iloc[13:]
patrimonio = (1 + ret_estrategia).cumprod()
drawdown   = patrimonio / patrimonio.cummax() - 1

print('=== Dual Momentum fiel (12m por calendario, mensal, 20 bps) ===')
print(f'Periodo:        {ret_estrategia.index[0]:%Y-%m} a {ret_estrategia.index[-1]:%Y-%m}')
print(f'Sharpe:         {ret_estrategia.mean()/ret_estrategia.std()*np.sqrt(12):.2f}')
print(f'Max Drawdown:   {drawdown.min():.0%}  (regua mensal; na diaria e mais fundo)')
print(f'Retorno total:  {patrimonio.iloc[-1]-1:.0%}')
print(f'Tempo em caixa: {(caixa.iloc[13:] == 1).mean():.0%} dos meses | '
      f'trocas: {int((peso.diff().abs().sum(axis=1).iloc[13:] > 0).sum())} em {len(ret_estrategia)} meses')
print(f'Posicao hoje:   {lider.iloc[-1] if investe.iloc[-1] else "CAIXA"}')
