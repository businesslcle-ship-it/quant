# Pseudocódigo — estratégia-própria, book E59 (`src/estrategia_propria.py`)

Código à esquerda, explicação à direita — cada linha, na ordem em que executa.

Universo: Path B (145 ações). Sinal: momentum de **1 mês** (calendário). Rebalance: **semanal**. Book: **130/30 clássico, sem CDI** — o short de 30% financia os 30% a mais de long.

## Parâmetros — o contrato

| Linha | Código | O que faz |
|---|---|---|
| 30 | `TOP_N = 20` | Long: as **20** ações de maior momentum (Top20). |
| 31 | `BOTTOM_N = 10` | Short: as **10** de menor momentum (Bottom10). |
| 32 | `PESO_LONG = 1.30` | A perna long soma **+130%** → 6,5% por nome. |
| 33 | `PESO_SHORT = 0.30` | A perna short soma **−30%** → −3% por nome; é ela que **financia** o long extra. |
| 34 | `CUSTO_ORDEM = 0.0020` | **20 bps** cada vez que um peso muda. |
| 35 | `# sem CDI` | Caixa **0**; retorno é **long menos short** — ação vs ação. |

## A regra — `book_130_30`

| Linha | Código | O que faz |
|---|---|---|
| 46 | `retorno_diario = precos.pct_change()` | Retorno diário de cada ação: **matéria-prima** de tudo. |
| 49 | `pesos = pd.DataFrame(datas × ações)` | Tabela de pesos vazia, preenchida **só** nas datas de sinal. |
| 50 | `for t in datas_sinal:` | Para cada rebalance **t** (último pregão da semana). |
| 51 | `historia = precos.loc[:t]` | Recorto a história **até t** — sem espiar o futuro. |
| 52 | `preco_1m_atras = historia.asof(t − 1 mês)` | Busco o preço de **~1 mês** atrás. |
| 53 | `momentum = preco[t] / preco_1m_atras − 1` | **Quanto cada ação subiu** no mês. |
| 54–55 | `if len(momentum) < 30: continue` | Menos de 30 elegíveis (20+10)? **Pulo** a data. |
| 56 | `linha = pd.Series(0.0, ações)` | Monto a linha de pesos do dia, **toda em zero**. |
| 57 | `linha[20 maiores] = 1.30 / 20` | As 20 maiores recebem **+6,5%** cada. |
| 58 | `linha[10 menores] = −0.30 / 10` | As 10 menores recebem **−3%** cada. |
| 59 | `pesos.loc[t] = linha` | Gravo a carteira decidida na data **t**. |
| 61 | `pesos = pesos.ffill()` | **Seguro** os pesos até o próximo sinal (mantém a posição a semana toda). |
| 62 | `pesos_ontem = pesos.shift(1)` | Execução defasada: o peso de **t** só paga em **t+1** — sem look-ahead. |
| 64 | `custo = abs(Δpesos).sum() × 0.0020` | Custo do dia: variações absolutas dos pesos × **20 bps**. |
| 65 | `retorno_bruto = (pesos_ontem × ret).sum()` | Bruto: pesos de ontem × retornos de hoje — **long menos short, sem CDI**. |
| 66 | `return retorno_bruto − custo` | Retorno **líquido** = bruto − custo. |

## Métricas — a partir da série oficial do lab

| Linha | Código | O que faz |
|---|---|---|
| 72 | `serie = pd.read_csv(SAIDAS / "...diario.csv")` | Leio a série exportada do motor. **Não** recalculo o book aqui (os 145 nomes não vêm no repo público). |
| 76 | `patrimonio = (1 + retorno).cumprod()` | Curva de capital, base 1. |
| 77 | `retorno_total = patrimonio[-1] − 1` | Retorno acumulado → **+126%**. |
| 78 | `sharpe = média/desvio × √252` | Sharpe vs zero → **0,44** (secundário, não é o critério). |
| 79 | `max_drawdown = min(patrimonio/pico − 1)` | Pior queda do pico → **−71%**. |
| 82 | `print(resumo)` | **Única** saída: uma linha de resumo. O resto fica nas variáveis (explorer do Spyder). |

## Números (stdout de `python3 estrategia_propria.py`)

| Métrica | Valor |
|---|---|
| Retorno líquido | +126% |
| Sharpe (secundário) | 0,44 |
| Max drawdown | −71% |
| Rebalances / ordens | 519 / 12 480 |
| Exposição long / short / caixa | 1,30 / −0,30 / 0 |

## Limites

Short ilustrativo (sem borrow). Gross ≈ 160% → drawdown mais fundo é o preço honesto do 130/30. Path B ≠ universo de três ativos da Rotação v2; survivorship declarado.
