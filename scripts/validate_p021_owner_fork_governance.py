from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class P021GovernanceError(AssertionError):
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P021GovernanceError(message)


def validate_route_context_owner() -> None:
    route_context = ROOT / "backend" / "src" / "nautilus_account_console" / "route_context.py"
    source_bridge = ROOT / "backend" / "src" / "nautilus_account_console" / "source_bridge.py"
    account_mirror = ROOT / "backend" / "src" / "nautilus_account_console" / "account_mirror.py"
    require(route_context.exists(), "P021-I1: canonical route_context.py is missing")
    source_text = read(source_bridge)
    mirror_text = read(account_mirror)
    require("route_context_from_source_artifact" in source_text, "P021-I1: source_bridge must use canonical source route resolver")
    require("blocked_route_context" in source_text, "P021-I1: source_bridge must use canonical blocked route resolver")
    require("route_context_from_capability_bundle" in mirror_text, "P021-I1: account_mirror must use canonical bundle route resolver")
    require("_fallback_route_context" not in source_text, "P021-I1: source_bridge must not define fallback route_context")
    require("_fallback_route_context" not in mirror_text, "P021-I1: account_mirror must not define fallback route_context")
    require("_validate_route_context_impl" in source_text, "P021-I1: source_bridge must delegate validation to canonical route_context")
    require("RouteContextError" in source_text and "SourceBridgeError" in source_text, "P021-I1: source_bridge compatibility wrapper must preserve SourceBridgeError")
    require("def validate_route_context" not in mirror_text, "P021-I1: account_mirror must not duplicate route_context validation")


def validate_source_package_boundary() -> None:
    source_bridge = ROOT / "backend" / "src" / "nautilus_account_console" / "source_bridge.py"
    issue_list = ROOT / "docs" / "proposals" / "p021-account-console-owner-fork-governance" / "issue-list.md"
    owner_map = ROOT / "docs" / "ownership" / "account-console-owner-map.md"
    source_text = read(source_bridge)
    issue_text = read(issue_list)
    owner_text = read(owner_map)
    for name in [
        "CTP19053_REAL_SOURCE_PACKAGE",
        "CTP025292_REAL_SOURCE_PACKAGE",
        "IB_U3028269_SOURCE_PACKAGE",
    ]:
        require(name in source_text, f"P021-I2: expected source package ref {name} is missing")
    require("source_ref" in source_text and "checksum" in source_text, "P021-I2: source package refs must preserve source_ref and checksum")
    require("not Account Console-owned truth" in issue_text, "P021-I2: issue ledger must reject Account Console source ownership")
    require("external strategy/runtime owner" in owner_text, "P021-I2: owner map must anchor external source owner boundary")


def validate_synthetic_test_boundary() -> None:
    spec = ROOT / "frontend" / "tests" / "e2e" / "p019-ib-tws-synthetic-ready-projection.spec.ts"
    evidence = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json"
    text = read(spec)
    require("synthetic_contract_guard_not_account_truth" in text, "P021-I3: synthetic route context must not claim account truth")
    forbidden_truth_claims = [
        "capital_truth: true",
        "account_truth: true",
        "broker_truth: true",
        "runtime_truth: true",
    ]
    present = [claim for claim in forbidden_truth_claims if claim in text]
    require(not present, f"P021-I3: synthetic test has authority leakage {present}")
    require("expect(readyProjection.boundaries.account_truth).toBe(false)" in text, "P021-I3: synthetic test needs account_truth false assertion")
    require("expect(readyProjection.boundaries.capital_truth).toBe(false)" in text, "P021-I3: synthetic test needs capital_truth false assertion")
    if evidence.exists():
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        require(payload.get("verdict") == "synthetic_contract_only", "P021-I3: synthetic evidence verdict must stay synthetic-only")
        boundaries = payload.get("boundaries", {})
        require(boundaries.get("synthetic_contract_only") is True, "P021-I3: synthetic evidence must mark synthetic_contract_only")
        require(boundaries.get("broker_truth") is False, "P021-I3: synthetic evidence must not claim broker truth")


def validate_frontend_registry_boundary() -> None:
    tests_dir = ROOT / "frontend" / "tests"
    src_dir = ROOT / "frontend" / "src"
    readme = ROOT / "frontend" / "tests" / "README.md"
    readme_text = read(readme)
    require("No test file creates a second route registry" in readme_text, "P021-I4: frontend tests README must ban second route registry")
    production_text = "\n".join(read(path) for path in src_dir.glob("*.tsx"))
    require("frontend/tests" not in production_text, "P021-I4: production frontend must not import frontend/tests")
    forbidden_test_registry = re.compile(r"\b(createBrowserRouter|RouterProvider|routes\s*=|routeRegistry)\b")
    offenders = []
    for path in tests_dir.rglob("*.ts"):
        text = read(path)
        if forbidden_test_registry.search(text):
            offenders.append(str(path.relative_to(ROOT)))
    require(not offenders, f"P021-I4: tests must not create route registries: {offenders}")


def validate_p021_docs_closed() -> None:
    proposal = ROOT / "docs" / "proposals" / "p021-account-console-owner-fork-governance"
    for name in ["README.md", "phase-plan.md", "acceptance.md", "issue-list.md"]:
        require((proposal / name).exists(), f"P021 docs missing {name}")
    issue_text = read(proposal / "issue-list.md")
    require("Status | `closed`" in issue_text or "Status | `accepted_with_guardrails`" in issue_text, "P021 issues must include closed or guarded rows")
    require("Status | `open`" not in issue_text, "P021 issue-list must not retain open issues at closeout")


def main() -> int:
    validate_route_context_owner()
    validate_source_package_boundary()
    validate_synthetic_test_boundary()
    validate_frontend_registry_boundary()
    validate_p021_docs_closed()
    print("P021_OWNER_FORK_GOVERNANCE_OK: issues=4 route_context=canonical synthetic=guarded registry=single_owner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
