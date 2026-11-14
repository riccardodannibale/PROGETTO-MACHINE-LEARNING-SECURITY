# Beyond the X-Ray

**Detecting steganographic modifications in neural network weights**  
Machine Learning Security project by Riccardo D’Annibale (2063306) and Fabrizio Giuseppe Mazzilli (2287495).

This repository contains the E1 X-LSB baseline, the E2 synthetic spread-spectrum transfer experiment, the E3 matched-control analysis, their published results, and the source code needed to understand and audit the work.

## Main findings

| Experiment | Main result |
|---|---|
| E1 — X-LSB baseline | At X=23, centroid AUROC is 0.901863 on Ubuntu and 0.904378 on Mac M4. |
| E2 — Spread-spectrum transfer | At alpha=0.24, centroid AUROC is 0.477620 on Ubuntu and 0.474500 on Mac M4. |
| E3 — Matched controls | Benign scores and FPR remain stable; TPR falls sharply for the tested spread-spectrum samples. |

These conclusions apply to the detector, checkpoint collection and synthetic embedding settings used in this project. The custom spread-spectrum method is educational and is not the original MaleficNet implementation.

## Complete report

The project theory, methodology, results, interpretation, limitations, reproducibility instructions, repository map and licensing notes are consolidated in one detailed report:

- [Complete project report](report/final_report.md)

## Repository map

| Path | Contents |
|---|---|
| `report/` | The single comprehensive project report. |
| `scripts/` | Data preparation, E1/E2/E3 runners, audits and result verification. |
| `tests/` | Essential submission and E2 protocol-gate checks. |
| `results/` | Final E1/E2/E3 tables, paired results, figures and provenance manifests. |
| `manifests/` | Frozen source-checkpoint split and protocol metadata. |
| `configs/` | Pinned Ubuntu/Python dependency list. |
| `external/ModelXRay/` | Model X-Ray upstream Git submodule at a fixed commit. |
| `docs/` | Only the frozen E2 protocol and the historical authorization/compatibility records required by its integrity checks. |

The original checkpoint collection and some raw prediction files are not included. Read the complete report before attempting a full rerun.

## Quick verification

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY
python3 scripts/verify_published_results.py
python3 tests/test_verify_published_results.py
python3 tests/test_repository_layout.py
python3 tests/test_e2_g5_preflight.py
python3 tests/test_e2_g7_release_contract.py
```

These checks verify the published aggregate summaries, essential repository paths and E2 protocol gates. They do not retrain the detector or rebuild AUROC from all raw predictions. There is no automatic GitHub Actions workflow in this submission branch; checks are run manually.

## Authors and license

**Authors:** Riccardo D’Annibale and Fabrizio Mazzilli.  
The project’s own code is distributed under the MIT License in [LICENSE](LICENSE). Model X-Ray and third-party data remain subject to their own terms.
