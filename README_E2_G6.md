# E2 — G6 official LSB validation gate (22 ottobre 2026)

Three new **orchestration/QA scripts only**. The reviewed and committed runner `scripts/run_e2_paired_v0.py` **is not modified**. These scripts do not create an E2 test-approval file and do not run the OOD test.

1. Execute `scripts/e2_g6_freeze_protocol.py` to approve personally and create `docs/E2_PROTOCOL_FROZEN.md` (requires a clean tracked working tree and unchanged G4 document and runner).
2. Review the new Markdown freeze, stage it plus the three orchestration scripts, `git diff --cached --check`, commit and push. **Only then** start official validation.
3. Execute `bash scripts/e2_g6_run_validation.sh`. This starts ten **separate** Python processes in order and saves individual logs under `$HOME/mlsec-local/runs/e2_validation_official_v1_logs`.
4. Execute `python3 scripts/e2_g6_audit_validation.py --validation-dir "$HOME/mlsec-local/runs/e2_validation_official_v1"`.
5. Share audit plus summary; **do not** create test authorization or run `--stage test` until a separate review.

The G5 diagnostic directory is kept untouched. If a fit fails, do not delete or selectively rerun results before investigating. The frozen document intentionally does not contain its own Git commit hash: record that after committing in a separate ledger.
