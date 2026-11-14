# E2 protocol review

This note summarizes the E2 protocol review. The frozen protocol file itself is retained unchanged because the E2 runner checks its SHA-256 hash. This English note is for reading; it is not used as the integrity source by the runner.

## Frozen settings
- Source-checkpoint split: 600 training-pool identities, 200 validation identities, 200 test identities.
- Few-shot training: three benign/stego pairs per fit.
- Ten fits per platform.
- Primary score: centroid AUROC and paired OOD-minus-ID difference.
- Secondary score: 1-NN, alpha=0.16 and threshold-based metrics.
- Primary spread setting: alpha=0.24.
- Secondary spread setting: alpha=0.16.
- Threshold calibration: X-LSB validation only.

The original frozen record is `docs/E2_PROTOCOL_FROZEN.md`. Do not edit that file as part of documentation cleanup; its exact contents and hash are part of the experiment provenance.

The spread-spectrum method is an educational 16-bit synthetic implementation, not MaleficNet. The experiment is an internal attack-family-shift test on one checkpoint collection. X-LSB and spread settings are not matched for relative perturbation magnitude or payload capacity. E3 is a retrospective audit of E2 scores, not a new blind holdout.
