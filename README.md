# Machine Learning Security Project

University project focused on the detection of
steganographic payloads in neural network weights.

## Reference paper

Model X-Ray: Detection of Hidden Malware in AI Model
Weights Using Few Shot Learning.

Gilkarov and Dubin, 2026.

DOI: https://doi.org/10.1016/j.jisa.2026.104517

## Objectives

- Reproduce selected Model X-Ray experiments.
- Evaluate in-distribution stegomalware detection.
- Evaluate generalization to unseen embedding techniques.
- Investigate dataset leakage and confounding factors.

## Repository structure

- `external/ModelXRay/`: original upstream implementation
- `src/`: project-specific Python code
- `scripts/`: experiment and setup scripts
- `configs/`: experiment configurations
- `tests/`: automated tests
- `manifests/`: checkpoint and dataset metadata
- `results/`: experimental results and figures
- `docs/`: documentation and experiment logs
- `exam/`: final report and presentation

## Clone

git clone --recurse-submodules --branch ricky \
  https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git

## Upstream

https://github.com/danigil/ModelXRay

The upstream code is maintained as a Git submodule
and remains subject to its original license.

## Safety

Experiments use synthetic, non-executable payloads.
Untrusted model checkpoints must not be deserialized
using unsafe loaders.
