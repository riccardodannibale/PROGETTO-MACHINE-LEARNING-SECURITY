# E2 — G3-C | Pilot di utilità su CNN originali (TRAIN-only)

**Data osservazione:** 22 ottobre 2026  
**Stato:** pilot esplorativo, NON risultato di detection OOD.  
**Fonte:** output terminale e contenuto dei file `utility_summary.csv` e `utility_per_model.csv` comunicati da Riccardo. I CSV originali devono essere archiviati dalla VM.

## Protocollo verificato

- Tre `row_index` del **TRAIN pool dei checkpoint**: `3`, `4`, `7`.
- CNN originali GHRP/STL10 ricostruite con nomi/forme dei layer identici allo `state_dict` originale.
- Dataset originale `tune_zoo_stl_small_uniform/dataset.pt`, SHA-256 `7afdccfe4d5418d3645e1a42f149c377cdc9088a9283cfd8288924c3a2e0b434`.
- Immagini preprocessate `(3,28,28)` in `[-1,1]`; valutazione sulle stesse **256 immagini** del `valset` dello zoo, campionate con seed `2026`.
- Attacco LSB **upstream X=23** e spread-spectrum sintetico v0 con **B=16**, `alpha=0.16/0.24`.
- Checkpoint del *detector* VAL/TEST **mai utilizzati** in questo pilot; `valset` delle immagini non è la validation dei checkpoint del detector.
- CNN valutate con `model.eval()`, no fine-tuning, no nuovi checkpoint scritti, payload solo inerti.

## Risultati medi

| Condizione | Accuracy media | Delta vs benign (punti percentuali) | Rel-L2 medio |
|---|---:|---:|---:|
| Benign | 37,2396% | — | 0,00% |
| X-LSB X=23 | 26,0417% | **−11,1979 pp** | 31,2191% |
| Spread α=0,16 | 35,6771% | **−1,5625 pp** | 16,0000% |
| Spread α=0,24 | 31,3802% | **−5,8594 pp** | 24,0000% |

Per `row_index` 3, 4, 7 sono stati riportati **0 errori di decodifica** sui rispettivi messaggi da 16 bit per entrambe le intensità spread. Il pilot iniziale su **20 checkpoint TRAIN** aveva invece recupero completo **19/20 a α=0,16** e **20/20 a α=0,24**. Questi risultati non sono contraddittori perché si riferiscono a campioni diversi.

### Osservazioni

- Le CNN modificate possono essere eseguite e il pilot rileva perdita di accuracy dopo gli attacchi.
- Su queste tre CNN X-LSB X=23 ha il peggior delta medio di accuracy; **non generalizzare** l'ordinamento alla popolazione del dataset.
- La capacità dei payload e l'entità della perturbazione **non sono appaiate** fra X-LSB e spread.
- **Non** usare questi tre modelli per scegliere nuovamente `alpha`, ottimizzare la metrica OOD o rivendicare che il payload sia stealth.
- Prima di citare numeri nel report finale, conservare `utility_summary.csv`, `utility_per_model.csv` e `audit_config.json`, e verificare che i riepiloghi siano ricostruibili dai per-model.

## Decisione metodologica

**G3-C superato come fattibilità, non come prova statistica di utility preservata.** Il protocollo E2 può procedere usando `alpha=0.24` (primario) e `alpha=0.16` (secondario predefinito), con limiti dichiarati. Eventuali studi estesi di utilità devono essere preregistrati come analisi distinta; non ritardano il confronto del detector.
