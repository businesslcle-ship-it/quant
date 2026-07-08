# Quant Momentum — Rotacao v2

Estrategia sistematica de momentum cross-sectional com **volatility targeting** e rebalance semanal, aplicada a ITUB3, PRIO3 e ABEV3 (desde 2008). A cada dia o sistema mede o momentum dos tres ativos em quatro janelas (6, 9, 12 e 15 meses), aloca no mais forte, **dimensiona a posicao pela volatilidade do portfolio** (mira 20% ao ano) e congela os pesos por uma semana. O capital nao investido rende 100% do CDI. Long-only, sem alavancagem, liquido de custos, sem look-ahead (`shift(1)`).

A logica tem tres camadas independentes: **direcao** (em quem — a media dos lideres das quatro janelas), **tamanho** (quanto — o vol target, uma vez, no nivel do portfolio) e **ritmo** (quando — rebalance semanal).

## Resultados (janela dos 3 ativos, regua diaria, liquido de 20 bps)

| Estrategia | Sharpe | Vol | Max Drawdown | Retorno |
|---|---|---|---|---|
| **Rotacao v2 (freio)** | **1,56** | 22% | **-24%** | +2.403% |
| v2 sem freio | 1,09 | 50% | -79% | +6.207% |
| Dual Momentum (livro, baseline) | 1,03 | 50% | -79% | +4.727% |
| Buy & Hold 1/3 | 1,17 | 27% | -52% | +1.539% |

![Comparativo](comparativo.png)

**Leitura:** o vol target ("o freio") e o que separa a v2 do resto. Sem ele, a rotacao converge para o Dual Momentum classico (mesma vol de 50%, mesmo drawdown de -79%) — ou seja, o diferencial da v2 nao esta no sinal de direcao, e sim no **controle de risco**: terceiro do risco, metade do drawdown, e o melhor retorno ajustado a risco (Sharpe) do grupo. O Dual Momentum entrega mais retorno absoluto (concentra 100% no lider), mas ao custo de um drawdown de -79%.

![Rotacao v2](rotacao.png)

## Como rodar

```bash
pip install -r requirements.txt
python3 rotacao.py          # metricas da v2
python3 rotacao_graf.py     # v2 + grafico (3 paineis)
python3 dual_momentum.py    # baseline do livro (Antonacci)
python3 comparativo.py      # compara as 4 estrategias + grafico
python3 sinais.py           # exporta a alocacao diaria por ativo
```
Requer a pasta `dados/` com CSVs no formato `date,open,high,low,close,adjustedClose,volume`.

## Estrutura

| Arquivo | Conteudo |
|---|---|
| `rotacao.py` | Estrategia v2 (nucleo legivel, comentado) |
| `rotacao_graf.py` | v2 + grafico de 3 paineis |
| `dual_momentum.py` | Dual Momentum fiel ao livro (baseline de comparacao) |
| `comparativo.py` | Comparativo das 4 estrategias + grafico |
| `sinais.py` | Exporta a alocacao diaria por ativo |
| `Pseudocodigo_v2.docx` | Pseudocodigo da v2 (linha a linha) |
| `Pseudocodigo_DualMomentum.docx` | Pseudocodigo do Dual Momentum (linha a linha) |
| `dados/` | Precos ajustados dos 3 ativos |

Stack: Python, pandas, numpy, matplotlib.
