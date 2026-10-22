# E3 — Controlli matched benign e metadati; nessun nuovo training

## Motivazione
La roadmap di progetto A4 definisce E3 come controllo con benigni appaiati e controlli metadati. E2 ha già il confronto ID/OOD: E3 deve verificare l'assenza di scorciatoie ovvie e chiarire l'origine dell'errore a soglia fissata, non inventare un nuovo attacco. Analisi retrospettiva, non blind.

## Riccardo — Ubuntu

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
unzip -n ~/Scaricati/E3_CONTROLS_STARTER.zip -d .
PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
"$PY" tests/test_e3_controls.py
"$PY" scripts/e3_matched_controls.py \
  --platform ubuntu \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1" \
  --split-csv manifests/e1_uniform_v1/splits.csv \
  --out-dir "$HOME/mlsec-local/runs/e3_controls_ubuntu_v1"
cat "$HOME/mlsec-local/runs/e3_controls_ubuntu_v1/e3_controls_summary.csv"
```

La directory `--out-dir` deve **non esistere**; non sovrascrivere output E2. Per caricare **il codice** su GitHub (non ancora i risultati):

```bash
git add -- README_E3_CONTROLS.md docs/E3_PROTOCOL_CONTROLS.md \
  scripts/e3_matched_controls.py scripts/e3_compare_controls.py \
  tests/test_e3_controls.py docs/E3_REPORT_SECTION_TEMPLATE.md
git diff --cached --check
git commit -m "feat: add read-only E3 matched benign and metadata controls"
git push origin ricky
```

## Fabrizio — Mac M4

Prima di eseguire, riceve lo ZIP o il nuovo commit e verifica che il suo branch possa aggiornarsi (`git status -sb`, `git pull --ff-only origin ricky`). Imposta `PY` sul venv E1 effettivamente usato. Poi:

```bash
"$PY" tests/test_e3_controls.py
"$PY" scripts/e3_matched_controls.py \
  --platform mac_m4 \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_mac_m4_v1" \
  --split-csv manifests/e1_uniform_v1/splits.csv \
  --out-dir "$HOME/mlsec-local/runs/e3_controls_mac_m4_v1"
cat "$HOME/mlsec-local/runs/e3_controls_mac_m4_v1/e3_controls_summary.csv"
```

Se il suo percorso E2 differisce, aggiornare solo `--test-dir`, senza cambiare il codice.

## Scambio file per confronto finale

Fabrizio crea ZIP con soli 3 output E3 e lo invia a Riccardo (o direttamente alla chat):

```bash
cd "$HOME/mlsec-local/runs/e3_controls_mac_m4_v1"
zip -j "$HOME/Desktop/E3_MAC_M4_CONTROLS.zip" \
  e3_controls_per_fit.csv e3_controls_summary.csv e3_source_manifest.json E3_CONTROLS_REPORT.md
```

Su Ubuntu estrarre lo ZIP Mac in una directory nuova, per esempio `results/e3_final/mac_m4_inputs/`, **solo se non contiene dati già esistenti**:

```bash
mkdir -p results/e3_final/mac_m4_inputs
unzip -n ~/Scaricati/E3_MAC_M4_CONTROLS.zip -d results/e3_final/mac_m4_inputs
"$PY" scripts/e3_compare_controls.py \
 --ubuntu "$HOME/mlsec-local/runs/e3_controls_ubuntu_v1" \
 --mac results/e3_final/mac_m4_inputs \
 --out-dir "$HOME/mlsec-local/runs/e3_cross_platform_v1"
```

**Prima** di pubblicare il report finale E3, verificare i due manifest SHA e gli output. Non pubblicare gli ZIP dei dataset/checkpoint o i payload originali.

## Come finisce il progetto
Dopo aver ottenuto gli output verificati su entrambi i computer: (1) scrivere la sezione E3 nell'`exam/PROJECT_REPORT.md` e nella versione Word mantenendo E1/E2; (2) un executive summary compatto per consegna e slide; (3) audit di README, licenze, environment, riproducibilità, titoli e contributi; (4) approvazione scope/docente e tag di rilascio quando appropriato. Non si promette paper entro dicembre.
