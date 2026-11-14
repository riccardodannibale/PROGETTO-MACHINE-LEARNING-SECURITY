# Third-party content and data policy

## Licensing

- **Project code and documents** (`scripts/`, `tests/`, `docs/`, `report/`, result tables and figures) are released under the MIT license in [`LICENSE`](../LICENSE).
- **Model X-Ray** ([`danigil/ModelXRay`](https://github.com/danigil/ModelXRay)) is included only as a pinned Git submodule (`external/ModelXRay`, commit `a880e332f556fc71faf8d3753931005d5d019339`). Upstream declares **CC BY-NC-ND 4.0** and mentions a patent application. The MIT license of this repository does **not** relicense it, and no modified copy of its code is distributed here.
- **MaleficNet** and **Model X-Ray** papers are cited as references only; their PDFs are not redistributed.

## Data

| Object | Status |
|---|---|
| GHRP/STL10 model zoo ([Zenodo 6631784](https://zenodo.org/records/6631784)) | Not included. Obtain it from the original source; `scripts/download_d1_stl10.sh` automates this with checksum verification. |
| `weights.npy` (1000 × 2864 float32) | Not included. Rebuilt with `scripts/extract_d1_real_weights.py`; SHA-256 in [`REPRODUCING.md`](../REPRODUCING.md). |
| Synthetic payloads / embedded checkpoints | Not included. Generated on the fly; payloads are inert random bytes. |
| Small summary CSVs, manifests, plots in `results/` | Included. Generated from our own runs; no third-party data. |
| Full raw prediction CSVs | Kept locally, not published. |

All experiments use synthetic, non-executable payloads. No real malware was created, embedded or distributed.

## Reproducibility notes

- Provenance and hashes: [`E1_REPRODUCIBILITY.md`](E1_REPRODUCIBILITY.md).
- Verification of published numbers without data: [`REPRODUCING.md`](../REPRODUCING.md).
