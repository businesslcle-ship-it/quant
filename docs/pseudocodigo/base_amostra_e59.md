# Pseudocódigo — estratégia-própria, book E59 (`src/estrategia_propria.py`)

Cada item traduz uma linha do código de referência para português, na ordem em que executa.

Universo: Path B (145 ações). Sinal: momentum de **1 mês** (calendário). Rebalance: **semanal**. Book: **130/30 clássico, sem CDI** — o short de 30% financia os 30% a mais de long.

## Parâmetros

- **29** — Long: 20 maiores momentum (Top20).
- **30** — Short: 10 menores momentum (Bottom10).
- **31** — Soma da perna long = **+130%** → 6,5% por nome.
- **32** — Soma da perna short = **−30%** → −3% por nome; é o short que financia o long extra.
- **33** — Custo: 20 bps por troca de peso.
- **34** — CDI = **0**: não entra no book (decisão 2026-07-17 — comparação relativa, ação vs ação, não vs CDI).

## A regra (`book_130_30`, linhas 37–60)

- **44** — Retorno diário de cada ativo: preço de hoje sobre o de ontem, menos um.
- **45** — Tabela de pesos vazia (datas × ativos), a preencher só nas datas de sinal.
- **46** — Para cada data de rebalance *t* (último pregão da semana):
- **47** — Recorto a história até *t* (sem espiar o futuro).
- **48** — Busco o preço de **~1 mês de calendário** atrás (`asof` = último preço em ou antes da data).
- **49** — Momentum de cada ativo: preço em *t* sobre esse preço de 1 mês atrás, menos um; descarto quem não tem série.
- **50–51** — Se não há pelo menos 30 nomes elegíveis (20 + 10), pulo esta data.
- **52** — Monto a linha de pesos do dia começando toda em zero.
- **53** — Os 20 maiores momentum recebem **+6,5%** cada.
- **54** — Os 10 menores recebem **−3%** cada.
- **55** — Gravo essa linha na tabela, na data *t*.
- **56** — Repito (ffill) os pesos entre um sinal e o próximo — a carteira **segura** a posição a semana toda; o que sobra fica em zero.
- **57** — Executo com defasagem: o peso decidido em *t* só paga a partir de *t+1* (`shift(1)`, sem look-ahead).
- **58** — Custo do dia: soma das variações absolutas dos pesos × 20 bps.
- **59** — Retorno bruto: pesos de ontem × retornos de hoje, somados — **long menos short, sem CDI**.
- **60** — Retorno líquido = bruto − custo.

## Métricas e saída (linhas 63–85)

- **65–67** — Patrimônio acumulado, Sharpe vs zero (anualizado por √252) e pior drawdown.
- **74–85** — O `__main__` lê a série publicada (`dados/saidas/estrategia_propria_diario.csv`, exportada do motor do lab) e imprime janela, retorno, Sharpe, MaxDD e exposições.

> **Reprodução completa:** `book_130_30` é a lógica em forma mínima; rodar de ponta a ponta exige um painel de preços do Path B (145 nomes), que não é embarcado neste repo público. Os números canônicos vêm do motor do lab (ramo E59, `contrib_cdi = 0`).

## Números (série publicada, stdout de `python3 estrategia_propria.py`)

| Métrica | Valor |
|---|---|
| Retorno líquido | +126% |
| Sharpe (secundário) | 0,44 |
| Max drawdown | −71% |
| Rebalances / ordens | 519 / 12 480 |
| Exposição long / short / caixa | 1,30 / −0,30 / 0 |

## Limites

Short ilustrativo (sem borrow). Gross ≈ 160% → drawdown mais fundo é o preço honesto do 130/30. Path B ≠ universo de três ativos da Rotação v2; survivorship declarado. Comparativos no README alinham calendário, não o painel.
