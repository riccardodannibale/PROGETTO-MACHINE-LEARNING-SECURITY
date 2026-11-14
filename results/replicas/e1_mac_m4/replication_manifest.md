# E1 v2 replication — Fabrizio, Apple M4 CPU

**Source archive:** `replica_e1_fabrizio.zip` and the accompanying replication note supplied on 20 October 2026. CSV files and logs were copied from the archive; their SHA-256 values are listed in `source_sha256.json`.

- **Host:** macOS, Apple M4, ARM64, CPU; no TensorFlow GPU device detected.
- **Reported environment:** Python 3.11.17, NumPy 1.26.4, TensorFlow 2.15.1 and PyTorch 2.4.0.
- **Reported project revision:** branch `ricky`, commit `59f556c`.
- **Upstream Model X-Ray:** commit `a880e332f556fc71faf8d3753931005d5d019339`.
- **Weight matrix SHA-256:** `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.
- **Split file SHA-256:** `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.
- **Primary files:** `summary.csv` (32 rows), `metrics_per_run.csv` (320 rows) and `e1_v2_test.log`.

The 320 per-run records cover 40 (repeat, X) combinations for validation and 40 for test. Reported means for accuracy, AUROC, AUPRC, F1 and FPR were recomputed from the CSV and matched the summary within numerical tolerance.

The original note reports that validation and test each completed 40/40 fits. The standalone validation per-run logs were not included in the shared archive. The final Mac audit artifacts added separately to this repository include run configurations, a standalone validation summary and the 403-row payload manifest for repeat 0 at X=23; the manifest hashes were regenerated and matched.

The Mac operator reported an empty diff of the experiment files against the Ubuntu runner. The shared archive does not include the diff output itself, so this remains a reported check rather than an independently inspectable artifact.

Mean test runtime was reported as about 100–110 seconds per fit, with no out-of-memory failures. These timings are operational notes, not a controlled hardware benchmark. The platform comparison is not a test on a different CNN architecture and does not establish statistical equivalence.
