# Auditoria de evidência — o que o repo público prova

Checklist para o mentor / leitor: cada claim abaixo aponta para **arquivo** e **número**. Se não bater, o repo está desatualizado.

## 1. Norte

| Claim | Onde |
|---|---|
| Objetivo = sinal/ML, não Sharpe de carteira | [LINHA_RACIOCINIO.md](LINHA_RACIOCINIO.md), README § Path B |
| Meta-treino **com Guilherme**, não neste repo | `dados/e55_schema_resumo.csv` campo `meta_treino` |

## 2. Base de amostra = E54

| Claim | Evidência |
|---|---|
| h=1m, freq semanal W-FRI, Path B 145, +100/−30/+30 CDI, 20 bps | [base_amostra_e54.md](pseudocodigo/base_amostra_e54.md) |
| Série diária exportada | `dados/estrategia_propria_diario.csv` |
| n_rebalances=519, n_ordens=12480, custo≈107%, ret≈+152%, Sharpe≈0,56 | `dados/comparativo_horizontes_filme.csv` linha E54 |
| vs E53 mensal: mais filme (5381→12480 ordens) | mesma tabela E53 vs E54 |

## 3. Por que 1m (não 3m / não 12m)

| Claim | Evidência |
|---|---|
| 1m gera mais ordens que 2m/3m na frequência mensal | tabela: E53 5381 > E52 4017 > E49 3354 |
| 12m ≈ E45 365d (quase-duplicata) — pouco filme novo | lab E51 overlap∩E45 99,4% (narrado na linha) |
| Escolha lexica: filme → alfa mínimo → interesse | LINHA_RACIOCINIO |

## 4. Schema de labels (E55) — sem modelo

| Claim | Evidência |
|---|---|
| Unidade = ticker × sinal × lado | [schema_labels_e55.md](pseudocodigo/schema_labels_e55.md) |
| N=15522, taxa y≈49,6% | `e55_schema_resumo.csv` |
| Partições train/test/holdout todas >4000 | `e55_schema_particoes.csv` |
| Veredito lab SCHEMA_PRONTO_PARA_META | resumo CSV |
| E47 book-level N≈107 — unidade errada para esta linha | README / linha |

## 5. Comparativo gráfico v2 / DM / própria

| Claim | Evidência |
|---|---|
| Curva “estratégia-própria” = **E54**, não E48 | cabeçalho `src/comparativo.py` + CSV |
| Universo Path B ≠ 3 ativos | print AVISO no script + README |
| Sharpe na tabela do README é **secundário** | nota explícita |

## 6. Limites declarados (não esconder)

- Survivorship Path B (só vivos com cobertura 2021–22).
- Short −30% = alocação ilustrativa; sem borrow/locate.
- Custo E54 come o path (~107%); stress 2020–22 book negativo.
- N labels bruto ≠ N independente.
- Sem motor Path B no GitHub (só exports).

## Regenerar

No lab: rodar E54/E55 → reexportar CSVs → neste repo `python3 comparativo.py` → commit.

Data desta auditoria: **2026-07-17**.
