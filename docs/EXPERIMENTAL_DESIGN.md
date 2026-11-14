# Experimental Design

## Study objective

The study evaluates a Siamese few-shot detector for steganographic modifications in neural-network weights. E1 is the controlled in-distribution baseline; E2 studies generalization to a project-specific synthetic spread-spectrum embedding family; E3 adds a retrospective matched-control analysis.

## E1 — In-distribution baseline

E1 uses the X-LSB embedding setting and a Siamese few-shot detector inspired by Model X-Ray. Data partitions are separated at source-checkpoint identity level to avoid placing derivatives of the same source checkpoint in multiple partitions. The canonical split manifest and protocol metadata are under `manifests/e1_uniform_v1/`.

## E2 — Out-of-distribution evaluation

E2 evaluates an alternative synthetic spread-spectrum method based on keyed orthogonal codes and a 16-bit payload. This is a project-specific method and is not MaleficNet. Validation and test are separated by a documented release procedure. The E2 runner and audit tools retain protocol and integrity checks; frozen protocol/release files are experimental records and must not be edited during a documentation-only change.

## E3 — Matched controls

E3 performs a retrospective analysis of matched benign and modified samples using existing E2 test scores. It is not a separate detector-training experiment and is not a newly collected blind holdout.

## Provenance and safeguards

The repository records seeds, source-checkpoint identities, split assignments, selected artifact hashes, upstream commit identity, environment information, and audit outputs. The published cross-platform analysis compares Ubuntu and macOS M4 runs; it does not claim bitwise identity.
