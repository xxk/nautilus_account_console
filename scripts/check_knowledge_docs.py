#!/usr/bin/env python3
"""Validate Account Console project-local knowledge docs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


REQUIRED_FILES = [
    "docs/knowledge/README.md",
    "docs/knowledge/00-dashboard.md",
    "docs/knowledge/project-playbook.md",
    "docs/knowledge/blocker-routing.json",
    "docs/knowledge/owner-boundaries.md",
    "docs/knowledge/account-console-read-model-boundary.md",
    "docs/knowledge/ui-projection-boundary.md",
    "docs/knowledge/runtime-secret-boundary.md",
    "docs/knowledge/adoption-note.md",
    "docs/knowledge/bug-ledger/README.md",
    "docs/knowledge/bug-ledger/KB-BUG-0001__readiness-claim-leaked-into-readonly-console.md",
    "docs/knowledge/bug-ledger/KB-BUG-0002__raw-report-treated-as-account-truth.md",
    "docs/knowledge/templates/bug-card.md",
]

BUG_REQUIRED_FRONTMATTER = {
    "id",
    "type",
    "scope",
    "area",
    "status",
    "source_ref",
    "prevention_gate",
    "shared_pattern_ref",
}

BUG_REQUIRED_SECTIONS = [
    "## Symptom",
    "## Trigger",
    "## Root Cause",
    "## Correct Action",
    "## Wrong Action",
    "## Prevention Gate",
    "## Source Ref",
]

FORBIDDEN_STATE_FIELDS = {
    "current_task",
    "acceptance_status",
    "ready",
    "admitted",
    "can_trade",
    "capital_status",
    "blocker_closed",
}

FORBIDDEN_ROUTE_FIELDS = {
    "verdict",
    "acceptance",
    "ready",
    "admitted",
    "can_trade",
    "pass",
    "closeout",
}

FORBIDDEN_PATTERNS = [
    ("knowledge_secret_or_runtime_leak", re.compile(r"\b(password|auth\s*code|api\s*key|account\s*secret|broker\s*secret)\s*[:=]\s*\S+", re.I)),
    ("knowledge_secret_or_runtime_leak", re.compile(r"\b(raw\s*endpoint|raw\s*front|front\s*address)\s*[:=]\s*\S+", re.I)),
    ("knowledge_secret_or_runtime_leak", re.compile(r"\b(order\s*insert|placeOrder|cancelOrder)\b", re.I)),
    ("knowledge_truth_source_drift", re.compile(r"\b(status|verdict|state|claim)\s*[:=]\s*(ready|admitted|can\s+trade|trading\s+readiness|pass|passed)\b", re.I)),
    ("knowledge_truth_source_drift", re.compile(r"\b(acceptance_status|current_task|blocker_closed)\s*[:=]", re.I)),
]

STATUS_WORDING = re.compile(r"\b(Paper ready|Live ready|can trade|admitted)\b", re.I)


class CheckError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        raise CheckError("bug_card_contract_violation", f"{path} missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise CheckError("bug_card_contract_violation", f"{path} has unterminated YAML frontmatter")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise CheckError("bug_card_contract_violation", f"{path} has invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def check_required_files(root: Path) -> None:
    for item in REQUIRED_FILES:
        path = root / item
        if not path.is_file():
            raise CheckError("knowledge_required_file_missing", item)


def check_dashboard(root: Path) -> None:
    text = read_text(root / "docs/knowledge/00-dashboard.md")
    for line in text.splitlines():
        if STATUS_WORDING.search(line) and "does not report" not in line:
            raise CheckError("knowledge_dashboard_status_drift", line.strip())


def check_forbidden_content(root: Path) -> None:
    for path in (root / "docs/knowledge").rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json"}:
            continue
        text = read_text(path)
        for code, pattern in FORBIDDEN_PATTERNS:
            match = pattern.search(text)
            if match:
                raise CheckError(code, f"{rel(root, path)} contains forbidden pattern: {match.group(0)}")


def ensure_file_target(root: Path, target: str, code: str) -> None:
    if target.endswith("/") or target.endswith("\\"):
        raise CheckError("route_directory_target_forbidden", target)
    path = Path(target)
    if not path.is_absolute():
        path = root / path
    if path.is_dir():
        raise CheckError("route_directory_target_forbidden", target)
    if not path.is_file():
        raise CheckError(code, target)


def check_router(root: Path) -> None:
    path = root / "docs/knowledge/blocker-routing.json"
    data = json.loads(read_text(path))
    if data.get("scope") != "project-local":
        raise CheckError("route_schema_invalid", "scope must be project-local")
    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        raise CheckError("route_schema_invalid", "rules must be non-empty")

    families = {rule.get("family") for rule in rules}
    expected = {"readiness-wording", "raw-report-truth", "secret-runtime-material", "owner-boundary-confusion"}
    missing = expected - families
    if missing:
        raise CheckError("route_schema_invalid", f"missing route families: {sorted(missing)}")

    for rule in rules:
        if not isinstance(rule, dict):
            raise CheckError("route_schema_invalid", "route rule must be object")
        for key in ["id", "when", "read", "must_not", "gate", "owner_boundary"]:
            if key not in rule or rule[key] in ("", [], None):
                raise CheckError("route_rule_underconstrained", f"{rule.get('id', '<missing>')} missing {key}")
        forbidden = FORBIDDEN_ROUTE_FIELDS & set(rule)
        if forbidden:
            raise CheckError("router_verdict_forbidden", f"{rule['id']} has forbidden fields {sorted(forbidden)}")
        for target in rule.get("read", []):
            ensure_file_target(root, target, "route_target_missing_or_unbounded")
        for target in rule.get("shared_patterns", []):
            ensure_file_target(root, target, "route_target_missing_or_unbounded")
        if "docs/knowledge" in rule.get("read", []):
            raise CheckError("route_directory_target_forbidden", rule["id"])


def check_bug_cards(root: Path) -> None:
    cards = sorted((root / "docs/knowledge/bug-ledger").glob("KB-BUG-*.md"))
    if len(cards) < 2:
        raise CheckError("bug_card_contract_violation", "at least two seed bug cards required")
    for path in cards:
        meta, body = parse_frontmatter(path)
        missing = BUG_REQUIRED_FRONTMATTER - set(meta)
        if missing:
            raise CheckError("bug_card_contract_violation", f"{rel(root, path)} missing {sorted(missing)}")
        leaked = FORBIDDEN_STATE_FIELDS & set(meta)
        if leaked:
            raise CheckError("knowledge_frontmatter_state_leak", f"{rel(root, path)} has {sorted(leaked)}")
        if meta.get("type") != "bug" or meta.get("scope") != "project-local":
            raise CheckError("bug_card_contract_violation", f"{rel(root, path)} invalid type/scope")
        for section in BUG_REQUIRED_SECTIONS:
            if section not in body:
                raise CheckError("bug_card_contract_violation", f"{rel(root, path)} missing section {section}")


def check_text_boundaries(root: Path) -> None:
    readme = read_text(root / "docs/knowledge/README.md")
    playbook = read_text(root / "docs/knowledge/project-playbook.md")
    adoption = read_text(root / "docs/knowledge/adoption-note.md")
    combined = f"{readme}\n{playbook}"
    bad_default = re.compile(r"read\s+(all|whole).*(knowledge-common|docs/knowledge).*before\s+every\s+task", re.I | re.S)
    if bad_default.search(combined):
        raise CheckError("full_library_read_default_forbidden", "default full-library read instruction found")
    if "current task truth" not in combined.lower():
        raise CheckError("agent_precedence_inversion", "current task truth precedence missing")
    if "must not copy Account Console owner facts" not in adoption:
        raise CheckError("project_fact_copy_forbidden", "adoption note must forbid copying Account Console facts")
    if ".obsidian" in combined and "read-only" not in combined.lower():
        raise CheckError("obsidian_truth_source_forbidden", "Obsidian mentioned without read-only boundary")


def run_checks(root: Path) -> None:
    check_required_files(root)
    check_dashboard(root)
    check_router(root)
    check_bug_cards(root)
    check_text_boundaries(root)
    check_forbidden_content(root)


def write_fixture(root: Path, rel_path: str, content: str) -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_minimal_valid_tree(src: Path, dst: Path) -> None:
    for rel_file in REQUIRED_FILES:
        source = src / rel_file
        target = dst / rel_file
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(read_text(source), encoding="utf-8")


def expect_failure(src_root: Path, mutate, expected_code: str) -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        copy_minimal_valid_tree(src_root, root)
        mutate(root)
        try:
            run_checks(root)
        except CheckError as exc:
            if exc.code != expected_code:
                raise CheckError("knowledge_negative_fixture_failed", f"expected {expected_code}, got {exc}") from exc
            return
        raise CheckError("knowledge_negative_fixture_failed", f"expected {expected_code}, got pass")


def run_selftest(root: Path) -> None:
    def nf1(tmp: Path) -> None:
        data = json.loads(read_text(tmp / "docs/knowledge/blocker-routing.json"))
        data["rules"][0]["read"] = ["docs/knowledge/"]
        write_fixture(tmp, "docs/knowledge/blocker-routing.json", json.dumps(data, indent=2))

    def nf2(tmp: Path) -> None:
        data = json.loads(read_text(tmp / "docs/knowledge/blocker-routing.json"))
        data["rules"][0]["verdict"] = "pass"
        write_fixture(tmp, "docs/knowledge/blocker-routing.json", json.dumps(data, indent=2))

    def nf3(tmp: Path) -> None:
        path = tmp / "docs/knowledge/bug-ledger/KB-BUG-0001__readiness-claim-leaked-into-readonly-console.md"
        text = read_text(path).replace("status: active\n", "status: active\nacceptance_status: passed\n")
        path.write_text(text, encoding="utf-8")

    def nf4(tmp: Path) -> None:
        path = tmp / "docs/knowledge/runtime-secret-boundary.md"
        path.write_text(read_text(path) + "\npassword: secret123\n", encoding="utf-8")

    def nf5(tmp: Path) -> None:
        path = tmp / "docs/knowledge/00-dashboard.md"
        path.write_text(read_text(path) + "\n| Current | Paper ready |\n", encoding="utf-8")

    def nf6(tmp: Path) -> None:
        path = tmp / "docs/knowledge/bug-ledger/KB-BUG-0002__raw-report-treated-as-account-truth.md"
        text = read_text(path).replace("source_ref: docs/adr/0004-adopt-account-mirror-observation-and-command-plane.md\n", "")
        path.write_text(text, encoding="utf-8")

    def nf7(tmp: Path) -> None:
        path = tmp / "docs/knowledge/README.md"
        path.write_text(read_text(path) + "\nAI should read all knowledge-common before every task.\n", encoding="utf-8")

    def nf8(tmp: Path) -> None:
        path = tmp / "docs/knowledge/adoption-note.md"
        text = read_text(path).replace("They must not copy Account Console owner facts", "They should copy Account Console owner facts")
        path.write_text(text, encoding="utf-8")

    fixtures = [
        (nf1, "route_directory_target_forbidden"),
        (nf2, "router_verdict_forbidden"),
        (nf3, "knowledge_frontmatter_state_leak"),
        (nf4, "knowledge_secret_or_runtime_leak"),
        (nf5, "knowledge_dashboard_status_drift"),
        (nf6, "bug_card_contract_violation"),
        (nf7, "full_library_read_default_forbidden"),
        (nf8, "project_fact_copy_forbidden"),
    ]
    for mutate, code in fixtures:
        expect_failure(root, mutate, code)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        run_checks(root)
        if args.selftest:
            run_selftest(root)
    except CheckError as exc:
        print(f"KNOWLEDGE_DOCS_ERROR: {exc}", file=sys.stderr)
        return 1
    print("KNOWLEDGE_DOCS_OK: files=13 routes=4 bug_cards=2 negative_fixtures=8" if args.selftest else "KNOWLEDGE_DOCS_OK: files=13 routes=4 bug_cards=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
