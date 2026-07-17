# Pseudocódigo — schema de labels E55 (base E54)

**Não é treino de metalabel.** Congela a unidade decisão→desfecho para o trabalho **junto com o Guilherme**.

## Schema

| Campo | Definição |
|---|---|
| Base | E54 (h=1m, semanal) |
| Unidade | `(ticker, data_sinal, lado)` — cada nome Top20 ou Bottom10 em `t` |
| Janela | pregões em `(t, t_próximo]` |
| y_seguir | `1` se a **perna** supera o CDI no intervalo; `0` senão |
| long | `ret_ativo > ret_cdi` |
| short | `(-ret_ativo) > ret_cdi` |
| Features inventário (≤ t) | momentum_1m, posição, passa_cdi_indiv, overlap Top20, n_elegível |

## Pseudocódigo

```text
sinais ← datas de rebalance E54 ordenadas
para cada t em sinais[0 .. −2]:
  t_prox ← próximo sinal
  ret_cdi ← produto(1+cdi) − 1 em (t, t_prox]
  para cada (ticker, lado) no ranking de t:
    ret_ativo ← produto(1+r_ativo) − 1 em (t, t_prox]
    se lado = long:  y ← 1 se ret_ativo > ret_cdi
    se lado = short: y ← 1 se (−ret_ativo) > ret_cdi
    gravar linha de label
```

## Números (stdout E55)

| Métrica | Valor |
|---|---|
| N labels | **15 522** |
| Taxa y=1 | **~49,6%** |
| Sinais com label | 518 |
| Train / test / holdout | 5 326 / 4 706 / 5 490 |
| vs E47 (book-level) | ~145× N bruto |

Arquivos: `dados/e55_schema_resumo.csv`, `dados/e55_schema_particoes.csv`.

## Declarações obrigatórias

- N bruto **≠** N independente (ticker × semanas vizinhas correlacionados).
- Schema pronto ≠ meta funciona.
- Treino/validação do meta = **sessão com Guilherme**.

## O que não fazer

- Não otimizar y pós-hoc.
- Não voltar a label no book inteiro (E47) como unidade principal desta linha.
- Não publicar o painel ticker-a-ticker completo neste repo (só resumos).
