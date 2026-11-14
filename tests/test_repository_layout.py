#!/usr/bin/env python3
"""Check repository links and paths used by the frozen experiment records."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?[[^]]*\]\(([^)]+)\)")

required = (
    "README.md",
    "REPRODUCING.md",
    "report/final_report.md",
    "scripts/verify_published_results.py",
    "scripts/run_e2_paired_v0.py",
    "tests/test_e2_g7_release_contract.py",
    "docs/E2_PROTOCOL_FROZEN.md",
    "docs/E2_G7_TEST_RELEASE_NOTICE.md",
    # Historical source paths cited by the frozen E2 record.
    "docs/E2_G3_UTILITY_RESULTS.md",
    "docs/E2_PROTOCOL_FINAL_REVIEW.md",
    "docs/data_and_licensing.md",
    "external/ModelXRay",
)

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing required repository paths: " + ", ".join(missing))

broken = []
for doc in ROOT.rglob("*.md"):
    if ".git" in doc.parts or "external" in doc.parts:
        continue
    text = doc.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip().split()[0].strip("<>")
        parts = urlsplit(target)
        if parts.scheme or target.startswith("#") or not parts.path:
            continue
        target_path = Path(unquote(parts.path))
        resolved = target_path if target_path.is_absolute() else (doc.parent / target_path)
        if not resolved.exists():
            broken.append(f"{doc.relative_to(ROOT)} -> {target}")

if broken:
    raise SystemExit("Broken Markdown links:\n" + "\n".join(broken))

duplicates = (
    "docs/EXPERIMENTAL_DESIGN.md",
    "docs/RESULTS_AND_LIMITATIONS.md",
    "docs/SETUP.md",
    "docs/THIRD_PARTY_AND_DATA.md",
    "docs/e1_platform_audit.md",
    "docs/e2_final_results.md",
    "docs/e3_controls_protocol.md",
    "docs/e3_cross_platform.md",
)
present = [p for p in duplicates if (ROOT / p).exists()]
if present:
    raise SystemExit("Duplicate documentation files remain: " + ", ".join(present))

print("REPOSITORY LAYOUT CHECK OK: required paths and Markdown links exist")
