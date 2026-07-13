# -*- coding: utf-8 -*-
"""
Grafico da apresentacao: Dual Momentum fiel vs Buy & Hold 1/3 vs CDI
Mesma logica e mesmos numeros do dual_momentum_livro.py (grade MENSAL, 20 bps).
Gera dm_vs_benchmark.png (patrimonio em escala log + drawdown).
Rodar da raiz Quantitative: python3 dual_momentum/dual_momentum_graf.py
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CUSTO  = 0.0020
ATIVOS = ['PRIO3', 'ITUB3', 'ABEV3']
CDI_POR_ANO = {2016: 0.1400, 2017: 0.0993, 2018: 0.0642, 2019: 0.0596, 2020: 0.0276,
               2021: 0.0442, 2022: 0.1239, 2023: 0.1304, 2024: 0.1088, 2025: 0.1350,
               2026: 0.1500}

# %% 1) Mesma preparacao do dual_momentum_livro.py
base = pd.read_csv('dados/base_plana.csv', parse_dates=['data'])
fech = (base[base['hora'] == 'dia'].set_index('data')[[f'{a}_fechamento' for a in ATIVOS]])
fech.columns = ATIVOS
mensal = fech.resample('ME').last()
retorno = mensal.pct_change()
cdi_mensal = (1 + pd.Series(mensal.index.year, index=mensal.index).map(CDI_POR_ANO)) ** (1/12) - 1
cdi_12m    = (1 + cdi_mensal).rolling(12).apply(np.prod, raw=True) - 1

momentum = mensal.pct_change(12)
lider    = momentum.dropna(how='all').idxmax(axis=1).reindex(momentum.index)
investe  = momentum.max(axis=1) > cdi_12m
matriz_lider = pd.get_dummies(lider).reindex(index=mensal.index, columns=ATIVOS, fill_value=False)
peso  = matriz_lider.mul(investe, axis=0).astype(float)
caixa = 1 - peso.sum(axis=1)

# %% 2) As tres curvas no MESMO periodo (sinal de t paga em t+1)
ret_dm  = ((peso.shift(1) * retorno).sum(axis=1) + caixa.shift(1) * cdi_mensal
           - peso.diff().abs().sum(axis=1) * CUSTO).iloc[13:]
ret_bh  = retorno.mean(axis=1).iloc[13:]                # 1/3 em cada acao, rebalanceado ao mes
ret_cdi = cdi_mensal.iloc[13:]

def resumo(r):
    eq = (1 + r).cumprod()
    return eq, r.mean() / r.std() * np.sqrt(12), (eq / eq.cummax() - 1).min()

eq_dm, sh_dm, dd_dm = resumo(ret_dm)
eq_bh, sh_bh, dd_bh = resumo(ret_bh)
eq_cdi = (1 + ret_cdi).cumprod()

# %% 3) O grafico: patrimonio (log) em cima, drawdown embaixo
fig, (em_cima, embaixo) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                       gridspec_kw={'height_ratios': [3, 1]})
em_cima.plot(eq_dm, color='#0b6e4f', lw=2,
             label=f'Dual Momentum (livro)  Sharpe {sh_dm:.2f} | MaxDD {dd_dm:.0%} | {eq_dm.iloc[-1]-1:+.0%}')
em_cima.plot(eq_bh, color='#d17a22', lw=1.6,
             label=f'Buy & Hold 1/3              Sharpe {sh_bh:.2f} | MaxDD {dd_bh:.0%} | {eq_bh.iloc[-1]-1:+.0%}')
em_cima.plot(eq_cdi, color='gray', lw=1.2, ls='--', label=f'CDI  {eq_cdi.iloc[-1]-1:+.0%}')
em_cima.set_yscale('log')
em_cima.set_title('Dual Momentum fiel ao livro vs benchmark — grade mensal, liquido de 20 bps')
em_cima.legend(loc='upper left', fontsize=9)
em_cima.grid(alpha=0.3)

embaixo.fill_between(eq_dm.index, eq_dm / eq_dm.cummax() - 1, 0, color='#0b6e4f', alpha=0.5)
embaixo.fill_between(eq_bh.index, eq_bh / eq_bh.cummax() - 1, 0, color='#d17a22', alpha=0.35)
embaixo.set_ylabel('Drawdown')
embaixo.grid(alpha=0.3)

fig.tight_layout()
fig.savefig('dm_vs_benchmark.png', dpi=150)
print(f'dm_vs_benchmark.png salvo | DM: Sharpe {sh_dm:.2f}, MaxDD {dd_dm:.0%} | '
      f'B&H: Sharpe {sh_bh:.2f}, MaxDD {dd_bh:.0%}')
