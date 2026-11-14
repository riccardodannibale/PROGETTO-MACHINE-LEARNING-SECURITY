# E1 platform comparison audit

Generated: 2026-10-20 (UTC).

## Inputs
- Ubuntu test metrics: `results/test/e1_uniform_v2/metrics_per_run.csv`.
- Mac M4 test metrics: `results/replicas/e1_mac_m4/metrics_per_run.csv`.
- Source-file hashes are recorded in the replication manifest and audit artifacts.

## Checks
- 320 metric records per platform: 160 validation and 160 test, covering 40 unique fits.
- Fits can be paired by X, repeat and fit seed, subject to source-code and training-identity audit.
- Test thresholds match the validation threshold from the same fit.
- Runtime values are deduplicated by (repeat, X); they are not 320 separate durations.

## Descriptive results
- X=23 centroid AUROC: Ubuntu 0.901863; Mac 0.904378; mean difference (Mac - Ubuntu) +0.002515.
- Mean timed test section across 40 fits: Ubuntu 217.124 s; Mac 104.412 s.
- Ratio of the timed-section means (Ubuntu / Mac): 2.079.

## Interpretation limits
- This is not an equivalence test, inferential confidence interval or causal CPU benchmark.
- `elapsed_sec` starts after train/validation image construction and excludes Python startup and CSV writing.
- Ubuntu ran in a virtual machine; operating system, virtualization, CPU, TensorFlow build and memory are confounded.
- No model training was performed during this audit and no original CSV values were changed.

## Supporting tables
- `paired_per_run.csv`: 40 X/repeat pairs and Mac-minus-Ubuntu differences.
- `metrics_by_x.csv`: differences and variation by X and metric.
- `timing_by_x.csv`: descriptive timing by X and platform.
