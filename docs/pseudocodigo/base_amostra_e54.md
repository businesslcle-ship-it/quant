# Pseudocódigo — estratégia-própria

Universo: Path B (145 ações).  
Sinal: momentum de **1 mês**. Rebalance: **semanal**.

## Contrato

- Em cada último pregão da semana *t*:
  - `mom = P(t) / P(ref) − 1`, com `ref` = último preço ≤ *t − 1 mês*.
  - Top 20 e Bottom 10 pelo ranking de `mom`.
- Carteira: **+100% Top20 EW**, **−30% Bottom10 EW**, **+30% CDI**.
- Execução: sinal *t* → retorno a partir de *t+1*; **20 bps** por ordem.

## Pseudocódigo

```text
para cada semana t (último pregão):
  para cada ativo i elegível:
    mom[i] ← retorno de calendário de 1 mês
  Top20 ← 20 maiores mom
  Bottom10 ← 10 menores mom
  pesos_alvo: +1/20 no Top20; −0,03 no Bottom10; CDI +0,30
pesos_executados(d) ← pesos_alvo(d−1)
retorno_liquido ← long − short + 0,30×CDI − custo
```

## Números (série publicada)

| Métrica | Valor |
|---|---|
| Retorno líquido | +152% |
| Sharpe | 0,56 |
| Max drawdown | −58% |
| Rebalances / ordens | 519 / 12 480 |

Série: `dados/estrategia_propria_diario.csv`.

## Limites

Short ilustrativo (sem borrow). Path B ≠ universo de três ativos da Rotação v2. Comparativos no README alinham calendário, não o painel.
