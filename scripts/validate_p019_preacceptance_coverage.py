from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "pre-acceptance-coverage.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "pre-implementation-audit.md"
ADR = ROOT / "docs" / "adr" / "0005-account-console-independent-broker-observation-sessions.md"


class PreacceptanceCoverageError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PreacceptanceCoverageError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_terms(path: Path, terms: list[str]) -> None:
    text = read(path)
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def table_row_for(text: str, row_id: str) -> str:
    pattern = re.compile(rf"^\| {re.escape(row_id)} \| (?P<row>.+)$", re.MULTILINE)
    match = pattern.search(text)
    require(match is not None, f"missing coverage row {row_id}")
    return match.group(0)


def main() -> None:
    coverage = read(COVERAGE)
    acceptance = read(ACCEPTANCE)
    audit = read(AUDIT)
    adr = read(ADR)

    require("decision_status: accepted" in adr, "ADR-0005 must now be accepted")
    require("- Status: accepted_with_residual_runtime_blockers" in acceptance, "P019 acceptance must be accepted")
    require("- Status: historical_pre_acceptance_retained" in coverage, "coverage doc must be historical retained")
    require("ADR-0005 is now accepted" in coverage, "coverage doc must acknowledge accepted ADR")

    for idx in range(1, 15):
        row_id = f"A{idx}"
        table_row_for(coverage, row_id)
        require(row_id in acceptance, f"{row_id} must exist in acceptance matrix")
    for idx in range(1, 10):
        row_id = f"PRE-G{idx:02d}"
        table_row_for(coverage, row_id)
        require(row_id in audit, f"{row_id} must exist in pre-implementation audit")

    for row_id in ["A5", "A13", "PRE-G06", "PRE-G08"]:
        row = table_row_for(coverage, row_id)
        require("execution_report_rows=0" in row or "zero execution rows" in row, f"{row_id} must retain zero-row term")
        require(
            "blocked" in row or "not report parity" in row or "non-empty" in row,
            f"{row_id} must retain blocker/non-parity term",
        )
    a11 = table_row_for(coverage, "A11")
    require("partial" in a11 and "blocked" in a11 and "no live memory" in a11, "A11 must retain durable partial/no-live-memory terms")

    require_terms(
        COVERAGE,
        [
            "Current real U3028269 TWS API evidence proves funds/positions collection and UI parity are ready",
            "Real `reqExecutions` success with zero rows must remain a typed empty-state blocker, not a real report parity pass.",
            "Durable reload from persisted artifacts with zero report rows must remain `partial` / `blocked`, not complete.",
            "P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=historical_retained",
        ],
    )
    require_terms(
        ACCEPTANCE,
        [
            "accepted_with_residual_runtime_blockers",
            "real U3028269 TWS API funds and positions render through Account Mirror with parity pass",
            "residual runtime blocker",
        ],
    )

    print("P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=historical_retained")


if __name__ == "__main__":
    main()
