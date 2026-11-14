# Results and Limitations

## Published E2 paired-test AUROC summaries

| Platform | ID (X-LSB) | Spread-spectrum α=0.24 | Spread-spectrum α=0.16 |
|---|---:|---:|---:|
| Ubuntu | 0.904273 | 0.477620 | 0.494701 |
| macOS M4 | 0.904300 | 0.474500 | 0.491042 |

These values are the paired-test AUROC summaries reported by the repository's published-result verifier. The ID setting has high AUROC in the evaluated configuration. The tested spread-spectrum OOD settings are around or below 0.5, so the detector does not demonstrate useful positive-ranking performance for these conditions. The result is scoped to this detector, checkpoint collection, and synthetic embedding implementation.

## Statistical interpretation

The 10 fit repetitions reuse the same 200 test checkpoint identities. They are correlated repeated evaluations, not 2,000 independent test models. E3 uses thresholds calibrated on LSB validation and held fixed for ID/OOD; it is a retrospective analysis of E2 scores.

## Reproducibility limitations

- The source checkpoint collection is finite; the test set is not an independently collected external model-zoo holdout.
- The synthetic spread-spectrum method is only one alternative embedding family.
- Raw prediction-level artifacts are not all distributed. Some public summaries cannot be independently reconstructed from the public clone alone.
- The published-result verifier checks summary consistency; it does not retrain models or recompute every AUROC from raw predictions.
- Full reruns require the original zoo/checkpoints, local validation artifacts, environment, and gated release inputs.
- Ubuntu and macOS may differ numerically because of hardware, libraries, and floating-point kernels.

These limitations define the supported scope of the conclusions and should accompany any presentation of the results.
