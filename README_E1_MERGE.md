# Pacchetto E1 unificato — Ubuntu e Mac M4

**Data:** 20 ottobre 2026. Pacchetto pronto per revisione e importazione nel branch `ricky` del progetto Machine Learning Security.

## Che cosa contiene

- `exam/E1_REPORT.md`: relazione metodologica completa E1 e nuova sezione 7 cross-platform;
- `exam/E1_REPORT.docx`: stessa relazione Word, con cinque grafici comparativi in appendice;
- `docs/PROJECT_OVERVIEW.md`, `docs/E1_REPRODUCIBILITY.md`: contesto E1/E2/E3 e audit aggiornato;
- `results/replicas/e1_mac_m4/`: **file originali** della replica di Fabrizio (CSV e log copiati senza alterazioni), SHA-256 dei file, manifest delle evidenze;
- `results/figures/e1/E1_grafici.xlsx`: workbook preesistente esteso (9 grafici Excel nativi totali), fogli `Mac_test`, `Mac_runs`, `Confronto_piattaforme`;
- `results/figures/e1/e1_platform_*.png`: 5 nuove figure ricostruibili dai CSV Ubuntu+Mac; comprende anche i precedenti PNG Ubuntu;
- `scripts/check_e1_replication.py` e `scripts/plot_e1_comparison.py`: audit e generazione PNG senza train;
- `E1_INSTALLAZIONE.md`, `exam/README.md`: note aggiornate per integrare il pacchetto.

**Non sono inclusi** i CSV Ubuntu `results/test/e1_uniform_v2/` e `results/validation/e1_uniform_v2/`: sono **già presenti su GitHub**, commit `d35f8f2` e precedenti. Non sostituirli con quelli Mac.

## Installazione sicura (Ubuntu, dalla root della repository)

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
git status --short                       # controllare modifiche locali
unzip -l ~/Scaricati/E1_merge_Ubuntu_Mac_M4.zip
unzip -o ~/Scaricati/E1_merge_Ubuntu_Mac_M4.zip -d .
python scripts/check_e1_replication.py
~/mlsec-local/venvs/modelxray/bin/python scripts/plot_e1_comparison.py
git status --short
git diff --stat
git add README_E1_MERGE.md E1_INSTALLAZIONE.md exam/ docs/ results/replicas/e1_mac_m4/ results/figures/e1/ scripts/check_e1_replication.py scripts/plot_e1_comparison.py
git diff --cached --stat
# Solo dopo revisione:
git commit -m "docs: merge E1 Ubuntu and Mac M4 replication with charts"
git push origin ricky
```

Lo ZIP aggiorna intenzionalmente la relazione e l'Excel della precedente versione E1. Non deve modificare gli script di training né il submodule upstream.

## Gerarchia delle evidenze

1. **Model X-Ray pubblicato/upstream:** punto di riferimento metodologico; **non** confronto quantitativo diretto con il nostro E1 (protocolli non allineati).
2. **Pilot E1 e validation v1:** risultati esplorativi, attacco inizialmente non riproducibile; non aggregarli al test finale.
3. **E1 v2 Ubuntu:** test finale 40/40, AUROC X23 centroid 0,901863.
4. **E1 v2 Mac M4:** test replicato 40/40, AUROC X23 centroid 0,904378.

L'hardware cambia (CPU x86_64 in VM vs CPU ARM64 M4), l'architettura CNN **no**. Le differenze di commit richiedono audit del codice prima di attribuire piccole oscillazioni al solo hardware.

## Prossima verifica consigliata (non blocca la chiusura E1)

Chiedere a Fabrizio il `run_config.json` Mac e il summary della validation stand-alone; verificare il diff del runner fra `f5bf86b` (Ubuntu test) e `59f556c` (Mac HEAD). E2/E3 rimangono esperimenti distinti.
