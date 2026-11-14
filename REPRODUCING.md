# Reproducing and checking the experiments

This guide separates three activities: checking the published tables, auditing existing experiment outputs, and running the full experiments again. Passing the first check does not mean that model training has been repeated.

## 1. Verify the published results

From the repository root, run:

```bash
python3 scripts/verify_published_results.py
python3 tests/test_verify_published_results.py
```

The verifier uses only the Python standard library. It checks the published E2 paired AUROC tables, summary CSVs, cross-platform statistics and E3 aggregate controls. A successful run prints `PUBLISHED E2/E3 SUMMARY QA OK`.

This check does not train the Siamese detector, load original checkpoints, reconstruct AUROC from every raw prediction or independently repeat the source-host G6/G7/E3 audits.

## 2. Audit existing experiment outputs

The original experiment machines contain additional files that are not all included in the public repository. Where those files are available, audit scripts can check them without retraining the detector.

For an existing Ubuntu E2 test directory:

```bash
PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
"$PY" scripts/e2_g7_audit_test.py \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1"
```

To recompute E3 into a new directory, leaving the original output untouched:

```bash
"$PY" scripts/e3_matched_controls.py \
  --platform ubuntu \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1" \
  --split-csv manifests/e1_uniform_v1/splits.csv \
  --out-dir "$HOME/mlsec-local/runs/e3_controls_verification"
```

Use the validated Python environment and actual experiment directory on the Mac M4. Do not copy Ubuntu paths to another machine without checking them first. Always write verification output to a new directory.

## 3. Recreate the experiments

A full rerun needs more than a clean Git clone. It requires the original GHRP/STL10 checkpoint collection, extracted weights, the frozen split, the pinned upstream repository, compatible dependencies and the relevant validation/test inputs.

### Tested environment

The recorded Ubuntu setup uses Ubuntu 24.04 LTS and Python 3.11. The dependency list is stored in `configs/modelxray-ubuntu24-py311.lock.txt`.

The setup helpers are:

```bash
./scripts/setup_linux.sh
./scripts/check_setup.sh
```

Read [docs/setup.md](docs/setup.md) and inspect the scripts before running them. The setup helper creates its environment under `$HOME/mlsec-local/venvs/modelxray`; check that this path is suitable for your machine.

### Data and checkpoint requirements

The original model collection is not bundled with this repository. The expected extracted weight matrix has shape `(1000, 2864)`, dtype `float32`, and SHA-256:

```text
5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad
```

The frozen split file is `manifests/e1_uniform_v1/splits.csv`, with SHA-256:

```text
3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f
```

The Model X-Ray submodule is pinned to commit `a880e332f556fc71faf8d3753931005d5d019339`. Initialize and check it with:

```bash
git submodule update --init --recursive
git -C external/ModelXRay rev-parse HEAD
```

The source data and checkpoints must be obtained from their original location and used under the applicable terms. See [docs/data_and_licensing.md](docs/data_and_licensing.md).

### Experiment entry points

- **E1:** `scripts/run_e1_final_v2.py`, with matrix scripts `scripts/run_e1_v2_matrix.sh` and `scripts/run_e1_v2_test_matrix.sh`.
- **E2:** `scripts/run_e2_paired_v0.py`; validation and test audits use the `e2_g6_*` and `e2_g7_*` scripts.
- **E3:** `scripts/e3_matched_controls.py` and `scripts/e3_compare_controls.py`.

The historical E1/E2 execution workflow checks for branch `ricky`; full reruns should use the historical experiment branch and exact protocol revision described in the experiment notes. The `main` branch is the presentation and submission branch.

Do not bypass a failed integrity check, edit a frozen protocol to make a runner proceed, overwrite completed runs or re-open test identities to tune model choices. Any amended experiment must be treated as a new experiment with its own version and records.

## 4. Interpreting reproducibility

- Ten fits reuse the same 200 test checkpoint identities. They are repeated fits, not ten independent test datasets.
- The Mac M4 run is a replication on a different computing platform, not a new CNN architecture or external model zoo.
- Numerical agreement across Ubuntu and macOS does not imply bitwise-identical TensorFlow training.
- E3 is retrospective and reuses E2 test scores. It is not an independent blind holdout.
- The public repository contains published summaries and audit records, but not every raw prediction or original checkpoint.

For the scientific scope and limitations, see [report/final_report.pdf](report/final_report.pdf) and [docs/results_and_limitations.md](docs/results_and_limitations.md).
