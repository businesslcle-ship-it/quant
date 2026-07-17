# Pseudocódigo — estrategia-propria (entrada legada)

> **Atualização 2026-07-17:** a série pública `dados/estrategia_propria_diario.csv` é a base **E54** (1m semanal), não mais E48.

Documentação canônica da base atual:

- [base_amostra_e54.md](base_amostra_e54.md) — contrato + pseudocódigo + números
- [schema_labels_e55.md](schema_labels_e55.md) — labels (sem treino)
- [../LINHA_RACIOCINIO.md](../LINHA_RACIOCINIO.md) — por que essas escolhas

## Histórico (lab, não norte)

| Versão | Papel |
|---|---|
| E45 | single 365d mensal — arquivo |
| E48 | combo {3,6,9,12}m — **desvio de portfólio**; Sharpe 1,31 histórico |
| E54 | **base atual** de amostra ML |

Pseudocódigo E48 (arquivo):

```text
# NÃO é a base do CSV público atual
score = média dos percentis mom em {3,6,9,12}m
Top20 / Bottom10 / CDI+30 como E45
```
