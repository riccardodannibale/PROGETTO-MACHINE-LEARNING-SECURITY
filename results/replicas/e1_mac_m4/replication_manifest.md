# E1 v2 replication — Fabrizio, Apple M4 CPU

This note records the provenance of the Mac M4 E1 replica. The original CSV exports and replication note were supplied on 20 October 2026. The retained files are:

- `summary.csv`: aggregate metrics;
- `metrics_per_run.csv`: per-fit metrics for validation and test;
- `source_sha256.json`: SHA-256 digests of the retained source exports and the original test log.

## Recorded environment and sources

- **Host:** macOS, Apple M4, ARM64, CPU; no TensorFlow GPU device detected.
- **Reported environment:** Python 3.11.17, NumPy 1.26.4, TensorFlow 2.15.1 and PyTorch 2.4.0.
- **Reported project revision:** branch `ricky`, commit `59f556c`.
- **Upstream Model X-Ray:** commit `a880e332f556fc71faf8d3753931005d5d019339`.
- **Weight matrix SHA-256:** `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.
- **Split file SHA-256:** `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.

## Audit summary

The per-run CSV contains 320 records covering the 40 (repeat, X) combinations across validation and test. Reported means for accuracy, AUROC, AUPRC, F1 and FPR were recomputed from the CSV and matched the summary within numerical tolerance. The original operator reported that validation and test each completed 40/40 fits and that the experiment files matched the Ubuntu runner.

The compact submission retains the summary, per-run metrics and source digests, but omits the original log and detailed machine-local audit bundle. Those omitted records are not required to read the final results; the provenance limits are described in the [complete report](../../../report/final_report.md).

Mean test runtime was reported as about 100–110 seconds per fit, with no out-of-memory failures. These timings are operational notes, not a controlled hardware benchmark. The platform comparison is not a test on a different CNN architecture and does not establish statistical equivalence.
