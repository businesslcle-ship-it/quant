# Pseudocódigo — painel de decisões

A partir da estratégia-própria (rebalance semanal), cada posição gera um exemplo para aprendizado supervisionado.

## Definição

| Campo | Valor |
|---|---|
| Unidade | ação × data do sinal × lado (long ou short) |
| Janela | pregões entre o sinal e o próximo rebalance |
| Rótulo positivo | a perna supera o CDI nessa janela |
| Long | retorno da ação > retorno do CDI |
| Short | −retorno da ação > retorno do CDI |

## Pseudocódigo

```text
para cada sinal t com próximo sinal t':
  ret_cdi ← CDI composto em (t, t']
  para cada ação no Top20 ou Bottom10 em t:
    ret_acao ← retorno composto em (t, t']
    se long:  y ← 1 se ret_acao > ret_cdi
    se short: y ← 1 se (−ret_acao) > ret_cdi
```

## Escala

| Métrica | Valor |
|---|---|
| Exemplos | 15 522 |
| Taxa de positivos | ~50% |
| Train / test / holdout | 5 326 / 4 706 / 5 490 |

Resumos: `dados/e55_schema_resumo.csv`, `dados/e55_schema_particoes.csv`.

Exemplos vizinhos no tempo (mesma ação) não são independentes — o N bruto superestima o N efetivo.
