# Progetto Machine Learning Security — dossier d'esame

**Titolo di lavoro:** Beyond the X-Ray — rilevamento di embedding nei pesi delle reti neurali.  
**Periodo:** ottobre–dicembre 2026, progetto condiviso Riccardo–Fabrizio.

## Indice

1. [Contesto, threat model, obiettivi e struttura E1–E3](../docs/PROJECT_OVERVIEW.md)
2. [E1 — relazione tecnica completa in Markdown](E1_REPORT.md) / [versione Word](E1_REPORT.docx)
3. [E1 — riproducibilità e audit](../docs/E1_REPRODUCIBILITY.md)
4. [E1 — figure e workbook Excel](../results/figures/e1/)
5. [Dati validation E1](../results/validation/e1_uniform_v2/)
6. [Dati test E1](../results/test/e1_uniform_v2/)

## Avanzamento

| Esperimento | Stato | Evidenza |
|---|---|---|
| E1 | **Completato 19/10/2026** | 40/40 validation, 40/40 test, commit `d35f8f2` |
| E2 | Da svolgere | Nessun dato finale |
| E3 | Da svolgere (alcuni controlli già in E1) | Nessun audit finale |

Le figure sono generate dai CSV del repository. La validazione esterna cross-zoo e la utility dei CNN sotto attacco non sono state misurate in E1.

## Replica Mac M4 integrata — 20 ottobre 2026

Il report E1 include ora il confronto fra i run di Riccardo su Ubuntu CPU x86_64 e di Fabrizio su Mac M4 CPU ARM64. La replica Mac si trova in `../results/replicas/e1_mac_m4/` e le figure cross-platform si rigenerano con `python scripts/plot_e1_comparison.py` dalla root. Questa è una replica dello stesso protocollo e stesso zoo: **non** è un test cross-architecture delle CNN e non sostituisce E2.
