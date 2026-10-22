# Third-party content, data policy and licensing review

**Status: review checklist, not legal advice or confirmation of distribution rights.**

## Why this matters

The historical repository snapshot (16 October 2026) had a top-level **MIT** `LICENSE` with a single named copyright holder. The project itself was carried out by **two contributors, Riccardo and Fabrizio**. Their contributions and any change to license/copyright metadata should be agreed between them; do not silently rewrite the historical license.

The upstream [`danigil/ModelXRay`](https://github.com/danigil/ModelXRay) explicitly declares **CC BY-NC-ND 4.0** and mentions a US provisional patent application. This is **not automatically compatible with treating all upstream source code as MIT**, particularly when making derivative copies. The repository's technical workflow uses a pinned upstream dependency; keep it referenced as upstream rather than silently vendoring modified code.

## Inventory and recommended handling

| Type | Recommendation | Action before public release |
|---|---|---|
| Original student experiment code | Keep in `scripts/` and `tests/`, subject to actual authorship agreement. | Determine applicable project code license/ownership. |
| Model X-Ray third-party source | Keep upstream in `external/ModelXRay` as a genuine Git submodule (or documented external dependency), not as uncredited MIT source. | Confirm its exact license/version; avoid redistributing modified copies without authorization. |
| GHRP/STL10 original checkpoint zoo, preprocessed dataset | Keep **outside** the public repository unless redistribution rights are explicitly confirmed. | Provide data source reference and SHA-256; keep local data. |
| `weights.npy`, checkpoint `.pt`, payload `.bin`, downloaded model files | Usually keep **outside** Git (already in local `~/mlsec-local/`). | Check license and sizes; do not push into Git history. |
| `docs/references/*.pdf` (third-party paper PDFs) | Prefer links and citations rather than distributing PDF copies. | Review each item's redistribution terms. If already in Git history, a regular removal does not erase history. |
| Small analysis CSVs, manifests, generated plots | Usually suitable to publish when generated from your own runs and free of restrictive third-party data. | Confirm they do not contain bundled third-party data or personal identifiers. |
| Internal planning docs, personal notes, credentials, private paths/logs | Do not include in the portfolio release by default. | Inspect content before any removal or publishing. |

## Recommended documentation

- `docs/E1_REPRODUCIBILITY.md`: original experiment hashes and data provenance.
- `REPRODUCING.md`: verify summaries without running experiments, and prerequisites for full training.
- `docs/CONTRIBUTIONS.md`: two contributors and review of actual roles.
- `docs/REPOSITORY_CLEANUP_PLAN.md`: nondestructive cleanup sequence.

## Release gate

Before making `main` a clean public portfolio page, verify all of the following:

- Both contributors have reviewed credit and distribution terms for the code they wrote.
- Third-party PDF redistribution is assessed and unnecessary PDF blobs removed from the visible tree if permission is unclear.
- The exact provenance and copyright notices of the Model X-Ray submodule remain intact.
- Dataset and model zoo redistribution rules are documented; no raw zoo/checkpoint blobs are committed inadvertently.
- A fresh clone can at least verify published numeric summaries **without the raw dataset**.
- Any Git history cleanup is a separate, planned operation requiring agreement from collaborators; ordinary `git rm` only removes from the latest tree.
