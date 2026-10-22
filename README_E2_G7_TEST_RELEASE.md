# E2 G7 release / paired test — Riccardo Ubuntu + Fabrizio Mac M4

Questo pacchetto **non modifica** `scripts/run_e2_paired_v0.py`, `docs/E2_PROTOCOL_FROZEN.md` né alcun risultato precedente. Prima commit/push degli script e del notice G7, poi ciascun utente fa `prepare_test_release.py` con la propria validation locale e lancia `bash scripts/e2_g7_run_test.sh` sul proprio OS.

- Validation Ubuntu: `$HOME/mlsec-local/runs/e2_validation_official_v1`
- Validation Mac: `$HOME/mlsec-local/runs/e2_validation_official_mac_m4_v1`
- Release JSON Ubuntu: `$HOME/mlsec-local/runs/e2_test_release_ubuntu_v1.json`
- Release JSON Mac: `$HOME/mlsec-local/runs/e2_test_release_mac_m4_v1.json`
- Output test: `$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1` oppure `_mac_m4_v1`.
- Ogni processo salva 800 predizioni validation e 2.400 predizioni test (tre condizioni × 400 immagini × due metodi), 16 metriche e 803 payload manifest; dieci fit → 8.000 validation, 24.000 test, 160 metriche, 8.030 manifest.

Per Mac, usare l'ambiente Python E1 funzionante: lo script prova `$HOME/mlsec-local/venvs/modelxray/bin/python`, oppure impostare `E2_PY` prima del lancio. Testare la sintassi e il test locale prima di avviare il campione. Il launcher rifiuta di riusare un output/log già esistente; **non cancellarli e non ripetere selettivamente un fit**.

Per audit finale: `python_in_venv scripts/e2_g7_audit_test.py --test-dir <path>`.

Per report finale cross-platform: `python_in_venv scripts/e2_g7_compare_platforms.py --ubuntu <ubuntu-path> --mac <mac-path> --out-dir <new-empty-folder>` (se i due output non sono sullo stesso computer, importare solo i CSV e le verifiche di provenienza dopo gli audit locali; non condividere pesi originali o dati STL10).
