# E2 G6 — Diagnosi e audit per soglia Youden su macOS

**Data:** 22 ottobre 2026. **Stato:** correzione del *lettore CSV di audit*, non del runner.

## Perché

In E1 `validation_threshold` converte una soglia `roc_curve` in una decisione stretta `score > threshold` mediante `np.nextafter(candidate, -np.inf)`. A livello float64 la soglia può differire dallo score di un solo ULP. Il parser CSV predefinito di pandas non garantisce il round-trip esatto dei float64, pertanto la verifica `score > threshold` fatta *dopo* il caricamento del CSV può produrre un falso mismatch. `float_precision='round_trip'` è la corretta ricostruzione dai decimali scritti da pandas.

**Il risultato Mac non dimostra ancora questa causa.** Lo script `e2_g6_diagnose_threshold_csv.py` individua e mostra tutte le discrepanze, confrontando i due parser e la soglia JSON originale. Se rimane qualche mismatch con il parser round-trip, fermarsi: non sostituire il controllo con `np.isclose()`.

## Istruzioni (Ubuntu e Mac, già nella root repo)

1. `unzip -n ~/Scaricati/E2_G6_MAC_AUDIT_FIX.zip -d .`
2. Usare *il proprio Python del venv E1* (Mac percorso da adattare se diverso):
   ```bash
   PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
   "$PY" tests/test_e2_g6_csv_roundtrip.py
   "$PY" scripts/e2_g6_diagnose_threshold_csv.py --validation-dir "$HOME/mlsec-local/runs/e2_validation_official_mac_m4_v1"
   "$PY" scripts/e2_g6_audit_validation_v2.py --validation-dir "$HOME/mlsec-local/runs/e2_validation_official_mac_m4_v1"
   ```
   **Ubuntu:** sostituire `e2_validation_official_mac_m4_v1` con `e2_validation_official_v1`.

3. Attesi: `roundtrip_mismatches=0` a tutte le ripetizioni e `E2 G6 OFFICIAL VALIDATION QA OK` in v2. Se così non fosse: conservare CSV e JSON, non riaddestrare e non procedere al test.

## Integrità e freeze

- Non modificare `scripts/run_e2_paired_v0.py`, `run_e1_final_v2.py`, `docs/E2_PROTOCOL_FROZEN.md`, output ufficiali o threshold JSON. Il runner SHA è invariato.
- Conservare `scripts/e2_g6_audit_validation.py` originale e il suo hash, aggiungere *solo* diagnostica e audit v2 in nuovi file.
- Registrare sul branch `ricky` il presente audit amendment e i risultati della verifica. L'amendment è una modifica nel *controllo post-hoc degli artifact* e non nelle decisioni scientifiche preregistrate.
- La validation deve passare su entrambe le architetture prima di aprire il test. Non creare file di test approval se gli audit sono incompleti.
