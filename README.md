# Beyond the X-Ray

**Importante:** `main` è il branch della consegna; i runner sperimentali E1/E2 funzionano soltanto dal branch `ricky` e si fermano se vengono lanciati da `main`.

**Detecting steganographic modifications in neural network weights**  
Machine Learning Security project by Riccardo D'Annibale and Fabrizio Giuseppe Mazzilli.

This project evaluates a few-shot detector inspired by Model X-Ray on X-LSB weight modifications and tests transfer to a project-specific synthetic spread-spectrum encoder. The experimental protocol uses source-checkpoint-disjoint train/validation/test splits, paired ID/OOD conditions and retrospective matched controls.

## Main results

### E1 - X-LSB baseline

Centroid test results:

| X-LSB | Ubuntu AUROC | Ubuntu AUPRC (mean ± SD) | Mac M4 AUROC | Mac M4 AUPRC (mean ± SD) |
|---:|---:|---:|---:|---:|
| 1 | 0.500150 | 0.504064 ± 0.001444 | 0.500209 | 0.504417 ± 0.001155 |
| 8 | 0.508233 | 0.509345 ± 0.025420 | 0.509388 | 0.510389 ± 0.025776 |
| 16 | 0.501293 | 0.512234 ± 0.021902 | 0.501425 | 0.512511 ± 0.023323 |
| **23** | **0.901863** | **0.902063 ± 0.069213** | **0.904378** | **0.904875 ± 0.065256** |

The detector is near chance at X=1, 8 and 16, and detects X=23 in this checkpoint collection.

### E2 - ID/OOD transfer

Centroid results over ten fits:

| Condition | Ubuntu AUROC (mean ± SD) | Ubuntu AUPRC | Mac M4 AUROC (mean ± SD) | Mac M4 AUPRC |
|---|---:|---:|---:|---:|
| ID: X-LSB X=23 | 0.904273 ± 0.063014 | 0.904619 | 0.904300 ± 0.059861 | 0.904341 |
| OOD: spread alpha=0.24 | 0.477620 ± 0.039926 | 0.492045 | 0.474500 ± 0.037686 | 0.488265 |
| OOD: spread alpha=0.16 | 0.494701 ± 0.024164 | 0.497873 | 0.491042 ± 0.022405 | 0.496086 |

AUPRC per-fit standard deviations are not present in the published E2 aggregate tables and are therefore not reported here.

### E3 - matched controls

The TPR falls from about 81-82% on ID to about 18% on spread alpha=0.24. The stable FPR is a structural check, not an independent result: benign scores are identical across ID/OOD by construction, and the validation threshold is held fixed.

## Scientific scope

The project reuses upstream Model X-Ray Siamese/X-LSB components but adapts the protocol; it is not a bit-for-bit reproduction. The paper's 2026 OOD transfer result concerns MaleficNet. This project tests `e2-keyed-orthogonal-spread-v0-educational`, a custom educational encoder rather than the original MaleficNet implementation. The E2 result therefore does not contradict the paper.

X counts modified mantissa-bit positions and is not directly comparable to the paper's embedding-rate percentages. X-LSB X=23 and spread alpha=0.16/0.24 are not intensity- or capacity-matched. The possible role of relative L2 perturbation is discussed as an unverified hypothesis in the report.

## Report

The complete Italian report, with the methodology, results, limitations, chronology note, reproducibility appendix and repository map, is maintained as the canonical source:

- [report/final_report.md](report/final_report.md)

The PDF and editable LaTeX source are supplied separately as submission files. The DOCX and duplicate report files are intentionally not maintained in this repository.

## Quick verification

Clone `main` including the upstream submodule:

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY

python3 scripts/verify_published_results.py
python3 tests/test_verify_published_results.py
python3 tests/test_repository_layout.py
python3 tests/test_e2_g5_preflight.py
python3 tests/test_e2_g7_release_contract.py
```

These checks validate the published aggregate summaries, repository layout and E2 integrity gates. They do not retrain the detector or recreate the full predictions. There is no active GitHub Actions workflow on `main`; run the checks manually.

## Reproduction data and integrity

The original checkpoint collection and `weights.npy` are not stored in the repository. The expected matrix has shape 1000 × 2864, dtype `float32` and size about 10.92 MiB. Source data: [Zenodo record 6631784](https://zenodo.org/records/6631784).

Expected `weights.npy` SHA-256:

```text
5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad
```

To recreate it, download the source data, extract the archive containing `tune_zoo_stl_small_uniform/`, then run `scripts/extract_d1_real_weights.py` with `--expected-models 1000`. Publish a Release asset only after checking the exact hash and including the extraction manifest and attribution.

## Runner branch and protocol

For the frozen experiment runners:

```bash
git switch ricky
git rev-parse HEAD
```

The experiment branch head recorded for this delivery is `3ef84f73d994fc447b12bb99f265c203548480e4`. E1 test and E2 wrappers enforce this branch name and check the frozen runner/protocol hashes. E2 additionally requires the recorded sequence of validation, audit and local test-release authorization. Do not remove these gates or modify `docs/E2_PROTOCOL_FROZEN.md`.

The full command sequence, local paths and protocol constraints are documented in Appendix A of the report.

## Repository map

| Path | Purpose |
|---|---|
| `report/final_report.md` | Single canonical report source. |
| `scripts/` | Data preparation, E1/E2 runners, audits, E3 controls and result verifier (23 scripts). |
| `results/` | Published E1/E2/E3 tables, per-fit outputs, manifests and figures. |
| `manifests/` | Frozen split and experiment protocol metadata. |
| `tests/` | Four essential layout, results and E2-gate checks. |
| `docs/` | Frozen E2 protocol, test-release record and two historical integrity pointers. |
| `external/ModelXRay/` | Upstream Model X-Ray submodule pinned to a fixed commit. |
| `configs/` | Locked Ubuntu 24.04 / Python 3.11 dependencies. |

The `G3/G4/G5/G6/G7` labels are internal E2 gate names, not additional scientific experiments.

## Licences

- Project-authored code: MIT (`LICENSE`).
- Model X-Ray upstream: CC BY-NC-ND 4.0; its terms are separate from this repository's MIT licence.
- GHRP/STL10 source data: CC BY 4.0; retain attribution and respect third-party components' terms.
