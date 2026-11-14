# E3 cross-platform summary

This report compares the E3 matched-control summaries from Ubuntu and Mac M4. Both platforms report ten fits, 200 paired source-checkpoint identities per fit, three test conditions and two scoring methods.

| Measure | Ubuntu ID | Ubuntu alpha=0.24 | Mac ID | Mac alpha=0.24 |
|---|---:|---:|---:|---:|
| AUROC | 0.9043 | 0.4776 | 0.9043 | 0.4745 |
| TPR at validation threshold | 0.8135 | 0.1815 | 0.8190 | 0.1785 |
| FNR | 0.1865 | 0.8185 | 0.1810 | 0.8215 |
| FPR | 0.1820 | 0.1820 | 0.1750 | 0.1750 |
| Matched concordance | 0.9265 | 0.4765 | 0.9280 | 0.4800 |

The fixed benign scores and validation threshold produce the same FPR across ID and OOD conditions within each platform. The main change is the decrease in TPR for modified spread-spectrum samples.

E3 does not train a general metadata classifier, rule out every possible preprocessing or representation shortcut, or match X-LSB and spread-spectrum for payload capacity or perturbation magnitude. It is a retrospective analysis of E2 outputs, not a new independent test set.
