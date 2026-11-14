# Beyond the X-Ray

**Detecting steganographic modifications in neural network weights**  
Machine Learning Security project by Riccardo D'Annibale and Fabrizio Mazzilli.

This project evaluates a Siamese few-shot detector inspired by Model X-Ray. It covers an in-distribution X-LSB baseline (E1), a test on a project-specific synthetic spread-spectrum embedding (E2), and a retrospective matched-control analysis (E3).

## Main results

| Experiment | Main result |
|---|---|
| **E1 — X-LSB baseline** | At X=23, centroid AUROC is 0.901863 on Ubuntu and 0.904378 on Mac M4. |
| **E2 — Spread-spectrum test** | At alpha=0.24, centroid AUROC is 0.477620 on Ubuntu and 0.474500 on Mac M4. |
| **E3 — Matched controls** | Benign scores and FPR remain unchanged at the fixed validation threshold; TPR falls sharply for the spread-spectrum samples. |

These results apply to the tested detector, checkpoint collection and embedding settings. They do not show that spread-spectrum methods are generally undetectable and are not a reproduction of MaleficNet.

## Final report

- [Final report (PDF)](report/final_report.pdf)
- [Final report (Word)](report/final_report.docx)
- [Final report (Markdown)](report/final_report.md)

## Repository map

| Path | Contents |
|---|---|
| `report/` | Final report in PDF, DOCX and Markdown. |
| `scripts/` | Experiment runners, audit tools, plotting and published-result verification. |
| `tests/` | Unit and regression tests. |
| `results/` | Published CSV summaries, figures, platform comparisons and audit records. |
| `manifests/` | Frozen source-checkpoint split and protocol metadata. |
| `configs/` | Pinned Ubuntu/Python dependency list. |
| `external/ModelXRay/` | Model X-Ray upstream Git submodule at a fixed commit. |
| `docs/` | Experimental design, setup, licensing and experiment notes. |
| `REPRODUCING.md` | Verification and reproduction instructions. |

The experiment code uses scripts rather than notebooks. The original checkpoint collection and some raw prediction files are not included; see the data and licensing notes before attempting a full rerun.

## Quick check

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY
python3 scripts/verify_published_results.py
python3 tests/test_repository_layout.py
```

A successful result check prints `PUBLISHED E2/E3 SUMMARY QA OK`. The layout test checks internal Markdown links and required experiment records. These checks do not retrain the detector or rebuild AUROC from raw predictions. See [REPRODUCING.md](REPRODUCING.md) for details.

## Authors and license

**Authors:** Riccardo D'Annibale and Fabrizio Mazzilli.

The project's own code is distributed under the MIT License in [LICENSE](LICENSE). Model X-Ray and third-party data remain subject to their own terms. See [docs/data_and_licensing.md](docs/data_and_licensing.md).
