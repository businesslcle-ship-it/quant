# Pseudocódigo — Dual Momentum fiel nos 60min (`src/dual_momentum.py`)

Cada item traduz uma linha do código para português, na ordem em que executa.

Núcleo do livro intacto (12 meses por **calendário**). Uma concessão: **histerese de 5%** na troca de líder.

## Parâmetros

- **26** — Custo: 20 bps por perna (trocar de ação = 2 pernas).
- **27** — Histerese: só troca de líder se o desafiante ganhar por mais de 5% de momentum.
- **28** — Um ano de pregão tem ~1.764 barras de 60min (252 dias × 7).
- **29–32** — Os três ativos e o CDI de cada ano (2016–2026).

## 1) Dados: as barras de 60 minutos

- **36–37** — Leio a base plana e fico só com as barras horárias (descarto a linha-resumo `'dia'`).
- **38–40** — Remonto o timestamp real (data + hora) e organizo os fechamentos por barra, uma coluna por ativo.
- **41** — Retorno de cada ativo, barra a barra.
- **42** — CDI convertido para taxa por barra horária.

## 2) As duas pernas do livro, pelo CALENDÁRIO

- **47–48** — Para cada barra, localizo a barra mais próxima de **365 dias corridos** atrás — 12 meses de calendário, nunca contagem de barras (contar barras estica o ano e perde Sharpe — E25). O primeiro ano fica sem sinal.
- **50–51** — Momentum (perna **RELATIVA**): preço de agora sobre o preço de 12 meses atrás, para cada ativo.
- **53–55** — Barreira (perna **ABSOLUTA**): o CDI acumulado entre as **mesmas** duas datas. O log transforma soma em produto (eficiência).

## 3) A regra do livro para UMA barra (`onde_ficar`)

- **61** — Líder: o ativo de maior momentum de 12 meses.
- **62–63** — ABSOLUTA: se nem o líder supera o CDI do período, vou para caixa (retorna `-1`).
- **64–65** — Se eu estava em caixa e agora posso investir, entro no líder.
- **66–67** — RELATIVA com histerese: só troco de ativo se o novo líder ganhar do que tenho por mais de 5%.
- **68** — Vantagem pequena demais: fico onde estou (a histerese amortece o ruído dos cruzamentos).

## 4) Passa barra a barra (a histerese exige memória)

- **71–75** — Começo em caixa; zero os contadores de trocas (de líder × do caixa) e de custo.
- **76–78** — Para cada barra: se ainda não há 12 meses de histórico, pulo.
- **79** — Pergunto à regra do livro onde ficar nesta barra.
- **80–86** — Se mudou de posição: conto as pernas (vender o antigo e/ou comprar o novo), somo o custo e classifico a troca — de líder (relativa) ou do caixa (absoluta).
- **89** — Assumo a nova posição.
- **90–91** — O sinal desta barra paga na **próxima**: retorno do ativo (ou CDI se em caixa), menos o custo — já líquido, sem look-ahead.

## 5) Resultados

- **94–95** — Monto a série e começo no primeiro retorno real (depois do aquecimento de 12 meses).
- **96–102** — Patrimônio, anos, Sharpe (anualizado pela raiz das ~1.764 barras), MaxDD, retorno total, custo/ano e posição de hoje.
- **105–108** — Sharpe em três blocos de ~3 anos — robustez no tempo.
- **110–115** — Imprimo cabeçalho, desempenho (régua **horária**), trocas por tipo, blocos e o baseline mensal para comparar.
