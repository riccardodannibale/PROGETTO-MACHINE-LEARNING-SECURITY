# E2 G7 — Pacchetto finale per la repository

Il pacchetto contiene il rapporto `docs/E2_G7_FINAL_RESULTS.md`, gli output CSV e tre grafici di confronto ID/OOD Ubuntu e Mac M4.

## Installazione (da Ubuntu, branch `ricky`)

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
unzip -n ~/Scaricati/E2_G7_FINAL_CLOSEOUT.zip -d .
```

## Controllo incrociato indipendente sulla directory Ubuntu originale

La copia Ubuntu del pacchetto è estratta dall'output testuale del terminale. Per rigenerare i grafici e le statistiche direttamente dalle cartelle ufficiali (preferibile per la tracciabilità), riutilizzare lo script già committato G7:

```bash
PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
"$PY" scripts/e2_g7_compare_platforms.py \
  --ubuntu "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1" \
  --mac "results/e2_final/mac_m4" \
  --out-dir "$HOME/mlsec-local/runs/e2_g7_cross_platform_local_verification"
```

Esaminare `e2_hardware_summary.csv` e `E2_G7_CROSS_PLATFORM_REPORT.md` nella nuova directory. Il comando non modifica il runner né il dataset e non esegue training.

## Commit selettivo

```bash
git add -- docs/E2_G7_FINAL_RESULTS.md results/e2_final README_E2_G7_FINAL_CLOSEOUT.md
git diff --cached --check
git diff --cached --stat
git commit -m "docs: finalize E2 paired ID OOD results and Mac M4 replication"
git push origin ricky
```

Non usare `git add .`, non pubblicare il dataset originale e non modificare più il protocollo frozen per migliorare retroattivamente le metriche. Nessuna necessità di rifare i fit.

## Provenienza e verificabilità

Lo ZIP Mac originale aveva tre CSV; `metrics_per_run.csv` è incluso per audit di tutte le medie Mac. La copia dei due CSV Ubuntu è ottenuta dal testo terminale fornito. I CSV raw delle predizioni G7 rimangono nelle directory dei due partecipanti e **non** sono inclusi.

Una replica scientifica più forte richiederebbe in una fase successiva altri zoo/checkpoint esterni, una valutazione d'utilità su più reti e confronti con intensità/capacità matched.
