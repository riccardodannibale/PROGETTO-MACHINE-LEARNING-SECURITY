# E3 — Controlli su benigni appaiati e metadati: confronto Ubuntu / Mac M4

> Analisi retrospettiva di predizioni E2 già viste, NON secondo blind test indipendente.
> L’intensità e la capacità dei payload differiscono ancora: E3 non identifica causalmente la famiglia di attacco.

## Controlli strutturali

- Entrambe le piattaforme: 10 fit, 200 checkpoint appaiati per fit/condizione/metodo.
- Metadata-only majority baseline 50% per identità checkpoint.
- Score benigni e FPR costanti al variare di ID/OOD, a metodo e soglia congelati.

## Confronti medi sui 10 fit

| Metodo | Condizione | AUROC Ubuntu / Mac | Concordanza entro coppia Ubuntu / Mac | TPR Ubuntu / Mac | FPR Ubuntu / Mac |
|---|---|---:|---:|---:|---:|
| centroid | LSB_ID | 0.9043 / 0.9043 | 0.9265 / 0.9280 | 0.8135 / 0.8190 | 0.1820 / 0.1750 |
| centroid | SPREAD_0.24 | 0.4776 / 0.4745 | 0.4765 / 0.4800 | 0.1815 / 0.1785 | 0.1820 / 0.1750 |
| centroid | SPREAD_0.16 | 0.4947 / 0.4910 | 0.5030 / 0.4970 | 0.1740 / 0.1695 | 0.1820 / 0.1750 |
| nn | LSB_ID | 0.8202 / 0.8167 | 0.8470 / 0.8500 | 0.7275 / 0.7190 | 0.2385 / 0.2390 |
| nn | SPREAD_0.24 | 0.4805 / 0.4809 | 0.4810 / 0.4830 | 0.2330 / 0.2430 | 0.2385 / 0.2390 |
| nn | SPREAD_0.16 | 0.4920 / 0.4891 | 0.4895 / 0.4935 | 0.2325 / 0.2315 | 0.2385 / 0.2390 |

Le 10 ripetizioni riutilizzano i medesimi 200 checkpoint test. Le statistiche sui fit sono descrittive, non 2000 unità indipendenti.

## Cosa E3 non dimostra

- Che tutte le informazioni spurie siano assenti: controlliamo gli identificatori e score benigni, non ogni possibile artefatto a livello di rappresentazione.
- Che lo shift di famiglia *da solo* causi il calo: il payload spread è da 16 bit e il relativo L2 differisce da X-LSB X=23.
- Che questo test costituisca un nuovo holdout esterno; la stessa zoo e test identity sono già state analizzate in E2.

