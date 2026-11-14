# Experimental design

The project evaluates a Siamese few-shot detector for steganographic modifications in neural-network weights. It is organized into three experiments.

## E1 — In-distribution baseline
E1 uses X-LSB modifications and a detector inspired by Model X-Ray. Train, validation and test are split by source-checkpoint identity. The frozen split is stored in `manifests/e1_uniform_v1/`. The evaluated settings are X = 1, 8, 16 and 23.

## E2 — Embedding-family shift
E2 trains and calibrates only on X-LSB X=23. The same fitted detector is evaluated on X-LSB test examples and on a project-specific synthetic spread-spectrum embedding with a 16-bit payload. The primary setting is alpha=0.24; alpha=0.16 is secondary. This educational method is not the original MaleficNet implementation.

## E3 — Matched controls
E3 re-examines existing E2 test scores. It checks one-to-one benign/modified pairing by source identity, metadata balance, equality of benign scores across conditions, false-positive rates at the fixed validation threshold and within-pair score concordance. It does not retrain the detector or create a new blind holdout.

## Safeguards
The repository records source-checkpoint splits, configuration, seeds, hashes, the pinned upstream submodule and audit outputs. Thresholds are calibrated on validation data only. Test results are not used to select new parameters.
