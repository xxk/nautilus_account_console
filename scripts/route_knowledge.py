#!/usr/bin/env python3
"""Route a problem description to minimal Account Console knowledge cards."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


FORBIDDEN_OUTPUT_KEYS = {"verdict", "acceptance", "ready", "admitted", "can_trade", "pass", "closeout"}


def load_router(root: Path) -> dict:
    path = root / "docs/knowledge/blocker-routing.json"
    return json.loads(path.read_text(encoding="utf-8"))


def target_is_file(root: Path, target: str) -> bool:
    path = Path(target)
    if not path.is_absolute():
        path = root / path
    return path.is_file()


def match_rules(router: dict, query: str) -> list[dict]:
    q = query.lower()
    matches = []
    for rule in router.get("rules", []):
        triggers = [str(item).lower() for item in rule.get("when", [])]
        if any(trigger in q for trigger in triggers):
            matches.append(rule)
    return matches


def validate_rule(root: Path, rule: dict) -> str | None:
    leaked = FORBIDDEN_OUTPUT_KEYS & set(rule)
    if leaked:
        return f"route_smoke_verdict_forbidden: {rule.get('id')} has {sorted(leaked)}"
    for target in rule.get("read", []) + rule.get("shared_patterns", []):
        if target.endswith("/") or target.endswith("\\"):
            return f"route_smoke_target_drift: {rule.get('id')} points to directory {target}"
        if not target_is_file(root, target):
            return f"route_smoke_target_drift: {rule.get('id')} missing target {target}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--query", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    router = load_router(root)
    matches = match_rules(router, args.query)
    if not matches:
        payload = {
            "status": "no_match",
            "message": "Continue from current task truth; do not fall back to full-library read.",
            "read": [],
        }
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print("ROUTE_KNOWLEDGE_NO_MATCH: read=0 action=current_task_truth")
        return 0

    read_targets: list[str] = []
    output = []
    for rule in matches:
        error = validate_rule(root, rule)
        if error:
            print(f"ROUTE_KNOWLEDGE_ERROR: {error}", file=sys.stderr)
            return 1
        targets = list(rule.get("read", [])) + list(rule.get("shared_patterns", []))
        read_targets.extend(targets)
        output.append(
            {
                "id": rule.get("id"),
                "family": rule.get("family"),
                "read": targets,
                "must_not": rule.get("must_not", []),
                "owner_boundary": rule.get("owner_boundary"),
                "gate": rule.get("gate"),
            }
        )

    # Deduplicate while preserving order.
    read_targets = list(dict.fromkeys(read_targets))
    payload = {"status": "matched", "matches": output}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"ROUTE_KNOWLEDGE_OK: matches={len(matches)} cards={len(read_targets)}")
        for target in read_targets:
            print(f"READ {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
