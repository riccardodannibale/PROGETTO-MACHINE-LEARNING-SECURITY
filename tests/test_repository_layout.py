#!/usr/bin/env python3
"""Check the lean submission layout and relative Markdown links."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")

required = (
    "README.md",
    "LICENSE",
    "report/final_report.md",
    "scripts/verify_published_results.py",
    "scripts/run_e2_paired_v0.py",
    "tests/test_verify_published_results.py",
    "tests/test_e2_g5_preflight.py",
    "tests/test_e2_g7_release_contract.py",
    "docs/E2_PROTOCOL_FROZEN.md",
    "docs/E2_G7_TEST_RELEASE_NOTICE.md",
    "docs/E2_G3_UTILITY_RESULTS.md",
    "docs/E2_PROTOCOL_FINAL_REVIEW.md",
    "manifests/e1_uniform_v1/splits.csv",
    "external/ModelXRay",
)
missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing required submission paths: " + ", ".join(missing))

# The frozen E2 protocol is a historical integrity record. Its references
# describe the original experiment-time layout and are intentionally not
# rewritten as part of the submission cleanup.
broken = []
for doc in ROOT.rglob("*.md"):
    if ".git" in doc.parts or "external" in doc.parts or doc.name == "E2_PROTOCOL_FROZEN.md":
        continue
    content = doc.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(content):
        target = match.group(1).strip().split()[0].strip("<>")
        parts = urlsplit(target)
        if parts.scheme or target.startswith("#") or not parts.path:
            continue
        path = Path(unquote(parts.path))
        resolved = path if path.is_absolute() else doc.parent / path
        if not resolved.exists():
            broken.append(f"{doc.relative_to(ROOT)} -> {target}")
if broken:
    raise SystemExit("Broken Markdown links:\n" + "\n".join(broken))

for path in (".github", "REPRODUCING.md", "docs/README.md", "docs/experimental_design.md",
             "docs/results_and_limitations.md", "docs/setup.md", "report/final_report.pdf",
             "report/final_report.docx", "results/analysis", "results/validation",
             "results/pilots", "tests/test_e2_g2_audit_helpers.py",
             "tests/test_e2_g3_utility_helpers.py", "tests/test_e2_g6_csv_roundtrip.py",
             "tests/test_e2_g7_audit_helpers.py", "tests/test_e2_spread_synthetic.py", "tests/test_e3_controls.py"):
    if (ROOT / path).exists():
        raise SystemExit(f"Redundant submission path remains: {path}")

print("SUBMISSION LAYOUT OK: essential files exist and relative Markdown links resolve")
