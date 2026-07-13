# Pseudocódigo — Rotação Momentum v2 (`src/rotacao.py`)

Cada item traduz uma linha do código para português, na ordem em que executa.

Régua oficial: **20 bps por perna**. Warm-up honesto (E37): a história pré-2008 entra no lookback; as métricas só a partir de 2008.

## Parâmetros

- **23** — Custo oficial: 20 bps por perna (régua do lab / README).
- **24** — Custo tabela: 5 bps — só linha secundária de referência.
- **25** — Alvo de volatilidade: 20% ao ano (no portfólio).
- **26** — Janela de volatilidade: 20 dias.
- **27** — Quatro janelas de momentum: 126, 189, 252 e 315 dias.
- **28** — 252 dias úteis no ano.
- **29** — Três ativos: PRIO3, ITUB3 e ABEV3.
- **30–33** — CDI de cada ano, de 2008 a 2026.

## 1) Dados

- **37–39** — Abro o CSV de cada ativo, ponho a data como índice, pego o preço ajustado e junto os três numa tabela **com a história completa** (não corto antes do lookback).
- **40** — `precos` é essa série completa — o warm-up precisa do passado (E37).
- **41** — Retorno diário: preço de hoje sobre o de ontem, menos um.
- **42** — Para cada data, busco o CDI do ano correspondente.
- **43** — Converto o CDI anual em diário: `(1 + CDI)^(1/252) - 1`.
- **44** — `AVALIAR_DESDE = "2008"`: as métricas começam aqui; o cálculo do sinal usa o que existir antes.

## 2) Direção

- **47** — Defino a função que recebe uma janela `L`.
- **48** — Retorno dos últimos `L` dias de cada ativo.
- **49** — Ranqueio os três ativos em cada dia.
- **50** — Marco o ativo de maior ranking.
- **51** — Transformo a marcação em 1 ou 0.
- **52** — Divido pela soma do dia: o líder fica com 100%; em empate, os empatados dividem.
- **54** — Rodo a função nas quatro janelas e tiro a **média** dos pesos (quatro votos).

## 3) Tamanho

- **57** — Retorno diário da direção, com os pesos do dia anterior (`shift(1)`).
- **58** — Volatilidade dos últimos 20 dias dessa série, anualizada com raiz de 252.
- **59** — Divido o alvo de 20% pela volatilidade e limito entre 0 e 1 (sem alavancagem).
- **60** — Multiplico a direção por esse fator; onde não há dado, peso zero.

## 4) Ritmo

- **63** — Guardo os pesos da sexta-feira e repito esses pesos em todos os dias da semana seguinte.
- **64** — Soma dos pesos do dia = exposição.
- **65** — O que falta para 1 é o caixa.

## 5) Retorno

- **68** — Ganho investido: pesos de ontem × retornos de hoje, somados.
- **69** — Ganho do caixa: caixa de ontem × CDI diário.
- **70** — Giro: soma das variações absolutas dos pesos.
- **71** — Retorno da estratégia a **20 bps**; corto a série de avaliação em 2008.
- **72** — Mesma conta a **5 bps** (só referência).
- **73–75** — Alinho pesos, exposição e giro à janela de avaliação.

## 6) Resultados

- **78** — Patrimônio acumulado: produto de `(1 + retorno)`.
- **79** — Excesso sobre o CDI diário.
- **80** — Sharpe vs zero (mesma régua do buy & hold), anualizado.
- **81** — Sortino vs zero.
- **82** — Sharpe líquido do CDI.
- **83** — Pior drawdown.
- **84** — Sharpe a 5 bps (secundário).
- **86–94** — Imprimo título, período, Sharpes, Sortino, MaxDD, retorno, giro, exposição e alocação de hoje.
