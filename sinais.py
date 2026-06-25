import pandas as pd, numpy as np
A, N = 0.20, 252
LOOKBACKS = [126, 189, 252, 315]
ATIVOS = ["PRIO3", "ITUB3", "ABEV3"]

px = pd.concat({a: pd.read_csv(f"dados/{a}.csv", parse_dates=["date"]).set_index("date")["adjustedClose"]
                for a in ATIVOS}, axis=1, sort=True).loc["2008":]
ret = px.pct_change()

def pesos(L):                                              # alocação para UM lookback
    rank = px.pct_change(L).rank(axis=1)
    best = rank.eq(rank.max(axis=1), axis=0).astype(float); best = best.div(best.sum(axis=1), axis=0)
    vol = (best * ret.rolling(20).std() * N**.5).sum(axis=1)
    return best.mul((A / vol.replace(0, np.nan)).clip(0, 1), axis=0).fillna(0)

w = sum(pesos(L) for L in LOOKBACKS) / len(LOOKBACKS)      # alocação final (média dos 4 lookbacks)
mom = px.pct_change(252)                                   # momentum 12m (referência)
lider = mom.dropna(how="all").idxmax(axis=1)               # ativo mais forte do dia (ignora início sem dados)

# exporta um CSV por ativo: preço, momentum 12m, e o peso alocado (o sinal da estratégia)
for a in ATIVOS:
    out = pd.DataFrame({"adjustedClose": px[a], "momentum_12m": mom[a], "peso": w[a], "lider_do_dia": lider}).dropna(subset=["peso"])
    out.to_csv(f"sinais_{a}.csv")
    print(f"sinais_{a}.csv  ({len(out)} linhas)  | peso hoje: {w[a].iloc[-1]:.0%}")
