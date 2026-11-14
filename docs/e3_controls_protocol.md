# E3 matched controls

E3 is a retrospective audit of E2 test scores. It does not introduce a new attack, retrain the Siamese detector or create an independent holdout.

## Checks
- One benign and one modified observation exist for each source checkpoint.
- Source identifiers and hashes agree within each pair.
- The split remains source-checkpoint-disjoint.
- The metadata-only majority baseline is 50% under the 1:1 pairing.
- Benign scores are unchanged across ID/OOD conditions within the same fit and scoring method.
- The same validation threshold is applied to ID and OOD conditions.
- AUROC, TPR, FNR, FPR and matched concordance agree with the per-fit records.

The CSV reader uses round-trip floating-point parsing to preserve threshold comparisons near one-ULP differences.

## Results
For centroid scoring at alpha=0.24, TPR decreases from 0.8135 to 0.1815 on Ubuntu and from 0.8190 to 0.1785 on Mac M4. FPR remains fixed at 0.1820 and 0.1750, respectively. Matched concordance drops from 0.9265 to 0.4765 on Ubuntu and from 0.9280 to 0.4800 on Mac.

The same 200 test identities are reused across ten fits. Because E3 was run after E2 test scores had been examined, it is a retrospective control analysis rather than a new blind test.
