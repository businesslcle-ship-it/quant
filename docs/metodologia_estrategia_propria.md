# Metodologia — estratégia-própria

Como chegamos à regra publicada (momentum 1 mês, rebalance semanal, Path B 145).

## Objetivo da linha

Construir um **sinal cross-sectional** com muitas decisões observáveis e desempenho apenas adequado após custo — base útil para estudar o sinal e, depois, para modelos que aprendem **sobre** essas decisões (seguir / reduzir / recusar). O foco não é maximizar Sharpe de uma carteira cosmética.

## Passos (um parâmetro por vez)

1. **Horizonte de momentum** — testamos 3, 6 e 12 meses; depois 2 e 1 mês. Horizontes curtos geram mais trocas; horizontes longos geram ranking mais estável.
2. **Escolha do horizonte** — 1 mês: maior densidade de decisões na frequência mensal, com retorno líquido ainda positivo após 20 bps.
3. **Frequência** — com horizonte fixo em 1 mês, passamos de mensal para **semanal**. Rebalances e ordens sobem de forma clara; o custo sobe e o retorno líquido cai, mas a série permanece positiva no total.
4. **Painel de decisões** — cada posição Top20/Bottom10 vira um exemplo rotulado (perna vs CDI até o próximo sinal), com partição temporal.

Números: `dados/comparativo_horizontes_filme.csv` e `dados/e55_schema_resumo.csv`.

## O que não entrou (ainda)

- Filtro ou peso por **volume** (há auditoria prévia de elegibilidade binária no short; não alterou o Bottom10 naquela amostra — desenho de posicionamento por liquidez continua pendente).
- Combinação de vários horizontes no mesmo score (evitada para manter o sinal interpretável).
- Modelo de metalabeling treinado neste repositório (etapa seguinte).
- **Volume:** auditoria A30 nos 15 570 slots E54 → **0** secos em 21d/365d; Spearman mom×liquidez ≈ 0. Corte binário não se justifica; próximo passo = peso ∝ liquidez **dentro** da cesta (mesmo N de nomes).

## Universo

Path B: 145 ações vivas com cobertura completa 2021–2022 no painel operacional. Survivorship declarado; não é o painel pontual com deslistadas.
