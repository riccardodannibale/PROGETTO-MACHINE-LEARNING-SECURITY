# E2 utility pilot on original CNN checkpoints

This training-only pilot checked that modified vectors corresponded to real CNN parameters and measured the effect of embedding on a small image sample. It was not an OOD detector result.

- Three checkpoints from the detector training pool: `row_index` 3, 4 and 7.
- Original CNN parameters were reconstructed and matched against the extracted weight matrix.
- The same 256 images from the image-validation split were used in each condition.
- The CNNs were evaluated without fine-tuning.
- Conditions: benign, X-LSB X=23, spread alpha=0.16 and spread alpha=0.24.

| Condition | Mean image classification accuracy | Change from benign | Mean relative L2 |
|---|---:|---:|---:|
| Original benign | 37.2396% | 0 pp | 0% |
| X-LSB X=23 | 26.0417% | -11.1979 pp | 31.2191% |
| Spread alpha=0.16 | 35.6771% | -1.5625 pp | 16.0000% |
| Spread alpha=0.24 | 31.3802% | -5.8594 pp | 24.0000% |

All 16-bit messages were recovered for the three pilot checkpoints at both spread settings. The sample is too small to support a general claim that spread-spectrum preserves CNN utility. This is a feasibility check only.
