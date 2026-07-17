# -*- coding: utf-8 -*-
"""
Estrategia-propria — book E59: 130/30 classico, SEM CDI.

A regra em uma frase: toda sexta, ranqueio as 145 acoes por momentum de 1 mes,
compro as 20 melhores (+130% no total) e vendo as 10 piores (-30%). O short de
30% financia os 30% a mais de long. Nao ha CDI: a comparacao e relativa, uma
acao contra a outra.

Duas partes:
  1. book_130_30  — a regra em forma de funcao, curta, para LER e entender o
     mecanismo: ranking -> pesos -> execucao defasada -> PnL.
  2. bloco final  — le a serie ja calculada pelo motor do lab e guarda as
     metricas em variaveis nomeadas (aparecem no explorer do Spyder). Sem prints
     de debug: uma unica linha de resumo.

Spyder: abrir e F5 na raiz do repo.   Terminal: python3 estrategia_propria.py
"""
import sys
from pathlib import Path

import pandas as pd

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
from _paths import SAIDAS

# %% Parametros do book (o contrato E59)
TOP_N       = 20        # long: as 20 acoes de maior momentum
BOTTOM_N    = 10        # short: as 10 de menor momentum
PESO_LONG   = 1.30      # a perna long soma +130% do patrimonio
PESO_SHORT  = 0.30      # a perna short soma -30% (e ela que financia o long extra)
CUSTO_ORDEM = 0.0020    # 20 bps cada vez que um peso muda
# Sem CDI: caixa = 0 e o retorno e long menos short, so acoes contra acoes.


# %% A regra, em forma de funcao (o mecanismo, para ler devagar)
def book_130_30(precos, datas_sinal):
    """Retorno liquido diario do book E59 a partir de um painel de precos.

    precos       painel de precos ajustados (linhas = dias, colunas = acoes).
    datas_sinal  datas de rebalance (o ultimo pregao de cada semana).
    """
    # retorno diario de cada acao: e a materia-prima de todo o resto
    retorno_diario = precos.pct_change(fill_method=None)

    # tabela de pesos-alvo: um numero por acao, preenchida so nas datas de sinal
    pesos = pd.DataFrame(index=precos.index, columns=precos.columns, dtype=float)
    for t in datas_sinal:
        historia = precos.loc[:t]                          # so o passado ate t (nao espiar o futuro)
        preco_1m_atras = historia.asof(t - pd.DateOffset(months=1))
        momentum = (historia.iloc[-1] / preco_1m_atras - 1).dropna()   # quanto cada acao subiu no mes
        if len(momentum) < TOP_N + BOTTOM_N:               # poucas acoes elegiveis nesse dia: pulo
            continue
        linha = pd.Series(0.0, index=precos.columns)       # comeco o dia com todo mundo zerado
        linha[momentum.nlargest(TOP_N).index] = PESO_LONG / TOP_N       # +6,5% em cada vencedora
        linha[momentum.nsmallest(BOTTOM_N).index] = -PESO_SHORT / BOTTOM_N   # -3% em cada perdedora
        pesos.loc[t] = linha                               # essa e a carteira decidida na data t

    pesos = pesos.ffill().fillna(0.0)                      # seguro a posicao ate o proximo sinal
    pesos_ontem = pesos.shift(1).fillna(0.0)               # o peso de hoje so paga amanha (sem look-ahead)

    custo = pesos_ontem.diff().abs().sum(axis=1) * CUSTO_ORDEM       # 20 bps por peso que mudou
    retorno_bruto = (pesos_ontem * retorno_diario).sum(axis=1)      # long menos short; sem CDI
    return retorno_bruto - custo                                    # liquido = bruto menos custo


# %% Metricas canonicas (le a serie oficial do motor do lab; NAO recalcula aqui)
# O painel dos 145 nomes nao vem neste repo publico, entao o numero canonico e a
# serie exportada. Guardo tudo em variaveis para inspecionar no explorer do Spyder.
serie = pd.read_csv(SAIDAS / "estrategia_propria_diario.csv",
                    parse_dates=["dia"]).set_index("dia")

retorno_diario  = serie["retorno_liquido"]
patrimonio      = (1 + retorno_diario).cumprod()                 # curva de capital, base 1
retorno_total   = float(patrimonio.iloc[-1] - 1)                 # retorno acumulado da janela
sharpe          = float(retorno_diario.mean() / retorno_diario.std(ddof=1) * (252 ** 0.5))
max_drawdown    = float((patrimonio / patrimonio.cummax() - 1).min())
exposicao_long  = float(serie["exposicao_long"].mean())
exposicao_short = float(serie["exposicao_short"].mean())
caixa           = float(serie["caixa_cdi"].mean())

# unica saida: uma linha de resumo. O resto vive nas variaveis acima.
print(f"E59 130/30 sem CDI | ret {retorno_total:+.0%} | Sharpe {sharpe:.2f} | "
      f"MaxDD {max_drawdown:.0%} | long {exposicao_long:.2f} short {exposicao_short:.2f} caixa {caixa:.0f}")
