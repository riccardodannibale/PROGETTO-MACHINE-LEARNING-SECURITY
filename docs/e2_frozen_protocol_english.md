# E2 frozen protocol — English reading note

> **Integrity note:** the original `docs/E2_PROTOCOL_FROZEN.md` is preserved byte-for-byte because the E2 runner verifies its SHA-256 hash. This file is an English reading note and does not replace the original integrity record.

## Research question
Measure whether a Siamese Model X-Ray detector trained and calibrated only on X-LSB transfers to a project-specific spread-spectrum embedding that was not presented during training or calibration.

## Experimental design
- Use the frozen source-checkpoint split: 600 training-pool identities, 200 validation identities and 200 test identities.
- Train each fit using three benign/stego pairs from the training pool.
- Run ten fits per platform.
- Keep X-LSB X=23 as the only training and validation embedding condition.
- Evaluate ID X-LSB and OOD spread-spectrum alpha=0.24 (primary) and alpha=0.16 (secondary) on the same test identities.
- Use centroid AUROC as the primary metric and 1-NN/threshold metrics as secondary measures.
- Select thresholds on LSB validation data only. Do not tune on OOD test labels.

## Method scope
The spread method is `e2-keyed-orthogonal-spread-v0-educational`. It uses an inert 16-bit synthetic payload and keyed orthogonal codes. It is inspired by general spread-spectrum principles and is not the original MaleficNet implementation.

## Stop conditions
The original runner includes fail-closed checks for the frozen protocol, validation completion, hashes, source identities and separate test-release approval. Do not bypass those checks or overwrite completed runs. A full rerun should use the historical experiment branch and exact frozen inputs.

## Interpretation limits
The checkpoint collection is fixed and homogeneous. Ten fits reuse the same test identities. X-LSB and spread-spectrum are not matched for perturbation magnitude or payload capacity. The experiment does not isolate embedding family as the only causal factor.
