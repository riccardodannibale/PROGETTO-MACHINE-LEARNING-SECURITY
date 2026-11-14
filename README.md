# Beyond the X-Ray: Detecting Steganographic Modifications in Neural Network Weights

## Project overview

This project studies whether steganographic modifications embedded in neural-network parameters can be detected by a Siamese few-shot detector. It uses the Model X-Ray research direction as a controlled baseline and extends the investigation with (i) a project-specific synthetic spread-spectrum embedding method and (ii) a matched-control analysis.

The central finding is deliberately mixed: the detector achieves a high published in-distribution (ID) AUROC for the X-LSB setting, but does **not** show useful positive-ranking performance on the tested synthetic spread-spectrum out-of-distribution (OOD) settings. This distinction is important: the work evaluates a specific checkpoint collection and two specified embedding settings; it does not establish universal detection of model steganography.

## Research questions

1. Can a Siamese few-shot detector identify X-LSB modifications when training and evaluation use the same embedding family?
2. How does the detector behave when evaluated on a different synthetic embedding family not observed in the baseline training setting?
3. Do matched benign/stego controls add context for interpreting the observed detection results and possible confounding effects?

## Contributions and experiments

### E1 — In-distribution baseline

E1 implements a controlled Siamese few-shot detection baseline inspired by Model X-Ray. It evaluates the X-LSB setting. Train, validation, and test partitions are separated by **source-checkpoint identity**, not by randomly splitting derivative samples. The split manifest and protocol metadata are published under `manifests/e1_uniform_v1/`.

### E2 — Synthetic spread-spectrum and OOD evaluation

E2 introduces a project-specific synthetic spread-spectrum embedding mechanism using keyed orthogonal codes and a 16-bit payload. It is an experimental method developed for this project; it is **not** MaleficNet and should not be described as a reproduction of MaleficNet. E2 separates validation from test evaluation and records release conditions, audit procedures, and cross-platform results.

### E3 — Matched controls

E3 performs a retrospective matched-control analysis on existing E2 test scores. It compares benign and modified samples under documented conditions. E3 is an analysis of prior outputs, **not** a new independent detector-training experiment or a fresh blind holdout.

## Main published E2 result

The table below reports the published paired-test AUROC summaries printed by `scripts/verify_published_results.py` (10 paired centroid runs per platform):

| Platform | ID (X-LSB) | Spread-spectrum α=0.24 | Spread-spectrum α=0.16 |
|---|---:|---:|---:|
| Ubuntu | 0.904273 | 0.477620 | 0.494701 |
| macOS M4 | 0.904300 | 0.474500 | 0.491042 |

The ID result is high in the evaluated setting. By contrast, the tested OOD AUROCs are around or below 0.5, indicating that the detector did not achieve useful positive-ranking discrimination for these spread-spectrum conditions. These results should be interpreted within the defined experiment; they do not prove that every possible spread-spectrum detector or embedding is undetectable.

The 10 fits reuse the same 200 test checkpoint identities. Repeated fits must therefore not be treated as 2,000 independent test models when interpreting uncertainty. The published verifier checks consistency of summaries; it does not rescore every raw prediction.

## Methodological safeguards and provenance

The repository records experimental configuration, random seeds, source-checkpoint partitions, SHA-256 integrity information, the pinned upstream submodule, and audit outputs. E2 distinguishes validation from test and includes documented test-release conditions. Cross-platform comparisons cover Ubuntu and macOS M4 where artifacts are available; numerical agreement does not imply bitwise identity.

## Repository guide

| Path | Purpose |
|---|---|
| `README.md` | Project summary, contributions, main results, limitations, and navigation. |
| `REPRODUCING.md` | Three levels of verification, artifact audit, and experiment recreation requirements. |
| `configs/` | Pinned software-environment specification. |
| `manifests/e1_uniform_v1/` | Source-checkpoint split manifest and frozen E1 protocol metadata. |
| `external/ModelXRay/` | Model X-Ray upstream Git submodule, pinned to the commit documented in `REPRODUCING.md`. |
| `scripts/` | Dataset setup, weight extraction, experiment runners, plotting, and audit tools. |
| `tests/` | Standalone tests for helpers, release contracts, audits, and published-result verification. |
| `results/` | Published CSV summaries, per-run artifacts where distributed, audits, and figures for E1/E2/E3. |
| `report/` | Final project report in PDF/DOCX and its source, where present. |
| `docs/` | Experimental design, results interpretation, data/licensing notes, setup, and frozen protocol records. |

Important result locations include `results/e2_final/`, `results/e3_final/`, `results/figures/`, E1 validation/test outputs, platform replicas, and pilot artifacts. Inspect the actual subdirectories for the available files; not every raw prediction artifact is distributed.

## Quick verification

Clone with the upstream submodule and run the lightweight published-summary check:

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY
python3 scripts/verify_published_results.py
```

A successful run prints `PUBLISHED E2/E3 SUMMARY QA OK`. This is **Level 0 published-summary verification**, not a rerun of training and not an independent reconstruction of AUROC from all raw predictions.

For environment setup, data acquisition, artifact audits, and full experiment prerequisites, follow [`REPRODUCING.md`](REPRODUCING.md). The primary English-facing technical notes are [`docs/EXPERIMENTAL_DESIGN.md`](docs/EXPERIMENTAL_DESIGN.md), [`docs/RESULTS_AND_LIMITATIONS.md`](docs/RESULTS_AND_LIMITATIONS.md), and [`docs/DATA_AND_LICENSES.md`](docs/DATA_AND_LICENSES.md).

## Scientific limitations

- The checkpoint collection is finite; the test partition is not an independently collected external model-zoo holdout.
- The spread-spectrum method is synthetic and represents one investigated alternative embedding family, not all possible model-steganography methods.
- The 10 fits reuse the same 200 test checkpoint identities; repeated fits are correlated.
- The OOD AUROC results are near/below 0.5 for the tested settings. Claims must remain limited to these settings and this detector.
- E3 is retrospective and uses existing E2 test scores; it is not a fresh blind holdout.
- Not all raw prediction-level artifacts are distributed, so some published summaries cannot be reconstructed independently from the public clone alone.
- Full reproduction requires source data, model checkpoints, compatible environments, local validation artifacts, and test-release inputs that may not be included in Git.
- Ubuntu and macOS may produce small numerical differences due to hardware, libraries, and floating-point kernels.

These constraints define the scope of the evidence; they do not invalidate the experiments.

## Upstream work, authors, and license

The baseline is inspired by **Model X-Ray** (Gilkarov and Dubin). The upstream implementation is maintained as the `external/ModelXRay/` Git submodule; its pinned commit and licensing information are recorded in the repository documentation. Do not copy upstream files into the project's MIT-licensed code tree or assume the project license overrides third-party terms.

**Authors:** Riccardo D'Annibale and Fabrizio Mazzilli.

The original project code is distributed under the license in [`LICENSE`](LICENSE), subject to the separate licenses and terms governing third-party code, datasets, and model artifacts. See [`docs/DATA_AND_LICENSES.md`](docs/DATA_AND_LICENSES.md) before redistribution.
