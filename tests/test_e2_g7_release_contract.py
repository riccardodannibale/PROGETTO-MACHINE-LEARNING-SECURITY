"""Regression checks for the E2 test-release guard. Does not unblind anything."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/e2_g7_prepare_test_release.py"
RUNNER = ROOT / "scripts/run_e2_paired_v0.py"
NOTICE = ROOT / "docs/E2_G7_TEST_RELEASE_NOTICE.md"

script_tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
assert any(isinstance(node, ast.FunctionDef) and node.name == "prepare" for node in script_tree.body)
assert any(isinstance(node, ast.FunctionDef) and node.name == "committed_exact" for node in script_tree.body)

runner = RUNNER.read_text(encoding="utf-8")
assert "check_test_unlock" in runner
assert "approved_for_e2_test" in runner
assert "frozen_protocol_sha256" in runner
assert "--unblind-test" in runner

notice = NOTICE.read_text(encoding="utf-8")
assert "Approval: E2 test authorized" in notice
assert "10 new fits per platform" in notice
print("E2 G7 release-contract self-test passed: frozen runner and separate release record preserved")
