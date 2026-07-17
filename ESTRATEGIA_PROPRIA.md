# Estratégia-própria

Momentum cross-sectional em universo amplo (Path B · 145 ações).

## Regra

| Item | Escolha |
|---|---|
| Sinal | Momentum de **1 mês** (calendário) |
| Frequência | **Semanal** (último pregão da semana) |
| Long | Top 20 · equal weight · +100% |
| Short | Bottom 10 · equal weight · −30% |
| Caixa | +30% CDI |
| Custo | 20 bps por ordem |
| Execução | Sinal em *t* → PnL a partir de *t+1* |

## Resultado (série exportada)

| Métrica | Valor |
|---|---|
| Retorno líquido | +152% |
| Sharpe | 0,56 |
| Max drawdown | −58% |
| Rebalances | 519 |
| Ordens | 12 480 |

Série: [`dados/estrategia_propria_diario.csv`](dados/estrategia_propria_diario.csv).

## Por que este desenho

Horizontes mais curtos produzem mais decisões no mesmo universo — o que importa quando o objetivo é estudar o **sinal** e, em seguida, aprender sobre essas decisões. A frequência semanal aumenta o número de rebalances em relação à mensal, mantendo o horizonte de 1 mês.

Sensibilidade horizonte × frequência:

![Horizontes](figures/horizontes_path_b.png)

## Painel de decisões

Cada nome no Top20/Bottom10, a cada sinal, gera um exemplo: a perna bateu o CDI até o próximo rebalance? **15 522** exemplos, ~50% positivos, partições temporais train/test/holdout.

Pseudocódigo da regra: [docs/pseudocodigo/base_amostra_e54.md](docs/pseudocodigo/base_amostra_e54.md)  
Pseudocódigo do painel: [docs/pseudocodigo/schema_labels_e55.md](docs/pseudocodigo/schema_labels_e55.md)  
Metodologia: [docs/metodologia_estrategia_propria.md](docs/metodologia_estrategia_propria.md)

## Limites (declarados)

Universo Path B ≠ as três ações da Rotação v2 / Dual Momentum. O short −30% é alocação de carteira; execução real de short exige borrow/locate (não modelados aqui). Survivorship do painel operacional está declarado no lab.
