# Quant Research

Pesquisa quantitativa em ações brasileiras: duas linhas apresentadas neste repositório.

1. **Rotação Momentum v2** e **Dual Momentum** — universo de três ativos (ITUB3, PRIO3, ABEV3).  
2. **Estratégia-própria** — momentum cross-sectional em universo amplo (Path B, 145 ações), long/short com parcela em CDI.

Tudo líquido de **20 bps por ordem**, sem look-ahead (`shift(1)`), CDI diário do BCB no caixa.

---

## Estratégia-própria (universo amplo)

Cross-section de momentum no Path B (145 ações com histórico contínuo na janela operacional). A cada **semana**, o sistema:

- mede o momentum de **1 mês** (calendário) de cada ação elegível;
- compra equally-weighted o **Top 20**;
- vende equally-weighted o **Bottom 10** (exposição short −30%);
- mantém **+30% em CDI**;
- executa no pregão seguinte ao sinal; custo **20 bps** por ordem.

| Métrica | Valor |
|---|---|
| Universo | Path B · 145 ações |
| Sinal | Momentum 1 mês |
| Rebalance | Semanal |
| Carteira | +100% Top20 / −30% Bottom10 / +30% CDI |
| Ordens / rebalances | 12 480 / 519 |
| Retorno líquido* | +152% |
| Sharpe* | 0,56 |
| Max drawdown* | −58% |

\*Série diária exportada em `dados/estrategia_propria_diario.csv` (janela ~2016–2026). Números do comparativo alinhado no calendário abaixo.

**Por que 1 mês e frequência semanal.** Testamos horizontes de 1 a 12 meses (e 2 meses) com a mesma carteira. Horizontes mais curtos geram **mais decisões** — material mais rico para validar o sinal e, depois, para técnicas de aprendizado sobre essas decisões. A versão semanal multiplica rebalances em relação à mensal no mesmo horizonte de 1 mês. Detalhe e pseudocódigo: [docs/pseudocodigo/base_amostra_e54.md](docs/pseudocodigo/base_amostra_e54.md) · visão rápida: [ESTRATEGIA_PROPRIA.md](ESTRATEGIA_PROPRIA.md).

**Contagem de sinais (base publicada):**

| Objeto | N |
|---|---:|
| Sinais de carteira (rebalances semanais) | **519** |
| Decisões por nome (Top20+Bottom10 por sinal) | **15 570** |
| Ordens de execução (compra/venda @20 bps) | **12 480** |
| Exemplos rotulados (painel, com próximo sinal) | **15 522** |

![Patrimônio estratégia-própria](figures/estrategia_propria.png)

![Horizontes Path B](figures/horizontes_path_b.png)

**Liquidez (auditoria de volume).** Nos 15 570 slots da base, trailing de 21 e 365 dias: **0** nomes sem volume/financeiro. Momentum e liquidez quase não correlacionam (Spearman ≈ 0). Corte por volume seco **não** se justifica; o próximo passo natural é **peso proporcional à liquidez dentro da cesta** (mesmos 30 nomes). Resumo: `dados/a30_volume_resumo.csv`.

**Painel de decisões.** Cada posição do Top20/Bottom10 em cada sinal semanal vira um exemplo: a perna superou o CDI até o próximo rebalance? **15 522** exemplos (~50% positivos), partição temporal train / test / holdout. Schema: [docs/pseudocodigo/schema_labels_e55.md](docs/pseudocodigo/schema_labels_e55.md).

---

## Comparativo (mesma janela de calendário)

Régua diária, ativas @20 bps. **Atenção:** a estratégia-própria usa universo Path B; as demais usam só três ações. O gráfico alinha datas, não o painel.

| Estratégia | Universo | Sharpe | Vol | Max DD | Retorno |
|---|---|---|---|---|---|
| **Rotação v2 (com freio de vol)** | 3 ativos | **1,56** | 22% | **−24%** | +2.411% |
| v2 sem freio | 3 ativos | 1,09 | 50% | −79% | +6.207% |
| Dual Momentum mensal (livro) | 3 ativos | 1,03 | 50% | −79% | +4.731% |
| Buy & Hold 1/3 | 3 ativos | 1,17 | 27% | −52% | +1.539% |
| **Estratégia-própria** | Path B 145 | 0,56 | 21% | −58% | +152% |

![Comparativo](figures/comparativo.png)

---

## Rotação Momentum v2 (3 ativos)

Momentum cross-sectional com **volatility targeting** e rebalance semanal em ITUB3, PRIO3 e ABEV3. Três camadas: **direção** (média dos líderes em 6/9/12/15 meses), **tamanho** (vol alvo 20% a.a. no portfólio) e **ritmo** (pesos congelados por uma semana). Caixa rende CDI. Long-only, sem alavancagem.

**Amostra longa (`rotacao.py`, desde 2008, warm-up E37):** Sharpe **1,18** | MaxDD **−28%** | retorno +6.740%.

O freio de volatilidade é o que separa a v2 do Dual Momentum clássico no comparativo (vol ~22% vs ~50%). Não confundir o Sharpe 1,56 (janela ~2016+) com o 1,18 da amostra 2008+.

![Rotação v2](figures/rotacao.png)

### Sinais: v2 × Dual Momentum mensal

![Sinais comparados](figures/sinais_comparados.png)

---

## Dual Momentum (apresentado)

Núcleo do livro intacto (momentum **12 meses** + barreira CDI dos mesmos 12 meses), avaliado a cada barra de **60 minutos**, com histerese de **5%** na troca de líder.

| Versão | Sharpe | MaxDD | Retorno | Execução |
|---|---|---|---|---|
| **Dual Momentum** (`dual_momentum.py`, 60min) | **1,13** | −64% (horária) | **+4.931%** | 147 rebalances · 167 ordens |
| Dual Momentum mensal (baseline) | 1,04 | −65% mensal (−79% diária) | +3.858% | 18 meses com troca · 30 ordens |

![DM vs benchmark](figures/dm_vs_benchmark.png)

---

## Pseudocódigos

Narrativa em português para apresentação oral:

- [Rotação v2](docs/pseudocodigo/rotacao_v2.md)
- [Dual Momentum](docs/pseudocodigo/dual_momentum.md)
- [Estratégia-própria](docs/pseudocodigo/base_amostra_e54.md)
- [Painel de decisões (labels)](docs/pseudocodigo/schema_labels_e55.md)
- Índice: [docs/pseudocodigo/](docs/pseudocodigo/)

Metodologia (escolha de horizonte/frequência): [docs/metodologia_estrategia_propria.md](docs/metodologia_estrategia_propria.md).

---

## Como rodar

```bash
pip install -r requirements.txt
python3 rotacao.py
python3 dual_momentum.py
python3 dual_momentum_mensal.py
python3 comparativo.py                 # figures/comparativo.png
python3 estrategia_propria_graf.py     # figures/estrategia_propria.png + horizontes_path_b.png
python3 estrategia_propria_amostra.py  # métricas + contagem de sinais
python3 rotacao_graf.py                # figures/rotacao.png
python3 src/sinais_comparados.py
```

Requer `dados/` (preços dos 3 ativos, `base_plana.csv`, série da própria e tabelas auxiliares).

## Estrutura

```
├── README.md
├── ESTRATEGIA_PROPRIA.md
├── src/                 # código das estratégias apresentadas
├── dados/               # preços e séries exportadas
├── figures/             # gráficos do README
└── docs/pseudocodigo/   # narrativa linha a linha
```

Stack: Python, pandas, numpy, matplotlib.
