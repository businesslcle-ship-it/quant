# Pseudocódigo — painel de decisões (em relabel)

A partir da estratégia-própria (rebalance semanal), cada posição é uma **decisão** — matéria-prima do metalabel, que decide **seguir ou ignorar** cada decisão do sinal.

## Unidade de decisão

| Campo | Valor |
|---|---|
| Unidade | ação × data do sinal × lado (long ou short) |
| Janela de desfecho | pregões entre o sinal e o próximo rebalance |
| Escala | ~519 sinais × 30 nomes (Top20 + Bottom10) |

## Rótulo — em definição (decisão 2026-07-17)

A régua antiga (`perna vs CDI`) foi **aposentada** junto com o CDI do book. O rótulo passa a ser **relativo** — uma perna contra a outra, não contra a taxa de juros. O eixo exato ainda está aberto:

```text
para cada sinal t com próximo sinal t':
  para cada ação no Top20 ou Bottom10 em t:
    ret_acao ← retorno composto em (t, t']
    y ← comparação RELATIVA (a definir):
        (i)  perna long vs perna short do mesmo sinal, ou
        (ii) ação vs mediana cross-section do próprio sinal, ou
        (iii) book long vs book short agregado
```

O painel rotulado antigo (base CDI) não é publicado aqui. O relabel relativo é a etapa seguinte, antes de qualquer treino de metalabel.

## Baseline do metalabel

O modelo só se justifica se bater **"sempre seguir"** (seguir todas as decisões) num **holdout temporal**, sem vazamento (features só com informação ≤ *t*). Exemplos vizinhos no tempo, na mesma ação, **não** são independentes — o N bruto superestima o N efetivo.
