# Results and limitations

## Published centroid AUROC

| Platform | ID X-LSB X=23 | Spread alpha=0.24 | Spread alpha=0.16 |
|---|---:|---:|---:|
| Ubuntu | 0.904273 | 0.477620 | 0.494701 |
| Mac M4 | 0.904300 | 0.474500 | 0.491042 |

These are means over ten paired fits on each platform. The same 200 test checkpoint identities are reused across fits, so the repetitions are not ten independent test datasets.

The detector performs well on the tested ID X-LSB condition. It does not show useful positive-ranking performance on the two tested synthetic OOD spread-spectrum conditions. This result is limited to the detector, checkpoint collection and embedding settings used in the project.

## E3 controls

For centroid scoring at alpha=0.24, TPR decreases from 0.8135 to 0.1815 on Ubuntu and from 0.8190 to 0.1785 on Mac M4. FPR remains fixed at 0.1820 and 0.1750, respectively, because benign scores and the validation threshold are unchanged across conditions within a fit.

## Limitations

- One collection of small CNN checkpoints; no generalization test across architectures or independent model zoos.
- X-LSB X=23 and spread alpha=0.24/0.16 are not matched for perturbation magnitude or payload capacity.
- E3 is a retrospective analysis of E2 test scores, not a new blind holdout.
- Payloads are synthetic and inert. No executable malware or operational attack was tested.
- Some raw prediction files and original checkpoints are not distributed.
- Ubuntu and Mac results agree at the aggregate level, but bitwise-identical TensorFlow training is not claimed.

See `../report/final_report.pdf` for the full discussion.
