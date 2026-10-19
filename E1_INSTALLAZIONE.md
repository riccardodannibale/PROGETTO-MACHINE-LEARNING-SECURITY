# Come installare e verificare il dossier E1

Questo archivio contiene soltanto **nuovi documenti, uno script per figure, un workbook Excel e immagini**. Non modifica gli script E1 dei training, il submodule Model X-Ray né i CSV originali di test e validation.

## 1. Estrazione nella repository Ubuntu

Da Bash:

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
unzip -n ~/Scaricati/E1_documentazione_grafici_GitHub.zip -d .
```

L'opzione `-n` evita la sovrascrittura automatica dei file già esistenti.

## 2. Verifica dei grafici sui CSV autentici (prima del commit)

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
~/mlsec-local/venvs/modelxray/bin/python scripts/plot_e1_results.py
```

Lo script legge **solo** i CSV `results/validation/e1_uniform_v2/summary.csv` e `results/test/e1_uniform_v2/summary.csv`, confronta `stage` e `n_runs`, poi rigenera i quattro PNG in `results/figures/e1/`.

Se manca matplotlib: prima verifica che sia disponibile nel virtualenv; in caso contrario, chiedere conferma al gruppo prima di installare nuove dipendenze.

## 3. Controllo dei file

```bash
git status --short
ls -lh docs/PROJECT_OVERVIEW.md docs/E1_REPRODUCIBILITY.md exam/E1_REPORT.md
ls -lh results/figures/e1/
```

**Excel:** apri `results/figures/e1/E1_grafici.xlsx`. Il foglio `Grafici_E1` contiene 4 grafici Excel nativi, aggiornabili modificando i due fogli con i riepiloghi. L'Excel contiene soltanto valori **aggregati**; le 10 repliche per X restano negli archivi `metrics_per_run.csv` della repository.

## 4. Revisione e commit

Verifica contenuti, autori e licenze con Fabrizio; solo dopo:

```bash
git add E1_INSTALLAZIONE.md docs/PROJECT_OVERVIEW.md docs/E1_REPRODUCIBILITY.md \
        exam/README.md exam/E1_REPORT.md exam/E1_REPORT.docx \
        scripts/plot_e1_results.py results/figures/e1/
git diff --cached --stat
git commit -m "docs: document E1 protocol results and publish reproducible figures"
git push origin ricky
```

**Nota:** non è necessario aprire nuovamente il test o addestrare il Siamese. Nessun numero di E2 o E3 è stato inventato.

## 5. Ambito e provenienza

Il dossier è una **bozza tecnica per il progetto d'esame** ricostruita dai log, dalla roadmap di progetto e dalla struttura dichiarata della repository. Prima di usarlo come relazione ufficiale verificare tutte le cifre sui CSV, controllare con Fabrizio il registro dei contributi e integrare una bibliografia formale con il docente.
