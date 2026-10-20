# Replica E1 v2 — Fabrizio, Mac Apple Silicon M4 CPU

**Provenienza:** archivio `replica_e1_fabrizio.zip` e resoconto `resoconto_replica_e1_fabrizio.md` forniti il 20 ottobre 2026. CSV e log copiati byte-for-byte dall'archivio; SHA-256 in `source_sha256.json`.

- Host: macOS ARM64 Apple M4, CPU, TensorFlow GPU `[]`; Python 3.11.17, NumPy 1.26.4, TensorFlow 2.15.1, PyTorch 2.4.0.
- Versione codice riportata: branch `ricky`, commit `59f556c`; submodule upstream `a880e332f556fc71faf8d3753931005d5d019339`. Il confronto esatto del runner con commit Ubuntu `f5bf86b` **non è stato ancora verificato**.
- SHA-256 pesi: `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.
- SHA-256 split: `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.
- Dati primari allegati: `summary.csv` (32 righe) e `metrics_per_run.csv` (320 righe), `e1_v2_test.log`; presenti 40 combinazioni (repeat,X) per `stage=validation` e per `stage=test`, e 10 run per ogni aggregazione.
- Tutte le medie di accuracy, AUROC, AUPRC, F1, FPR sono state ricomputate dai record e corrispondono al summary entro tolleranza numerica.
- Smoke e standalone validation 40/40 dichiarati da Fabrizio. Il CSV standalone validation, `run_config.json` e manifest per-payload **non fanno parte di questo allegato**; non descriverli come verificati dai raw consegnati.
- Test accuracies calcolate con soglia Youden ricavata sulla validation del rispettivo fit.
- Durata test riferita: circa 100-110 sec per fit; nessun OOM; `caffeinate` contro sleep.
- **Avvertenza:** differenza hardware ≠ cross-architecture neural OOD; risultato qualitativo E1 in-distribution replicato, senza inferenza statistica di equivalenza.
