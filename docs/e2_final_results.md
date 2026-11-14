# E2 final results

E2 asks whether a Siamese detector trained and calibrated only on X-LSB X=23 transfers to a different synthetic embedding family. Each of ten fits is trained on three benign/stego pairs. The same fitted detector is evaluated on ID X-LSB and OOD spread-spectrum samples from the same 200 test checkpoint identities. No retraining or threshold recalibration is performed between conditions.

The spread method is a project-specific 16-bit synthetic embedding, not the original MaleficNet implementation. Alpha=0.24 is the primary setting; alpha=0.16 is secondary.

## Primary centroid results

| Condition | Ubuntu mean +/- SD | Mac M4 mean +/- SD |
|---|---:|---:|
| ID X-LSB X=23 | 0.904273 +/- 0.063014 | 0.904300 +/- 0.059861 |
| OOD spread alpha=0.24 | 0.477620 +/- 0.039926 | 0.474500 +/- 0.037686 |
| OOD spread alpha=0.16 | 0.494701 +/- 0.024164 | 0.491042 +/- 0.022405 |
| Delta AUROC, alpha=0.24 minus ID | -0.426652 +/- 0.085535 | -0.429800 +/- 0.084764 |

The primary Delta AUROC is negative in all ten fits on both platforms. The 1-NN secondary method shows the same broad trend: mean ID AUROC is 0.820174 on Ubuntu and 0.816670 on Mac, compared with 0.480515 and 0.480939 at alpha=0.24.

The detector retains strong ranking performance on the tested ID condition but does not show useful positive-ranking performance on the tested OOD conditions. This result is limited to the specific synthetic embedding and experiment settings. Perturbation magnitude and payload capacity are not matched to X-LSB, so the observed difference cannot be attributed to embedding family alone.

The ten fits reuse the same test identities. Standard deviations describe variation across fits on this fixed collection, not variation across independent checkpoint zoos.
