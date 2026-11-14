# Beyond the X-Ray
## Detecting Steganographic Modifications in Neural Network Weights

**Machine Learning Security project**  
**Authors:** Riccardo D'Annibale and Fabrizio Mazzilli  
**Experiments:** E1, E2 and E3

## Abstract

This project evaluates a Siamese few-shot detector inspired by Model X-Ray. E1 measures detection of X-LSB modifications. E2 tests whether the same detector transfers to a project-specific synthetic spread-spectrum embedding. E3 audits matched benign/modified pairs and metadata-related controls.

The experiments use 1,000 small CNN checkpoints from the GHRP/STL10 collection, each represented by 2,864 float32 parameters. The source-checkpoint split is fixed at 600 training, 200 validation and 200 test identities. Each few-shot fit uses three benign/stego pairs.

At X-LSB X=23, E1 reports mean centroid AUROC 0.901863 on Ubuntu and 0.904378 on Mac M4. In E2, the same detector is evaluated on a 16-bit synthetic spread-spectrum embedding. At the primary setting alpha=0.24, mean centroid AUROC is 0.477620 on Ubuntu and 0.474500 on Mac M4. E3 finds that benign scores and FPR remain unchanged across conditions at the fixed validation threshold, while TPR drops substantially for the spread-spectrum samples.

These findings are limited to the detector, checkpoint collection and embedding settings tested. They do not show that spread-spectrum methods are generally undetectable and are not a reproduction of MaleficNet.

## 1. Experimental setup

### Data and split

The study uses 1,000 original CNN checkpoints. Each checkpoint is represented by 2,864 float32 weights. The frozen split contains 600 training-pool identities, 200 validation identities and 200 test identities. Benign and modified versions of a source checkpoint remain in the same partition.

Each fit uses three source identities for training, with one benign and one modified example per identity. Ten fits are run per configuration. The same validation and test identities are reused across fits, so repetitions measure fit variability rather than ten independent datasets.

### Detector

The detector follows the Siamese few-shot approach implemented by Model X-Ray. The upstream repository is pinned to commit `a880e332f556fc71faf8d3753931005d5d019339`. Model weights are transformed into 100 by 100 representations and passed through the Siamese CNN.

The primary scoring method is centroid distance. The secondary method is 1-NN. The score is `distance_to_benign - distance_to_stego`; higher values favour the stego class. The binary threshold is either zero or selected on the X-LSB validation set using Youden's index. No threshold is tuned on OOD test labels.

## 2. Experiments

### E1 — X-LSB baseline

E1 evaluates X-LSB settings X=1, 8, 16 and 23. The method modifies the selected number of least-significant mantissa bits in float32 weights using deterministic synthetic bytes.

| X-LSB | Ubuntu centroid AUROC | Mac M4 centroid AUROC |
|---:|---:|---:|
| 1 | 0.500150 | 0.500209 |
| 8 | 0.508232 | 0.509388 |
| 16 | 0.501293 | 0.501425 |
| **23** | **0.901863** | **0.904378** |

At X=23, mean test accuracy using the validation Youden threshold is 0.82125 on Ubuntu and 0.82300 on Mac M4. The corresponding FPR values are 0.1550 and 0.1605.

### E2 — Spread-spectrum test

E2 trains and calibrates only on X-LSB X=23. The same fitted detector is evaluated on X-LSB ID examples and on a project-specific synthetic spread-spectrum method that was not used during training or calibration.

The custom method embeds a 16-bit synthetic message using deterministic, approximately orthonormal code vectors. It adds a perturbation to the weight vector with relative L2 magnitude controlled by alpha. The primary setting is alpha=0.24; alpha=0.16 is secondary.

This is an educational implementation inspired by the general spread-spectrum idea. It is not the original MaleficNet implementation: it does not include the original error-correction pipeline, fine-tuning procedure or model setup. The payload is synthetic and inert, not executable content.

| Test condition | Ubuntu mean +/- SD | Mac M4 mean +/- SD |
|---|---:|---:|
| ID: X-LSB X=23 | 0.904273 +/- 0.063014 | 0.904300 +/- 0.059861 |
| OOD: spread alpha=0.24 | 0.477620 +/- 0.039926 | 0.474500 +/- 0.037686 |
| OOD: spread alpha=0.16 | 0.494701 +/- 0.024164 | 0.491042 +/- 0.022405 |
| **Delta AUROC: alpha=0.24 minus ID** | **-0.426652 +/- 0.085535** | **-0.429800 +/- 0.084764** |

The primary Delta AUROC is negative in all ten fits on both platforms. The secondary 1-NN method shows the same broad pattern: mean ID AUROC is 0.820174 on Ubuntu and 0.816670 on Mac M4, compared with 0.480515 and 0.480939 at alpha=0.24.

The two embedding methods are not matched for perturbation magnitude or payload capacity. In the training-only G2 pilot, mean relative L2 perturbation was approximately 0.3126 for X-LSB X=23, compared with 0.16 and 0.24 for the spread settings. E2 therefore measures the detector's response to these particular conditions; it does not isolate the causal effect of embedding family alone.

### E3 — Matched controls

E3 is a retrospective analysis of the E2 test scores. It does not retrain the detector or create a new holdout. For each fit, method and test condition, it verifies one benign and one modified sample from the same source checkpoint.

For centroid scoring at alpha=0.24:

| Measure | Ubuntu ID | Ubuntu OOD | Mac ID | Mac OOD |
|---|---:|---:|---:|---:|
| AUROC | 0.9043 | 0.4776 | 0.9043 | 0.4745 |
| TPR | 0.8135 | 0.1815 | 0.8190 | 0.1785 |
| FNR | 0.1865 | 0.8185 | 0.1810 | 0.8215 |
| FPR | 0.1820 | 0.1820 | 0.1750 | 0.1750 |
| Matched concordance | 0.9265 | 0.4765 | 0.9280 | 0.4800 |

Benign scores remain unchanged across conditions within a fit and scoring method. The fixed validation threshold therefore produces the same FPR. The main change is in modified samples: TPR drops sharply for the spread-spectrum condition.

The metadata-only majority baseline is 50% by construction because each source identity has one benign and one modified example. This does not rule out every possible shortcut in preprocessing, serialization or representation.

## 3. Interpretation

The detector performs well on the tested ID X-LSB condition but does not transfer its ranking performance to the specific synthetic spread-spectrum method tested here. E3 adds evidence that this OOD drop is not explained by a change in benign scores or by a different FPR under the fixed threshold.

The supported conclusion is limited: under the checkpoint collection, detector, perturbation levels and payload settings used in this project, a few-shot detector trained on X-LSB does not transfer its ranking performance to the tested synthetic spread-spectrum embedding.

The experiments do not show that all spread-spectrum methods are undetectable, that the original Model X-Ray findings are incorrect, or that this embedding preserves CNN utility in general. The utility pilot used only three source checkpoints and 256 images; it is a feasibility check, not a broad claim about model utility.

## 4. Limitations

- **One checkpoint collection:** no generalization test across CNN architectures or independent model zoos.
- **Repeated test identities:** ten fits reuse the same 200 test checkpoints; they are not ten independent test samples.
- **Different perturbation scales:** X-LSB X=23 and spread alpha=0.24/0.16 are not matched for relative L2 magnitude or payload capacity.
- **Retrospective E3:** E3 analyzes E2 test scores after they were available; it is not a new blind holdout.
- **Synthetic payloads:** no executable malware or operational attack was tested.
- **Limited utility pilot:** only three checkpoints and 256 images were used.
- **Incomplete raw outputs:** not all prediction-level artifacts and original checkpoints are included in the public repository.
- **Numerical reproducibility:** aggregate Ubuntu and Mac results are close, but bitwise-identical TensorFlow training is not claimed.

## 5. Reproducibility

The repository includes experiment scripts, tests, an environment lock file, source-checkpoint split manifest, published CSV summaries, figures and audit records. Large source checkpoints and locally generated intermediate arrays are not redistributed.

From a fresh clone:

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY
python3 scripts/verify_published_results.py
```

This check verifies the internal consistency of published E2/E3 summary CSVs. It does not retrain the detector or rebuild AUROC from raw predictions. For environment setup, dataset acquisition, artifact audits and experiment entry points, see [REPRODUCING.md](../REPRODUCING.md). Dataset and third-party licensing details are in [docs/data_and_licensing.md](../docs/data_and_licensing.md).

## References

1. D. Gilkarov and R. Dubin, *Model X-Ray: Detection of Hidden Malware in AI Model Weights Using Few Shot Learning*, arXiv:2409.19310 (2024); journal version in *Journal of Information Security and Applications* (2026), DOI: 10.1016/j.jisa.2026.104517. Code: https://github.com/danigil/ModelXRay.
2. D. Hitaj et al., *MaleficNet: Hiding Malware into Deep Neural Networks Using Spread-Spectrum Channel Coding*, ESORICS 2022, DOI: 10.1007/978-3-031-17143-7_21.
3. D. Hitaj et al., *Do You Trust Your Model? Emerging Malware Threats in the Deep Learning Ecosystem*, arXiv:2403.03593 (2024).
4. GHRP/STL10 checkpoint collection: https://zenodo.org/records/6631784.

**Project scope:** This is a university research project. Results should be interpreted within the experimental conditions and limitations described above.
