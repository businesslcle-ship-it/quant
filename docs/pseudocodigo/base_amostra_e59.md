# Pseudocódigo — estratégia-própria, book E59 (`src/estrategia_propria.py`)

Cada item traduz uma linha do código de referência para português, na ordem em que executa.

Universo: Path B (145 ações). Sinal: momentum de **1 mês** (calendário). Rebalance: **semanal**. Book: **130/30 clássico, sem CDI** — o short de 30% financia os 30% a mais de long.

## Parâmetros

- **30** — Long: 20 maiores momentum (Top20).
- **31** — Short: 10 menores momentum (Bottom10).
- **32** — Soma da perna long = **+130%** → 6,5% por nome.
- **33** — Soma da perna short = **−30%** → −3% por nome; é o short que financia o long extra.
- **34** — Custo: 20 bps por troca de peso.
- **35** — Sem CDI: caixa 0 e o retorno é long menos short — ação vs ação.

## A regra (`book_130_30`, linhas 39–66)

- **46** — Retorno diário de cada ativo: matéria-prima de todo o resto.
- **49** — Tabela de pesos vazia (datas × ativos), preenchida só nas datas de sinal.
- **50** — Para cada data de rebalance *t* (último pregão da semana):
- **51** — Recorto a história até *t* (sem espiar o futuro).
- **52** — Busco o preço de **~1 mês** atrás (`asof` = último preço em ou antes da data).
- **53** — Momentum de cada ativo: preço em *t* ÷ preço de 1 mês atrás − 1.
- **54–55** — Se há menos de 30 nomes elegíveis (20 + 10), pulo a data.
- **56** — Monto a linha de pesos do dia, toda em zero.
- **57** — As 20 maiores recebem **+6,5%** cada.
- **58** — As 10 menores recebem **−3%** cada.
- **59** — Gravo a carteira decidida na data *t*.
- **61** — Seguro os pesos até o próximo sinal (`ffill`): a carteira mantém a posição a semana toda.
- **62** — Execução defasada: o peso de *t* só paga em *t+1* (`shift(1)`, sem look-ahead).
- **64** — Custo do dia: soma das variações absolutas dos pesos × 20 bps.
- **65** — Retorno bruto: pesos de ontem × retornos de hoje — **long menos short, sem CDI**.
- **66** — Retorno líquido = bruto − custo.

## Métricas (linhas 69–82, a partir da série do lab)

- **72–73** — Leio a série oficial exportada do motor (`dados/saidas/estrategia_propria_diario.csv`); **não** recalculo o book aqui (o painel dos 145 nomes não vem neste repo público).
- **75–79** — Patrimônio, retorno total, Sharpe vs zero (√252) e pior drawdown, guardados em **variáveis nomeadas** (aparecem no explorer do Spyder).
- **resumo** — uma única linha de print: ret / Sharpe / MaxDD / exposições. Sem prints de debug.

> Os números canônicos vêm do motor do lab (ramo E59, `contrib_cdi = 0`). `book_130_30` é a mesma lógica em forma mínima, para ler e entender o mecanismo.

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
