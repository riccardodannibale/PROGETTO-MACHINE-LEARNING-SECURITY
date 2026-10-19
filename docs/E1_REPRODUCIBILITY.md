# E1 — riproducibilità, provenance e audit

**Ambito:** esperimento *E1 v2* — i risultati esplorativi `v1` sono mantenuti separati e non aggregati alle metriche `v2`.

## Provenance e valori congelati

| Voce | Valore o fonte |
|---|---|
| Codice upstream | Model X-Ray, commit `a880e332f556fc71faf8d3753931005d5d019339` |
| Commit progetto usato nella validation v2 | `e1bb618e28b709d046c1f75649e5b67db222f552` |
| Commit progetto usato nel test v2 | `f5bf86b237ca61f1d845732be41aa24203855921` |
| Commit pubblicazione risultati test | `d35f8f2` |
| SHA-256 `weights.npy` | `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad` |
| SHA-256 `splits.csv` | `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f` |
| Checkpoint | 1000 CNN, 2864 parametri float32 ciascuna |
| Partizioni | train pool 600 / validation 200 / test 200 |
| Seed principale | 42 |
| Numero ripetizioni | 10 per X |
| X-LSB | 1, 8, 16, 23 |
| Campioni training per replica | 3 coppie = 6 immagini derivanti da 3 checkpoint |
| Valutazione per partizione | 200 coppie = 400 immagini |
| Modalità | `ub`; immagine `gf` 100×100, modello `osl_siamese_cnn` |
| Payload | `sha256-keyed-uint8-pcg64-per-model-v1`, 16384 byte ciascuno |
| Metriche principali | AUROC centroid; secondarie accuracy, AUPRC, F1, FPR e 1-NN |

La tabella si riferisce al **protocollo v2**. I file `run_config.json` sono la fonte autoritativa per ogni campagna: fanno fede se emergono discrepanze nei nomi o nelle opzioni.

## Pipeline di un singolo run

1. Leggere `weights.npy` in mmap con `allow_pickle=False`; confrontarne SHA-256 e forma con `protocol.json`.
2. Leggere `splits.csv`; verificare assenza di checkpoint duplicati e split distinti per sorgente.
3. Per ripetizione `r`, scegliere 3 identità dal pool train usando `default_rng(42+r)`; per ogni livello X addestrare con `fit_seed = 42 + 1000*r + X`.
4. Generare per ogni riga checkpoint `i` byte pseudo-casuali sintetici deterministici dalla chiave SHA-256 **schema | 42 | r | X | i**, quindi scriverli temporaneamente in un `.bin`.
5. Applicare `img_pp_xlsb_attack` upstream allo stesso checkpoint benign con X=0, e alla versione stego con X attuale e file payload; rappresentare entrambi come immagini *gf* 100×100.
6. Addestrare `train_fsl(..., model_arch='osl_siamese_cnn', mode='ub')` sui 6 campioni di tre identità.
7. Generare score: differenza tra distanza alla classe benign e distanza alla classe stego (positivo = stego); verificare concordanza delle predizioni di riferimento upstream. Valutare centroid (primario) e nearest-neighbor (secondario).
8. Calcolare sulla validation AUROC, AUPRC e metriche di classificazione con soglia originale 0 e soglia Youden massimizzando TPR−FPR **sulla validation**.
9. Nella campagna finale riaddestrare il detector con le stesse impostazioni, ricalcolare la soglia sulla **validation della medesima nuova istanza**, applicarla al test; non scegliere parametri in base al test.
10. Scrivere per-run `metrics.json`, `payload_manifest.csv`, `predictions_validation.csv`, `predictions_test.csv` (solo test); aggregare `metrics_per_run.csv` e `summary.csv`.

### Distinguere le due validation

- `results/validation/e1_uniform_v2/`: validation sviluppata *prima* dell'unblinding del test, con 40 fit.
- Righe `stage=validation` in `results/test/e1_uniform_v2/`: nuova validation calcolata durante i fit del test, con 40 fit aggiuntivi. Non è un secondo test; serve a selezionare la soglia per ciascun fit test.
- Righe `stage=test` in `results/test/e1_uniform_v2/`: **test interno riservato**; riportare queste per la conclusione finale.

I pesi dei 40 modelli addestrati nella validation non sono stati salvati; per questo la campagna test ripete il training. Il protocollo con seed **non equivale alla garanzia di addestramento TensorFlow bitwise deterministico**. I payload, viceversa, sono rigenerabili dalla chiave e dalle versioni delle dipendenze.

## Guida rapida ai risultati senza rifare gli addestramenti

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
~/mlsec-local/venvs/modelxray/bin/python scripts/plot_e1_results.py
```

Il comando legge i **CSV versionati** già prodotti e rigenera quattro PNG in `results/figures/e1/`; non apre i checkpoint né richiede il training. Per una figura specifica, vedere `scripts/plot_e1_results.py`.

## QA e incidenti rilevanti nella storia dell'esperimento

| Fase | Osservazione | Azione/documentazione |
|---|---|---|
| Acquisizione dati | `dataset.pt` conteneva le immagini STL10; una prima estrazione di array immagini **non** rappresentava pesi. | Pipeline iniziale scartata; estratti 1000 **veri checkpoint** CNN con `extract_d1_real_weights.py` e manifest di provenance. |
| Pilota originale | Train/test few-shot upstream su stesso zoo; segnali forti soltanto per X=23. | Risultati trattati come esplorativi; successivo protocollo matched/split fissati. |
| Pilota paired | Esempi benign/stego della **stessa identità sorgente**, separati dalla validation. | Controllo di identità come principio del protocollo finale. |
| Validation `v1` | 40 run completati, ma payload casuali interni non riproducibili da `random.seed`/`np.random.seed`. | Preservata come campagna esplorativa; non aggregata a v2. |
| Correzione `v2` | Controllo A cover=True; B random non deterministico=False; C file payload=True; D attacco modifica=True. | Payload sintetici su file deterministici per checkpoint e manifest SHA-256. |
| Memoria VM | Python/TensorFlow ha subito un OOM in `v1` dopo 36 run consecutivi. | Matrix `v2` eseguita in **processi separati** con resume dei run completati. |
| Discordanza centroid | `v2`, repeat=8, X=1: 1 discordanza su 400 tra segno del margine e inferenza upstream, che ha causato STOP. | Eseguita diagnostica: nella ripetizione diagnostica 0/400 discordanti, centroidi NumPy/TF identici; una riesecuzione controllata dello stesso run ha prodotto risultati accettati. Non dimostrato che tutti i fit TensorFlow siano bitwise riproducibili. Il test non ha applicato retry selettivi sulla base delle performance. |
| Test | Preflight 40/40, Git pulito e commit del protocollo richiesti per sblocco; poi 40/40 run completati. | Metriche pubblicate nel commit `d35f8f2`. |

### Audit anti-leakage: implementato vs da fare

**Implementato in E1:** identità distinte, split manifestati con hash, coppie cover/stego appaiate, prevalenza di test 50%, calibrazione Youden **sulla validation**, test bloccato prima del freeze, nessuna selezione di X/metodi sulla base dei risultati test.

**Non ancora concluso:** test cross-architecture/cross-zoo; audit causale approfondito di precisione/serializzazione e altre scorciatoie; analisi utilità dei modelli attaccati, recovery di payload, stabilità bitwise dei training TF; statistiche inferenziali cluster-aware. Alcune prove esplorative precedenti hanno usato lo stesso zoo, quindi il test E1 non è un holdout esterno incontaminato in senso forte.

## File raw locali da conservare (non necessari a GitHub)

```text
~/mlsec-local/datasets/ghrp_zoos/d1_uniform_real/
  weights.npy
  checkpoint_manifest.csv
  extraction_summary.json
~/mlsec-local/runs/e1_v2_validation/repeat_XX_x_YY/
  metrics.json
  payload_manifest.csv
  predictions_validation.csv
~/mlsec-local/runs/e1_v2_test/repeat_XX_x_YY/
  metrics.json
  payload_manifest.csv
  predictions_validation.csv
  predictions_test.csv
~/mlsec-local/logs/e1_v2_validation.log
~/mlsec-local/logs/e1_v2_test.log
```

**Non inserire grandi checkpoint grezzi o payload binari nel repository** senza prima verificare necessità, licenze e policy. Gli script e le metriche versionate consentono comunque un audit sostanziale.

## Riferimenti

- GitHub upstream: https://github.com/danigil/ModelXRay
- Dataset zoo GHRP STL10: https://zenodo.org/records/6631784
- Roadmap originale del progetto d'esame, file del gruppo: `Roadmap_Progetto_Tesi_Paper_IEEE_con_Letture(7).docx`.
