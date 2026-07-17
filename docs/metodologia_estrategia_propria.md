# Metodologia — estratégia-própria

Como chegamos à regra publicada (momentum 1 mês, rebalance semanal, Path B 145, book **E59** 130/30 sem CDI).

## Objetivo da linha

Construir um **sinal cross-sectional** com muitas decisões observáveis e desempenho apenas adequado após custo — base útil para estudar o sinal e, depois, para modelos que aprendem **sobre** essas decisões (seguir / reduzir / recusar). O foco não é maximizar Sharpe de uma carteira cosmética.

## Passos (um parâmetro por vez)

1. **Horizonte de momentum** — testados 3, 6 e 12 meses; depois 2 e 1 mês. Horizontes curtos geram mais trocas; horizontes longos geram ranking mais estável.
2. **Escolha do horizonte** — 1 mês: maior densidade de decisões, com o book ainda vivo após 20 bps.
3. **Frequência** — com horizonte fixo em 1 mês, de mensal para **semanal**. Rebalances e ordens sobem de forma clara; o custo sobe junto.
4. **Book** — o veículo passou por versões (100/−30 com CDI → sem CDI) até o **E59**: 130/30 clássico, long +130% financiado por short −30%, **sem CDI**. A comparação é relativa (ação vs ação), não contra a taxa de juros.
5. **Painel de decisões** — cada posição Top20/Bottom10 vira uma decisão rotulável. O rótulo relativo (uma perna vs a outra) está em definição; o painel base-CDI foi aposentado.

Filme por horizonte (densidade de decisões, neutro ao CDI): `dados/saidas/comparativo_horizontes_filme.csv` — coluna de decisão útil = `n_ordens` / `n_rebalances`.

## O que não entrou (ainda)

- Filtro ou peso por **volume/liquidez** — auditoria nos slots não achou nomes secos; a regra **não** usa filtro nem peso por liquidez (orientação do mentor: não mexer nisso).
- Combinação de vários horizontes no mesmo score (evitada para manter o sinal interpretável).
- **CDI no book** — removido de propósito (viés de juros BR); a régua é relativa.
- Modelo de **metalabeling** treinado neste repositório (etapa seguinte, sobre o painel relabelado).

## Universo

Path B: 145 ações vivas com cobertura completa 2021–2022 no painel operacional. Survivorship declarado; não é o painel pontual com deslistadas.
