# Pseudocódigo — base de amostra E54 (estratégia-própria no repo)

Nome no gráfico/CSV: **estratégia-própria**.  
Papel real: **base de amostra para ML** (não “carteira vencedora”).  
Contrato lab: **E54** — horizonte momentum **1 mês**, rebalance **semanal (W-FRI)**.

Universo **distinto** da Rotação v2 / Dual Momentum (3 ativos): Path B 145.

## Por que esta base (motivo da escolha)

1. Norte mentor: muitas movimentações + alfa mínimo + sinal interessante.
2. Paisagem de horizontes (E49–E53): **1m** maximiza filme na frequência mensal.
3. Knob frequência: **semanal** multiplica rebalances (~4×) e ordens (~2× vs E53).
4. Combo E48 demovido (desvio de portfólio / janelas aninhadas).

Números (stdout lab E54): ver `dados/comparativo_horizontes_filme.csv`.

## Contrato

- Universo Path B 145 (cobertura 2021–22; survivorship declarado).
- Em cada **último pregão da semana** `t` (periodo `W-FRI`):
  - `mom_1m = P(t)/P(ref) − 1` com `ref` = último preço ≤ `t − 1` mês.
  - Ranking cross-sectional dos elegíveis.
- Carteira: **+100% Top20 EW**, **−30% Bottom10 EW**, **+30% CDI**.
- CDI +30% = parcela da alocação — **não** é borrow/locate.
- Execução: sinal `t` → PnL a partir de `t+1`; custo **20 bps/ordem**.

## Pseudocódigo

```text
para cada semana t (último pregão W-FRI):
  para cada ativo i com preço em t e ref ≤ t−1m:
    mom_1m[i] ← P(t)/P(ref) − 1
  Top20 ← 20 maiores mom_1m
  Bottom10 ← 10 menores mom_1m
  pesos_alvo: +1/20 nos Top20; −0,03 nos Bottom10; CDI +0,30
pesos_executados(d) ← pesos_alvo(d−1)
retorno_bruto ← long − short_subjacente + 0,30×cdi
retorno_liquido ← retorno_bruto − custo_20bps(ordens em d−1)
```

## Números (stdout E54)

| Métrica | Valor |
|---|---|
| Líquido / Sharpe* / MaxDD | +152% / 0,56 / −58% |
| Rebalances / ordens | 519 / 12 480 |
| Turnover / custo | 535x / 107% |
| Duração média entre sinais | ~7 dias |
| Overlap Top20 sinal-a-sinal | ~62% |

\*Sharpe = **secundário** (norte = filme/amostra).

## vs E53 (mesmo h=1m, mensal)

| | E53 mensal | E54 semanal |
|---|---|---|
| Ordens | 5 381 | **12 480** |
| Rebalances | 120 | **519** |
| Custo | 50% | **107%** |
| Ret líquido | +458% | +152% |

Leitura: frequência aumenta o filme; alfa mínimo fica mais frágil (custo) — declarado.

## Série no repo

`dados/estrategia_propria_diario.csv` — retorno líquido diário **E54**.

## Labels

Schema E55 (sem treino): [schema_labels_e55.md](schema_labels_e55.md).  
Meta-treino: **com o mentor**, não neste repositório.

## Limites

Não investível sem borrow real. Path B ≠ painel com mortos. Comparativo com v2/DM alinha calendário, não o universo.
