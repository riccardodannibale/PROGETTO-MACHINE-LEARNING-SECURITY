# Reproducibility guide — Beyond the X-Ray (E1–E3)

This guide deliberately separates **verification of published numbers** from **re-execution of expensive experiments**. Reproducing the reported table does not imply that the entire dataset or checkpoint zoo can be redistributed.

## Level 0 — Verify published outputs without the dataset

From the project root (on `ricky` or the release branch containing E1–E3):

```bash
python3 scripts/verify_published_results.py
```

Only standard-library Python modules are required. Checks:

- E2 10 paired centroid AUROC rows per platform; ID, α=0.24, α=0.16 and signed deltas.
- Consistency with `results/e2_final/{ubuntu,mac_m4}/summary.csv`.
- Cross-platform paired table means versus its published summary.
- E3 10-fit group summaries on each platform, where available; balanced metadata and unchanged FPR across ID/OOD within platform.

**Not checked at this level:** re-scoring every raw prediction, TensorFlow model training, the original checkpoint's provenance or model-utility evaluation. The original G6/G7/E3 QA tools already cover these aspects on the source hosts.

For the historical E1 figures, if the E1 dependencies are installed and the versioned CSV paths are present:

```bash
"$HOME/mlsec-local/venvs/modelxray/bin/python" scripts/plot_e1_results.py
```

The E1 plotting entry point and inputs should be checked against [`docs/E1_REPRODUCIBILITY.md`](docs/E1_REPRODUCIBILITY.md) before attempting a new run.

## Level 1 — Re-check available source artifacts

The original experiment hosts have the complete local paths and raw scores. To audit E2 on Ubuntu **without re-training**, use the existing environment:

```bash
PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
"$PY" scripts/e2_g7_audit_test.py \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1"
```

To re-check E3 against the raw E2 scores, **choose a new, non-existing output directory**:

```bash
"$PY" scripts/e3_matched_controls.py \
  --platform ubuntu \
  --test-dir "$HOME/mlsec-local/runs/e2_test_official_ubuntu_v1" \
  --split-csv manifests/e1_uniform_v1/splits.csv \
  --out-dir "$HOME/mlsec-local/runs/e3_controls_verification_2"
```

On the Mac M4, use its actual Python path, local E2 test directory, and `--platform mac_m4`. These tools **read prior predictions and do not train**. Preserving the original E3 outputs is recommended.

## Level 2 — Full experiment recreation (requires data, time and permission)

Use the **recorded, pinned environment**, not a guessed modern `pip install` sequence. Historically, Ubuntu used Python 3.11 in `~/mlsec-local/venvs/modelxray/`; the Mac used a separately validated Apple M4 environment. The E1 documentation lists the Ubuntu dependency lock file under `configs/`.

The sources require:

1. Original GHRP/STL10 model zoo and checkpoint weights, acquired **from the original source** in accordance with dataset terms.
2. A provenance audit: `scripts/extract_d1_real_weights.py` creates `weights.npy` from **real checkpoint parameters**, not the image dataset `dataset.pt`; checkpoint deserialization uses restricted loading where supported.
3. `weights.npy` with **shape `(1000, 2864)`, dtype `float32`** and SHA-256 `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.
4. Split file with SHA-256 `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.
5. `external/ModelXRay` pinned to `a880e332f556fc71faf8d3753931005d5d019339`. Confirm upstream licensing and submodule initialization rather than copying its sources into your own MIT tree.
6. Exact experiment runner: E1 `scripts/run_e1_final_v2.py`, E2 `scripts/run_e2_paired_v0.py`, E3 `scripts/e3_matched_controls.py`.

**Safe preflight only, E2:**

```bash
PY="$HOME/mlsec-local/venvs/modelxray/bin/python"
"$PY" scripts/run_e2_paired_v0.py \
  --weights "$HOME/mlsec-local/datasets/ghrp_zoos/d1_uniform_real/weights.npy" \
  --split-dir manifests/e1_uniform_v1 \
  --out-dir "$HOME/mlsec-local/runs/e2_preflight_reproduction" \
  --stage preflight
```

This is **not a reproduction of the AUROC**. A full fit requires the historical frozen training protocol and separately gated test releases; do not casually re-open the previous test checkpoint identities after observing the results, and never select the best repeat.

### Why the results are not exactly bit-for-bit identical

Python/NumPy seeds, source manifests and payload generation are controlled. However, TensorFlow CPU kernels and different BLAS implementations can still yield slightly different learned weights and AUROC on Ubuntu x86_64 vs Mac ARM64. The published cross-platform comparison tests **statistical/experimental reproducibility**, not binary identity.

## Dataset and security policy

- The experiments used **only synthetic, inert payloads**. No executable malware has been embedded, activated or distributed.
- `dataset.pt` is original preprocessed STL10 **images and labels**, not the CNN parameter matrix.
- Never run `torch.load(..., weights_only=False)` on unknown checkpoint content.
- Do **not** publish the original downloaded zoo, large `.pt`/`.npy` checkpoints or transient embedding payload bytes without checking permissions.
- Do not silently broaden a report's claim from this synthetic experiment to real malware or all model architectures.

## Output interpretation

- AUROC is a **rank metric** and is independent of decision threshold.
- Youden FPR/TPR/FNR reported for E3 use thresholds **calibrated on LSB validation**, then held fixed for ID/OOD.
- Model pairs share a source identity. The 10 fit repetitions share the same 200 test checkpoint identities. Compute uncertainty with this correlation structure in mind; do not treat 2,000 repeated identities as independent test models.
- E3 is a **retrospective matched-control analysis** of E2 test scores, not a fresh blind holdout.

See [`docs/THIRD_PARTY_AND_DATA.md`](docs/THIRD_PARTY_AND_DATA.md) and [`docs/REPOSITORY_CLEANUP_PLAN.md`](docs/REPOSITORY_CLEANUP_PLAN.md).
