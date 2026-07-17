# -*- coding: utf-8 -*-
"""
Estrategia-propria — book E59: 130/30 classico, SEM CDI.

Este arquivo tem duas partes:
  1. book_130_30 : implementacao de REFERENCIA da regra, curta e legivel
     (ranking momentum 1m -> pesos 130/30 -> shift(1) -> PnL liquido).
  2. __main__    : imprime as metricas canonicas a partir da serie publicada
     (dados/saidas/estrategia_propria_diario.csv), exportada do motor do lab.

Os NUMEROS publicados vem do motor canonico do lab (ramo E59 em
rotacao/experimentos/motores/ranking_path_b.py); aqui esta a mesma logica em
forma minima. Para rodar book_130_30 de ponta a ponta e preciso um painel de
precos do universo Path B (145 nomes) — que nao e embarcado neste repo publico.

  python3 estrategia_propria.py
"""
import sys
from pathlib import Path

import pandas as pd

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
from _paths import SAIDAS

# ============================ PARAMETROS ============================
TOP_N       = 20        # long: 20 maiores momentum
BOTTOM_N    = 10        # short: 10 menores momentum
PESO_LONG   = 1.30      # soma da perna long = +130%
PESO_SHORT  = 0.30      # soma da perna short = -30% (financia o long extra)
CUSTO_ORDEM = 0.0020    # 20 bps por troca de peso
# CDI = 0: nao entra no book (decisao 2026-07-17: comparacao e relativa, nao vs CDI).


def book_130_30(precos, datas_sinal):
    """Regra E59 de referencia.

    precos       : painel de precos (datas x ativos), ja ajustado.
    datas_sinal  : datas de rebalance (ultimo pregao de cada semana).
    retorna      : serie de retorno liquido diario do book (sem CDI).
    """
    ret = precos.pct_change(fill_method=None)
    pesos = pd.DataFrame(index=precos.index, columns=precos.columns, dtype=float)
    for t in datas_sinal:
        janela = precos.loc[:t]
        ref = janela.asof(t - pd.DateOffset(months=1))      # preco de ~1 mes atras
        mom = (janela.iloc[-1] / ref - 1).dropna()          # momentum calendario 1m
        if len(mom) < TOP_N + BOTTOM_N:
            continue
        linha = pd.Series(0.0, index=precos.columns)
        linha[mom.nlargest(TOP_N).index] = PESO_LONG / TOP_N        # +6,5% por nome
        linha[mom.nsmallest(BOTTOM_N).index] = -PESO_SHORT / BOTTOM_N  # -3% por nome
        pesos.loc[t] = linha
    pesos = pesos.ffill().fillna(0.0)                       # segura os pesos ate o proximo sinal
    pesos_exec = pesos.shift(1).fillna(0.0)                 # sinal em t paga em t+1
    custo = pesos_exec.diff().abs().sum(axis=1) * CUSTO_ORDEM
    retorno_bruto = (pesos_exec * ret).sum(axis=1)          # long - short; sem CDI
    return retorno_bruto - custo


def metricas(ret):
    """Retorno total, Sharpe (vs zero, anualizado) e pior drawdown."""
    eq = (1 + ret).cumprod()
    sharpe = ret.mean() / ret.std(ddof=1) * (252 ** 0.5)
    maxdd = (eq / eq.cummax() - 1).min()
    return eq.iloc[-1] - 1, sharpe, maxdd


if __name__ == "__main__":
    serie = SAIDAS / "estrategia_propria_diario.csv"
    assert serie.exists(), f"Falta {serie} (export do motor E59 do lab)"
    ep = pd.read_csv(serie, parse_dates=["dia"]).set_index("dia")
    ret_total, sharpe, maxdd = metricas(ep["retorno_liquido"])

    print("=" * 72)
    print("Estrategia-propria | book E59 | 130/30 classico | SEM CDI")
    print("=" * 72)
    print(f"janela {ep.index.min().date()} -> {ep.index.max().date()} | dias {len(ep)}")
    print(f"retorno liquido {ret_total:+.2%} | Sharpe {sharpe:.2f} | MaxDD {maxdd:.2%}")
    print(f"exposicao long {ep['exposicao_long'].mean():.2f} | "
          f"short {ep['exposicao_short'].mean():.2f} | "
          f"caixa {ep['caixa_cdi'].mean():.2f} | CDI no book: NAO")
    print("numeros canonicos: motor do lab, ramo E59 (contrib_cdi = 0)")
    print("=" * 72)
