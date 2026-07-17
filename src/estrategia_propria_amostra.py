# -*- coding: utf-8 -*-
"""
Estratégia-própria — imprime métricas da série publicada e do painel de decisões.

  python3 estrategia_propria_amostra.py
"""
from pathlib import Path
import sys

import pandas as pd

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
from _paths import DADOS, ROOT  # noqa: E402

print("=" * 72)
print("Estratégia-própria · Path B · momentum 1m · rebalance semanal")
print("=" * 72)

serie = DADOS / "estrategia_propria_diario.csv"
horiz = DADOS / "comparativo_horizontes_filme.csv"
schema = DADOS / "e55_schema_resumo.csv"
part = DADOS / "e55_schema_particoes.csv"
for p in (serie, horiz, schema, part):
    assert p.exists(), f"Falta {p}"

ep = pd.read_csv(serie, parse_dates=["dia"]).set_index("dia")
ret = ep["retorno_liquido"]
eq = (1 + ret).cumprod()
sharpe = ret.mean() / ret.std(ddof=1) * (252 ** 0.5)
dd = (eq / eq.cummax() - 1).min()
print(f"\nSérie: {ret.index.min().date()} → {ret.index.max().date()}")
print(f"  dias={len(ret)} | retorno={eq.iloc[-1]-1:+.2%} | "
      f"Sharpe={sharpe:.2f} | MaxDD={dd:.2%}")

print("\nSensibilidade horizonte × frequência (ordens e retorno):")
h = pd.read_csv(horiz)
cols = ["experimento", "horizonte", "frequencia", "n_ordens", "n_rebalances",
        "retorno_liquido", "sharpe_zero_secundario"]
print(h[cols].to_string(index=False))

print("\nPainel de decisões:")
s = pd.read_csv(schema).iloc[0]
print(f"  exemplos={int(s['n_labels'])} | positivos={float(s['taxa_y1']):.1%}")
print(f"  train/test/holdout = "
      f"{int(s['n_train_ate_2019'])}/"
      f"{int(s['n_test_2020_2022'])}/"
      f"{int(s['n_holdout_desde_2023'])}")
print(pd.read_csv(part).to_string(index=False))

print(f"\nDocs: {ROOT / 'ESTRATEGIA_PROPRIA.md'}")
print("=" * 72)
