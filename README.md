# Beyond the X-Ray

**Detecting steganographic modifications in neural network weights**  
Machine Learning Security project by Riccardo D'Annibale and Fabrizio Giuseppe Mazzilli.

This repository studies whether a few-shot detector inspired by Model X-Ray, trained on X-LSB modifications, transfers to a second family of synthetic weight modifications. The project combines an adapted upstream baseline, a project-specific keyed spread-spectrum prototype, identity-disjoint splits and retrospective matched controls.

## Main results

### E1 — X-LSB baseline

Centroid results on the held-out test set:

| X-LSB | Ubuntu AUROC | Ubuntu AUPRC | Mac M4 AUROC | Mac M4 AUPRC |
|---:|---:|---:|---:|---:|
| 1 | 0.500150 | 0.504064 | 0.500209 | 0.504417 |
| 8 | 0.508233 | 0.509345 | 0.509388 | 0.510389 |
| 16 | 0.501293 | 0.512234 | 0.501425 | 0.512511 |
| **23** | **0.901863** | **0.902063** | **0.904378** | **0.904875** |

At X=1, 8 and 16 the detector is near chance; X=23 is detected reliably in this checkpoint collection.

### E2 — ID/OOD transfer

Centroid results, mean over ten fits:

| Condition | Ubuntu AUROC | Ubuntu AUPRC | Mac M4 AUROC | Mac M4 AUPRC |
|---|---:|---:|---:|---:|
| ID: X-LSB X=23 | 0.904273 | 0.904619 | 0.904300 | 0.904341 |
| OOD: spread alpha=0.24 | 0.477620 | 0.492045 | 0.474500 | 0.488265 |
| OOD: spread alpha=0.16 | 0.494701 | 0.497873 | 0.491042 | 0.496086 |

AUPRC values are reported as the means available in the published summaries; AUPRC per-fit standard deviations are not included in those aggregates.

### E3 — matched controls

The TPR falls from about 81–82% on ID to about 18% on spread alpha=0.24. The unchanged benign scores and FPR are a structural control property: the benign scores are identical by construction and the validation threshold is held fixed. This is not independent evidence of general robustness.

## Scope and correct interpretation

The project reuses upstream Model X-Ray Siamese/X-LSB components but adapts the experimental protocol; it is not a bit-for-bit reproduction of the paper. The official 2026 paper's reported OOD transfer concerns MaleficNet. This project instead tests `e2-keyed-orthogonal-spread-v0-educational`, a custom educational spread-spectrum encoder, not the original MaleficNet pipeline. The E2 result therefore does not contradict the paper.

X-LSB parameter `X` counts modified mantissa bit positions; it is not directly comparable to the paper's embedding-rate percentages. X-LSB X=23 and spread alpha=0.16/0.24 are also not intensity- or capacity-matched, so E2 isolates neither family change nor embedding strength causally.

## Report

The complete Italian technical report, including theory, methods, all experiment interpretations, limitations, reproducibility and repository map, is maintained at:

- [report/final_report.md](report/final_report.md)

A PDF version is supplied separately as the submission report. The Markdown file is the canonical version tracked in Git.

## Quick verification

Clone the submission branch with its Model X-Ray submodule:

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY

python3 scripts/verify_published_results.py
python3 tests/test_verify_published_results.py
python3 tests/test_repository_layout.py
python3 tests/test_e2_g5_preflight.py
python3 tests/test_e2_g7_release_contract.py
```

These checks validate the published aggregate summaries, essential repository layout and E2 integrity gates. They do **not** retrain the detector or recompute all metrics from raw predictions. There is no active GitHub Actions workflow on the submission branch; run the checks manually.

## Full reproduction requirements

A full rerun requires the original GHRP/STL10 checkpoint collection, the extracted `weights.npy`, the pinned upstream submodule, the locked Python environment and local validation/test outputs. The repository does not include the original checkpoints or `weights.npy`.

The source data are available from [Zenodo record 6631784](https://zenodo.org/records/6631784). The extraction script creates a 1000 × 2864 `float32` matrix and a checkpoint manifest. Expected `weights.npy` SHA-256:

Prepare the environment and rebuild the matrix outside the Git repository:

```bash
./scripts/setup_linux.sh
./scripts/check_setup.sh
export MODELXRAY_GHRP_DIR="$HOME/mlsec-local/datasets/ghrp_zoos"
bash scripts/download_d1_stl10.sh --all
INPUT_ROOT="$(find "$MODELXRAY_GHRP_DIR" -type d -name tune_zoo_stl_small_uniform -print -quit)"
test -n "$INPUT_ROOT"
python3 scripts/extract_d1_real_weights.py \
  --input-root "$INPUT_ROOT" \
  --output-dir "$MODELXRAY_GHRP_DIR/d1_uniform_real" \
  --expected-models 1000
```


```text
5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad
```

For the frozen E1/E2 experiment runners, switch to the experimental branch `ricky` (head verified at `3ef84f73d994fc447b12bb99f265c203548480e4`). E1 test and E2 runners explicitly require that branch. The G6/G7 E2 wrappers additionally require the prescribed sequence of validation, audit and local test-release approval. Do not bypass their preflight or alter the frozen protocol. Several runner paths default to `$HOME/mlsec-local`.

E1 validation can then be reproduced using the same default local paths:

```bash
git switch ricky
export MODELXRAY_PYTHON="$HOME/mlsec-local/venvs/modelxray/bin/python"
export MODELXRAY_GHRP_DIR="$HOME/mlsec-local/datasets/ghrp_zoos"
export E1_V2_OUT_DIR="$HOME/mlsec-local/runs/e1_v2_validation"
bash scripts/run_e1_v2_matrix.sh
```

The E1 test wrapper requires a successful preflight and an explicit unblind confirmation; its validation and test directories are fixed under `$HOME/mlsec-local/runs/`:

```bash
bash scripts/run_e1_v2_test_matrix.sh --preflight
E1_TEST_UNBLIND_CONFIRM=UNBLIND_E1_V2_TEST bash scripts/run_e1_v2_test_matrix.sh --run
```

E2 has a separate, gated lifecycle: run `bash scripts/e2_g6_run_validation.sh`, audit the ten validation fits with `e2_g6_audit_validation_v2.py`, create the platform-specific local authorization using `e2_g7_prepare_test_release.py`, then run `bash scripts/e2_g7_run_test.sh` and audit with `e2_g7_audit_test.py`. For Ubuntu the standard validation/test/approval paths are under `$HOME/mlsec-local/runs/e2_validation_official_v1`, `e2_test_official_ubuntu_v1` and `e2_test_release_ubuntu_v1.json`. The Mac wrapper uses corresponding `mac_m4` paths. E2 wrappers intentionally stop if hashes, branch, output directories or approval do not match.

## Repository map

| Path | Purpose |
|---|---|
| `scripts/` | Data preparation, E1/E2 runners, audits, E3 matched controls and result verifier (23 scripts). |
| `results/` | Final E1/E2/E3 summaries, per-fit data, manifests and figures. |
| `manifests/` | Frozen source-checkpoint split and protocol metadata. |
| `tests/` | Four essential layout, result and E2 gate tests. |
| `report/final_report.md` | Canonical technical report. |
| `docs/` | Frozen E2 protocol, test-release notice and two historical integrity pointers. |
| `external/ModelXRay/` | Model X-Ray upstream Git submodule at a fixed commit. |
| `configs/` | Locked Ubuntu 24.04 / Python 3.11 dependency versions. |

The `G3/G4/G5/G6/G7` names in a few filenames are internal E2 gate labels (utility pilot, protocol freeze, runner/preflight, validation audit and test release), not additional experiments.

## Licences

- Project-authored code: MIT, as stated in [LICENSE](LICENSE).
- Model X-Ray upstream submodule: CC BY-NC-ND 4.0; its terms are separate from this repository's MIT licence.
- GHRP/STL10 data on Zenodo: CC BY 4.0; retain attribution and respect third-party components' terms.

## Authors

Riccardo D'Annibale and Fabrizio Giuseppe Mazzilli.
