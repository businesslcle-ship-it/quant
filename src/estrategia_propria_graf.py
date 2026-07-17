"""
Estratégia-própria — gráficos (mesmo estilo do restante do repo).

Gera:
  figures/horizontes_path_b.png
  figures/estrategia_propria.png   (patrimônio + drawdown da série publicada)

  python3 estrategia_propria_graf.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
from _paths import DADOS, FIGS

FIGS.mkdir(exist_ok=True)

# --- 1) Sensibilidade horizonte × frequência ---
h = pd.read_csv(DADOS / "comparativo_horizontes_filme.csv")
ordem = ["E51", "E50", "E49", "E52", "E53", "E54"]
h = h.set_index("experimento").loc[ordem].reset_index()
labels = [f"{r.horizonte}\n{r.frequencia}" for _, r in h.iterrows()]
cores = ["#8a8a85"] * 4 + ["#2a78d6", "#c0392b"]

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), facecolor="#fcfcfb")
ax = axes[0]
bars = ax.bar(labels, h["n_ordens"], color=cores, width=0.7)
ax.set_title("Ordens por horizonte e frequência", fontsize=12, weight="bold")
ax.set_ylabel("Ordens (20 bps cada)")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25)
for b, v in zip(bars, h["n_ordens"]):
    ax.text(b.get_x() + b.get_width() / 2, v + 150, f"{v:,}".replace(",", "."),
            ha="center", va="bottom", fontsize=8)

ax2 = axes[1]
ax2.bar(labels, h["retorno_liquido"] * 100, color=cores, width=0.7)
ax2.set_title("Retorno líquido acumulado", fontsize=12, weight="bold")
ax2.set_ylabel("Retorno (%)")
ax2.spines[["top", "right"]].set_visible(False)
ax2.grid(axis="y", alpha=0.25)
fig.suptitle("Estratégia-própria (Path B) — horizonte e frequência", fontsize=13, weight="bold", y=1.02)
fig.tight_layout()
fig.savefig(FIGS / "horizontes_path_b.png", dpi=130, bbox_inches="tight", facecolor="#fcfcfb")
print(f"fig {FIGS / 'horizontes_path_b.png'}")

# --- 2) Patrimônio + drawdown da série ---
ep = pd.read_csv(DADOS / "estrategia_propria_diario.csv", parse_dates=["dia"]).set_index("dia")
ret = ep["retorno_liquido"].dropna()
eq = (1 + ret).cumprod()
dd = eq / eq.cummax() - 1
if not (0.9 <= float(eq.iloc[0]) <= 1.1):
    raise AssertionError(f"equity deve começar ~1; veio {eq.iloc[0]:.3f}")

fig2, (ax_eq, ax_dd) = plt.subplots(
    2, 1, figsize=(12, 7), sharex=True, height_ratios=[2, 1], facecolor="#fcfcfb"
)
fig2.suptitle(
    "Estratégia-própria — Path B · mom 1m · semanal @20 bps",
    fontsize=13, weight="bold",
)
ax_eq.plot(eq.index, eq.values, color="#c0392b", lw=2, label="estratégia-própria")
ax_eq.set_yscale("log")
ax_eq.set_ylabel("patrimônio (log, base 1)")
ax_eq.legend(loc="upper left", frameon=False)
ax_eq.grid(alpha=0.25)
ax_eq.spines[["top", "right"]].set_visible(False)
ax_eq.annotate(
    f" {(eq.iloc[-1]-1)*100:+,.0f}%".replace(",", "."),
    xy=(eq.index[-1], eq.iloc[-1]), color="#c0392b", fontsize=11, weight="bold", va="center",
)
ax_dd.plot(dd.index, dd.values * 100, color="#c0392b", lw=1.4)
ax_dd.set_ylabel("drawdown (%)")
ax_dd.grid(alpha=0.25)
ax_dd.spines[["top", "right"]].set_visible(False)
fig2.tight_layout(rect=[0, 0, 1, 0.97])
fig2.savefig(FIGS / "estrategia_propria.png", dpi=130, facecolor="#fcfcfb")
print(f"fig {FIGS / 'estrategia_propria.png'}")
print(
    f"série {ret.index.min().date()}→{ret.index.max().date()} | "
    f"ret={eq.iloc[-1]-1:+.2%} | "
    f"Sharpe={ret.mean()/ret.std(ddof=1)*(252**0.5):.2f} | "
    f"MaxDD={dd.min():.2%}"
)
