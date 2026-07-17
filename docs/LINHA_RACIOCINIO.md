# Linha de raciocínio — sinal → ML (repo público)

> Espelho do lab (vault Quant). Objetivo: deixar **auditável** por que a base pública é E54 e o que **não** está neste repo.

## Norte (mentor Guilherme, 2026-07-16)

O Desafio **não** é maximizar Sharpe de carteira Top-N / 130/30 / combo de janelas.

O objetivo é gerar **alfa/sinal explorável por machine learning**:
1. **Muitas movimentações** (decisões filmadas — certas e erradas).
2. Base só **minimamente boa** (não precisa ser maravilhosa).
3. Julgar **interesse do sinal**, não cosmética de portfólio.
4. **Metalabeling** aprende sobre decisões da base — faremos **junto com o Guilherme**; este repo **não** treina o meta.

Analogia: não é ganhar o amistoso 8×0 com cinco toques; é gerar **muito filme** para um segundo juiz (ML) aprender.

## O que estava errado (confissão)

Lab + IA interpretaram mentoria como **otimização de portfólio** (E45/E48 Sharpe, combo 3/6/9/12m, comparativo cosmética). Isso foi rabbit hole. E48 permanece só como artefato histórico no lab — **não** é a base deste repo.

## Sequência causal (um knob por vez)

| Passo | O quê | Por quê | Evidência (stdout lab) |
|---|---|---|---|
| Horizontes longos | E49=3m → E50=6m → E51=12m | Um horizonte por vez; sem média | Trade-off filme↑ / IC↑ com h |
| Vizinhos curtos | E52=2m, E53=1m | 3m não era pico de filme | 1m=5381 ordens > 2m > 3m |
| Multi-critério | filme + alfa mínimo + interesse | Não eleger por Sharpe | Canvas/lab 2026-07-17 |
| Travar h | **1m** | Lexico: filme → alfa vivo → interesse | E53 passa; máximo filme mensal |
| Frequência | **E54 semanal** (W-FRI) | Multiplicar decisões com h fixo | 519 reb / 12480 ordens |
| Schema label | **E55** ativo×sinal×lado | Unidade certa p/ meta (≠ book E47) | N=15522; y≈50% |
| Meta-treino | **com Guilherme** | Pedido explícito do mentor | Fora deste repo |

## Por que E54 é a série em `dados/estrategia_propria_diario.csv`

- Horizonte **1m** + frequência **semanal** = mais filme da linha Path B auditada.
- Veículo de carteira (+100/−30/+30 CDI) = **mínimo** para gerar PnL e custo realistas — **não** o produto.
- Placar secundário: líquido +152%, Sharpe 0,56, custo 107%, DD −58%. Alfa mínimo **vivo** no total; frágil no stress 2020–22 — declarado, não escondido.
- Comparativo com v2/DM no gráfico alinha **calendário**, não universo (Path B 145 ≠ 3 ativos).

## Por que não E48 / não combo

Combo de janelas = juízes aninhados (mesma armadilha da v2 com 4 lookbacks). Promover por Sharpe = Goodhart. Norte ML exige **átomo de sinal** claro.

## Por que schema E55 e não meta no GitHub

- Schema congelado: `y=1` se perna long/short > CDI em `(t, t_próximo]`.
- N bruto 15 522 com partições temporais — `SCHEMA_PRONTO_PARA_META`.
- N bruto ≠ N independente (mesmo ticker em semanas vizinhas).
- Treino/validação do segundo juiz = sessão com o mentor.

## O que este repo **não** contém (de propósito)

- Motor Path B / listas de ranking diárias (lab privado).
- Painel ticker-a-ticker completo de labels (só resumos `e55_schema_*.csv`).
- Modelo meta treinado.
- Mortos / painel sem survivorship (buraco A2/A4 declarado no lab).

## Arquivos de evidência neste repo

| Arquivo | Conteúdo |
|---|---|
| `dados/estrategia_propria_diario.csv` | Série diária **E54** (base amostra) |
| `dados/comparativo_horizontes_filme.csv` | E49–E54: ordens, custo, ret, Sharpe secundário |
| `dados/e55_schema_resumo.csv` | N labels / taxas / partições |
| `dados/e55_schema_particoes.csv` | Contagens por partida × lado |
| `docs/AUDITORIA_EVIDENCIA.md` | Checklist do que bate com o lab |
| `docs/pseudocodigo/base_amostra_e54.md` | Pseudocódigo da base |
| `docs/pseudocodigo/schema_labels_e55.md` | Pseudocódigo do schema |

Última atualização pública desta linha: **2026-07-17**.
