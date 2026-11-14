# Reproducing and Auditing the Experiments (E1–E3)

## Scope: three distinct levels

This guide deliberately separates **verification of published numbers** from **auditing source-host artifacts** and **re-executing expensive experiments**. Passing the published-result verifier does not mean that training has been rerun. Reproducing a summary table does not imply that the complete dataset or checkpoint zoo can be redistributed.

## Level 0 — Verify published outputs without the dataset

From the repository root:

```bash
python3 scripts/verify_published_results.py
```

Only Python standard-library modules are required. The verifier checks:

- The 10 paired centroid AUROC rows per platform for ID, α=0.24, α=0.16, and signed deltas.
- Consistency with `results/e2_final/{ubuntu,mac_m4}/summary.csv`.
- Cross-platform paired-table means against the published summary.
- E3 10-fit group summaries on each platform where available, including balanced metadata and unchanged FPR across ID/OOD within a platform.

**Not checked at Level 0:** rescoring every raw prediction, TensorFlow model training, original checkpoint provenance, or model-utility evaluation. The original G6/G7/E3 QA tools cover additional checks on the source hosts.

For historical E1 figures, if the E1 dependencies and versioned CSV inputs are available:

```bash
"$HOME/mlsec-local/venvs/modelxray/bin/python" scripts/plot_e1_results.py
```

Check the E1 inputs and provenance notes in `docs/E1_REPRODUCIBILITY.md` before attempting a new run.

## Level 1 — Re-check available source-host artifacts

The original experiment hosts contain local raw-score paths that are not all distributed in the public repository. These commands audit existing outputs; they do **not** retrain the detector.

### Ubuntu: audit E2 test outputs

```bash
PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
"$PY" scripts/e2_g7_audit_test.py \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1"
```

### Ubuntu: recompute retrospective E3 controls

Choose a **new, non-existing output directory** so the original E3 artifacts are preserved:

```bash
"$PY" scripts/e3_matched_controls.py \
  --platform ubuntu \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1" \
  --split-csv manifests/e1_uniform_v1/splits.csv \
  --out-dir "$HOME/mlsec-local/runs/e3_controls_verification_2"
```

On the Mac M4, use that host's validated Python executable and actual E2 test directory, and set `--platform mac_m4`. Do not copy Ubuntu paths literally. Preserve the original E3 outputs.

## Level 2 — Full experiment recreation (data, compute, and protocol required)

### Branch and frozen-protocol constraint

The E1 test-matrix, E2, and E3 launch scripts historically verify that they run on Git branch `ricky`; the E2 runner also checks `docs/E2_PROTOCOL_FROZEN.md` against `HEAD`. These checks are part of the frozen experimental protocol and were intentionally left unchanged. To re-execute the historical experiment, use branch `ricky` or tag `experiments-e1-e2-e3-v1`, where available, rather than assuming that the documentation branch is a valid experiment branch. The `main` branch contains the same experiment code plus published results and the final report.

Never edit a frozen protocol or bypass a runner's integrity check to make a run proceed. Any protocol amendment must be documented as a new experiment, with its own provenance and integrity records.

### Environment

Use the **recorded pinned environment**, not an improvised modern `pip install` sequence. The historical Ubuntu environment used Python 3.11 under `$HOME/mlsec-local/venvs/modelxray/`; its dependency lock is `configs/modelxray-ubuntu24-py311.lock.txt`. The Mac M4 used a separately validated Apple Silicon environment.

The repository includes setup helpers. Inspect their contents and the setup note before running them:

```bash
sed -n '1,220p' docs/SETUP.md
sed -n '1,220p' scripts/setup_linux.sh
sed -n '1,220p' scripts/check_setup.sh
```

The setup helper historically creates the environment at `$HOME/mlsec-local/venvs/modelxray`. Confirm paths and prerequisites on the machine where you intend to run it.

### Dataset, checkpoints, weights, and split provenance

The source requirements are:

1. The original GHRP/STL10 model zoo and checkpoint weights, acquired from the original source and used in accordance with its distribution terms.
2. A provenance audit. `scripts/extract_d1_real_weights.py` creates `weights.npy` from **real checkpoint parameters**, not from `dataset.pt`. The latter is the preprocessed STL10 image/label dataset. Checkpoint deserialization uses restricted loading where supported.
3. `weights.npy` with shape `(1000, 2864)`, dtype `float32`, and SHA-256 `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.
4. The split file with SHA-256 `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.
5. `external/ModelXRay/` initialized as a Git submodule and pinned to commit `a880e332f556fc71faf8d3753931005d5d019339`. Confirm upstream licensing; do not copy its sources into the project's MIT-licensed tree.
6. The exact experiment runners: E1 `scripts/run_e1_final_v2.py`; E2 `scripts/run_e2_paired_v0.py`; E3 `scripts/e3_matched_controls.py`.

Useful setup and provenance scripts include `scripts/download_d1_stl10.sh`, `scripts/extract_d1_real_weights.py`, and `scripts/make_e1_frozen_splits.py`. Inspect the scripts and their `--help` output where supported before executing them. Do not invent paths or replace omitted artifacts with empty placeholders.

Initialize and verify the submodule:

```bash
git submodule update --init --recursive
git -C external/ModelXRay rev-parse HEAD
```

### Safe E2 preflight (does not reproduce AUROC)

The following command runs only the E2 preflight stage, using the historical Ubuntu environment and expected local weights path:

```bash
PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
"$PY" scripts/run_e2_paired_v0.py \
  --weights "$HOME/mlsec-local/datasets/ghrp_zoos/d1_uniform_real/weights.npy" \
  --split-dir manifests/e1_uniform_v1 \
  --out-dir "$HOME/mlsec-local/runs/e2_preflight_reproduction" \
  --stage preflight
```

This is **not a reproduction of the AUROC**. A full fit requires the historical frozen training protocol and separately gated test releases. Do not re-open previous test checkpoint identities after observing the results, and never select the best repeat.

### Experiment entry points

- **E1:** `scripts/run_e1_final_v2.py`, orchestrated by `scripts/run_e1_v2_matrix.sh` and `scripts/run_e1_v2_test_matrix.sh`.
- **E2:** `scripts/run_e2_paired_v0.py`; validation and test orchestration/auditing use `scripts/e2_g6_run_validation.sh`, `scripts/e2_g6_audit_validation_v2.py`, `scripts/e2_g7_prepare_test_release.py`, `scripts/e2_g7_run_test.sh`, and `scripts/e2_g7_audit_test.py`.
- **E3:** `scripts/e3_matched_controls.py` and `scripts/e3_compare_controls.py`.

The E1 test matrix uses an explicit test-unblinding gate. E2 test runs are subject to the frozen protocol, release JSON, and runner hash checks. Read the relevant protocol and release documents before launching anything. A clean clone alone does not supply local validation data, approval JSON, original weights, or raw predictions.

## Why results are not bit-for-bit identical across platforms

Python/NumPy seeds, source manifests, and payload generation are controlled. However, TensorFlow CPU kernels and different BLAS implementations can produce small differences in learned weights and AUROC on Ubuntu x86_64 versus Mac ARM64. The published cross-platform comparison tests **statistical/experimental reproducibility**, not binary identity.

## Dataset and security policy

- The experiments used synthetic, inert payloads. No executable malware was embedded, activated, or distributed.
- `dataset.pt` is the preprocessed STL10 images and labels; it is not the CNN parameter matrix.
- Never run `torch.load(..., weights_only=False)` on unknown checkpoint content.
- Do not publish the original downloaded zoo, large `.pt`/`.npy` checkpoints, or transient embedding payload bytes without checking permissions.
- Do not generalize claims from this synthetic experiment to real malware or all model architectures.

## Output interpretation and statistical scope

- AUROC is a ranking metric and is independent of the decision threshold.
- E3 Youden FPR/TPR/FNR values use thresholds calibrated on LSB validation and then held fixed for ID/OOD.
- Paired model samples share a source identity. The 10 fit repetitions reuse the same 200 test checkpoint identities. Account for this correlation; do not treat 2,000 repeated observations as 2,000 independent test models.
- E3 is a retrospective matched-control analysis of E2 test scores, not a fresh blind holdout.

## Related documentation

- [`docs/SETUP.md`](docs/SETUP.md) — environment setup.
- [`docs/EXPERIMENTAL_DESIGN.md`](docs/EXPERIMENTAL_DESIGN.md) — E1/E2/E3 design.
- [`docs/RESULTS_AND_LIMITATIONS.md`](docs/RESULTS_AND_LIMITATIONS.md) — results and limitations.
- [`docs/DATA_AND_LICENSES.md`](docs/DATA_AND_LICENSES.md) — data and third-party licensing.
- Frozen protocol/release records remain under `docs/` and must not be modified during documentation cleanup.
