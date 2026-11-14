# E2 test release approval (G7)

**Approval: E2 test authorized — 22 October 2026.**

This approval is a separate record from the frozen validation protocol in `docs/E2_PROTOCOL_FROZEN.md`. It does not modify that file, its hash or the E2 runner (`scripts/run_e2_paired_v0.py`, SHA-256 `4719e6d947c5c5f7acba09f464ec0d2e5abf5182c642af8a063789ca217849ac`).

## Evidence reviewed before release

- **Ubuntu:** the ten official LSB validation fits had completed. The v2 audit passed with 10 fits, 40 metric records, 8,000 predictions and 2,030 payload-manifest records. No test scores had been examined. Mean centroid validation AUROC was 0.88170875 (SD 0.08349493).
- **Mac M4:** after the CSV round-trip parser check, the reported diagnostic found three mismatches with the default parser and zero with round-trip parsing. The v2 audit was reported as passed with 10 fits, 40 metric records, 8,000 predictions and 2,030 payload-manifest records. The reported mean centroid validation AUROC was approximately 0.88183.
- **Approvals:** Riccardo approved proceeding after the Ubuntu audit. Fabrizio approved the protocol and requested the ID/OOD test release after the Mac audit. These approvals were communicated in messages on 22 October 2026; this record is not a digital signature. Mac audit evidence is reported by the operator and was not independently inspected from raw prediction files in the shared archive.

## Fixed scope of the test

1. Run **10 new fits per platform**. Each fit trains on three benign and three X-LSB X=23 training examples and calibrates only on the 200 LSB validation identities.
2. For each fit, use the same fitted model to score the 200 test identities under benign/LSB ID and benign/spread OOD alpha=0.24 (primary) and alpha=0.16 (secondary).
3. The primary metric is `AUROC_centroid(SPREAD_0.24) - AUROC_centroid(LSB_ID)`, paired by repeat on the same 200 source identities.
4. Preserve per-checkpoint predictions and thresholds, payload records, manifests, logs and integrity checks. Do not tune parameters or select repeats using test scores.
5. Do not selectively repeat completed fits. If an error occurs, stop, preserve the log and document any required amendment.
6. This is an internal test on the GHRP/STL10 collection already used in E1. It is not a new external blind holdout and it is not the original MaleficNet implementation. Payload capacity and perturbation magnitude are not matched.

The approval does not authorize further optimization on test data, changes to the embedding method or additional experiments. Each platform must create its own local machine-readable test-release file only after passing the local ten-fit validation audit. That JSON file is an execution record, not a cryptographic signature.
