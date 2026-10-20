# E1 — Audit descrittivo Ubuntu vs Mac M4

Generato (UTC): 2026-10-20T12:30:47Z

## Input (integrità)
- Ubuntu: `/home/admin1/PROGETTO-MACHINE-LEARNING-SECURITY/results/test/e1_uniform_v2/metrics_per_run.csv` — SHA-256 `e8bb51a024a9e5f033c35088b980ab46458c5cd329de64770a989f5c976970ef`
- Mac: `/home/admin1/PROGETTO-MACHINE-LEARNING-SECURITY/results/replicas/e1_mac_m4/metrics_per_run.csv` — SHA-256 `f8783ad49489396a3ee3c5f34a47c291ddc97aed0da2b693008240cb15d7f84f`

## Controlli
- 320 metriche/stage per piattaforma? **320 metriche totali**, 160 validation + 160 test per piattaforma (40 fit distinti).
- I fit sono abbinabili per X, repeat e fit_seed, subordinatamente all’audit del codice e degli ID di training.
- Soglie applicate al test uguali a quelle della validation dello stesso fit.
- I tempi sono deduplicati per (repeat,X); non 320 durate.

## Risultati descrittivi
- X=23 AUROC centroid: Ubuntu 0.901863; Mac 0.904377; differenza media abbinata (Mac−Ubuntu) +0.002515.
- `elapsed_sec` test, 40 fit: Ubuntu media 217.124s; Mac media 104.412s.
- Rapporto delle **medie del tratto cronometrato** Ubuntu/Mac: 2.079.

## Limiti di interpretazione
- Non test di equivalenza, non CI inferenziale e non misura causale della CPU.
- `elapsed_sec` inizia DOPO la costruzione delle immagini train/validation e NON include l’avvio Python o la scrittura dei CSV.
- Ubuntu è in una VM: OS, virtualizzazione, CPU, build TensorFlow e RAM sono fattori concomitanti.
- Nessun training eseguito; nessun valore dei CSV originali modificato.

## Tabelle generate
- `paired_per_run.csv`: 40 coppie X/repeat e delta Mac−Ubuntu.
- `metrics_by_x.csv`: differenze e variabilità per X e metrica.
- `timing_by_x.csv`: tempi descrittivi per X e piattaforma.
