# Integrazione E1: audit finale hardware (20 ottobre 2026)

Questo archivio **non** modifica i runner E1, i dataset né i CSV già versionati. Sovrascrive soltanto i report E1 e l'Excel preesistente, aggiunge nuovi documenti e figure, e colloca gli artefatti ricevuti da Fabrizio sotto `results/replicas/e1_mac_m4/audit/`.

Prerequisito: branch `ricky` con E1 già pubblicato al commit `59e0288` o successivo. **Verificare che `git status --short` non mostri modifiche personali importanti.** In caso contrario salvare o verificare le differenze, senza sovrascriverle. Utilizzare Bash (senza `>` prima di `git`).

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
git status --short
unzip -l ~/Scaricati/E1_AUDIT_FINALE_UBUNTU_MAC.zip
unzip -o ~/Scaricati/E1_AUDIT_FINALE_UBUNTU_MAC.zip -d .
~/mlsec-local/venvs/modelxray/bin/python scripts/verify_e1_mac_audit_artifacts.py
python3 scripts/audit_e1_platforms.py --out-dir results/analysis/e1_hardware
# l'audit genera 40 righe paired_per_run, altre tabelle e riepilogo, NON avvia training
git status --short
git diff --stat
git diff --check
```

Il codice di audit precedente può aver lasciato `scripts/audit_e1_platforms.py` e documenti preparatori non ancora tracciati: si può aggiungerli, ma verificare prima. Stage esplicito (non `git add .`):

```bash
git add docs/E1_HARDWARE_FINAL_AUDIT.md docs/E2_PROTOCOL_DRAFT.md docs/PROJECT_OVERVIEW.md docs/E1_REPRODUCIBILITY.md
git add exam/E1_REPORT.md exam/E1_REPORT.docx results/figures/e1/
git add results/replicas/e1_mac_m4/audit/ results/analysis/e1_hardware/
git add scripts/verify_e1_mac_audit_artifacts.py scripts/audit_e1_platforms.py
git add README_E1_AUDIT_FINALE.md
git diff --cached --stat
git diff --cached --check
# Se nulla di estraneo e nessun errore:
git commit -m "docs: finalize E1 hardware audit and cross-platform reproducibility"
git push origin ricky
git status -sb
```

Il `mac_environment.txt` è stato verificato per l'assenza di numeri di serie e credenziali nel materiale ricevuto, ma rileggere ogni artefatto prima di committarlo. Gli output `results/analysis/e1_hardware` includeranno riferimenti a percorsi locali: per una pubblicazione esterna al gruppo preferire percorsi relativi o anonimizzati. Non pubblicare binari di payload né checkpoint non licenziati.

Il file Excel mantiene le 9 figure precedenti, aggiunge 2 figure native e 2 fogli nuovi. Le 10 differenze paired di ogni X si possono leggere da `results/analysis/e1_hardware/paired_per_run.csv`; non presentare IC o inferenza su zoo esterni senza un'analisi aggiuntiva.
