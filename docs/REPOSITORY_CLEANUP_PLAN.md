# Repository cleanup — nondestructive release plan

**Objective:** turn the existing E1–E3 research work into a coherent public portfolio and exam artifact **without breaking frozen provenance checks**.

## Known versus not yet verified

A provided **16 October 2026 historical repository snapshot** shows `main` with only the top-level `LICENSE` and `ricky` with early working files. This is **not proof** that the live `main` branch is still unchanged. The latest `ricky` E1–E3 artifact commit reported in the conversation is `3ef84f7` (22 October 2026). Since direct live GitHub tree access was unavailable, always run `python3 scripts/audit_repository.py` and inspect `git fetch` output in the authoritative local clone before editing or merging.

## Classification — what to keep, what to archive, what to avoid shipping

| Area | Recommendation | Reason |
|---|---|---|
| `.gitmodules` and `external/ModelXRay` | **KEEP intact**, upstream pinned at commit `a880e332...`. | Third-party source provenance and frozen import paths. |
| `scripts/run_e1_final_v2.py`, `scripts/run_e2_paired_v0.py`, `scripts/e2_synthetic_spread.py` | **KEEP exact path and SHA-256**. | Runners and auditors verify hashes; moving, editing or renaming breaks frozen experiments. |
| Other `scripts/e2_*`, `scripts/e3_*`, QA scripts and `tests/` | **KEEP**; describe core tools and audits by category in docs. | Provenance, reproducibility and history of important controls. |
| `manifests/e1_uniform_v1/` | **KEEP unchanged**. | Checkpoint split and dataset hashes. |
| `configs/` and applicable dependency locks | **KEEP**; state platform differences. | Environment reproduction. |
| `results/test`, `results/validation`, `results/replicas`, `results/figures` from E1 (if present) | **KEEP** selected official small CSV/plots. | E1 evidence; preserve audit artifacts. |
| `results/e2_final`, `results/e3_final` | **KEEP**. | Official E2/E3 summaries, matched per-fit data and cross-platform figures. |
| `exam/E1_REPORT.*`, `exam/PROJECT_REPORT.*`, `exam/E3_REPORT.md` | **KEEP**. | Historical E1 version and final course report. |
| Frozen `docs/E2_PROTOCOL_FROZEN.md`, experiment QA reports | **KEEP**. | Provenance and no post-test tuning. |
| Numerous `README_E2_G*_*.md`, `README_G3_FORWARD.md`, `TEST_STATUS.md`, handoff messages, duplicated protocol reviews | **REVIEW** and **ARCHIVE** selectively under `docs/archive/` only after checking no scripts link to them. | Keep audit trail without overwhelming root. No automatic deletion. |
| `docs/references/*.pdf` and copied external works | **RIGHTS REVIEW**; replace with bibliographic links when permitted. | Third-party copyright and distribution conditions. |
| `*.pt`, `*.npy`, `*.bin`, large model data, transient logs, `~/mlsec-local/runs` | **DO NOT ADD** to public release by default. | Size, security, data licenses, accidental credentials. |
| Personal notes, backups, `cp` empty file, ad hoc ZIP packages | **LOCAL ONLY**, after checking ownership and use. | Not part of reproducible final code. |

**Do not** execute `git clean -fd`, `git reset --hard`, force push, rewrite history or perform bulk `mv` on frozen experiment entry points as a cleanup shortcut.

## Suggested final layout (mostly preserve working paths)

```text
README.md                     # Portfolio entry point (new, curated)
REPRODUCING.md                # Verification levels and data prerequisites (new)
LICENSE                       # Existing project text: credit/compatibility review required
.gitignore                    # Existing rules; do not blindly overwrite
.gitmodules                   # Genuine upstream submodule, if configured
external/ModelXRay/           # Pinned dependency
configs/                      # Platform locks
manifests/e1_uniform_v1/      # Split hash, protocol, CSV
scripts/                      # Stable E1/E2/E3 entry points and audits
 tests/                       # Regression checks
results/                      # Official E1/E2/E3 metrics and figures
exam/                         # Full E1+E2+E3 report and preserved E1 history
docs/
  E1_REPRODUCIBILITY.md
  E2_PROTOCOL_FROZEN.md
  E2_G7_FINAL_RESULTS.md
  THIRD_PARTY_AND_DATA.md
  CONTRIBUTIONS.md
  REPOSITORY_CLEANUP_PLAN.md
  archive/                     # optional, AFTER path/reference review
```

## Recommended Git workflow (Riccardo + Fabrizio)

1. **Read-only inventory** on both machines before changing branches:

   ```bash
   git fetch origin
   git branch -avv
   git status --short
   git ls-remote --symref origin HEAD
   git log -1 --oneline origin/main
   git log -1 --oneline origin/ricky
   python3 scripts/audit_repository.py
   ```

   Stop if a path is missing or if there are unstaged local changes to protect.

2. **Branch from the known E1–E3 work** (not old `main`):

   ```bash
   git switch ricky
   git switch -c chore/portfolio-release
   ```

   If the branch already exists, inspect it rather than blindly recreate it.

3. **Apply only curated Markdown + read-only audit scripts** from this package; inspect diff:

   ```bash
   git diff -- README.md REPRODUCING.md docs/ scripts/audit_repository.py scripts/verify_published_results.py
   python3 scripts/verify_published_results.py
   python3 scripts/audit_repository.py
   ```

4. **Commit selectively** and push the review branch:

   ```bash
   git add README.md REPRODUCING.md docs/THIRD_PARTY_AND_DATA.md docs/CONTRIBUTIONS.md docs/REPOSITORY_CLEANUP_PLAN.md \
     scripts/audit_repository.py scripts/verify_published_results.py
   git diff --cached --check
   git diff --cached --stat
   git commit -m "docs: curate E1-E3 portfolio and reproducibility entry points"
   git push -u origin chore/portfolio-release
   ```

5. **Fabrizio reviews** especially authorship, README claims, Mac numbers, existing copyright notices, links and reproducibility instructions. Use a pull request **base `main`, compare `chore/portfolio-release`** when ready, and verify the PR file diff and whether `main` has diverged. Do **not** force-push `main`; resolve conflicts through normal review. If a release is to be kept separate from the shared project, agree that choice in advance.

6. After acceptance, verify default branch/readme appearance from a **fresh clone**, then tag the accepted commit **only after** the actual branch has been finalized.

## Acceptable definition of done

- GitHub `main` displays a readable README with scientific claims and limitations, and links are not broken.
- E1/E2/E3 tables and figures are findable in ≤2 clicks; both contributors are credited.
- `scripts/verify_published_results.py` succeeds on a clean clone **without dataset**.
- Reproduction documentation clearly distinguishes (a) precomputed-summary verification (b) audit with locally retained prediction scores (c) fresh training requiring original weights.
- All frozen experiments remain unchanged and original hashes are stable.
- No unsupported claim about real malware, architecture shift, attack equivalence or external untouched holdout.
- Third-party rights are reviewed and no unauthorized datasets/papers are blindly redistributed.
- The professors' required deliverable format and timing have been verified separately from this technical plan.
