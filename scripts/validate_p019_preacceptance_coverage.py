from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "pre-acceptance-coverage.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "pre-implementation-audit.md"
FOUNDATION = ROOT / "scripts" / "validate_p019_broker_observation_foundation.py"


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

    require("- Status: pre-acceptance partial" in coverage, "coverage closeout must remain partial")
    require("ADR-0005 is accepted" in coverage, "coverage must keep ADR acceptance as future requirement")
    require("does not authorize a direct Account Console broker observation session" in coverage, "coverage must not authorize direct session")

    for idx in range(1, 15):
        row_id = f"A{idx}"
        row = table_row_for(coverage, row_id)
        require("pre-acceptance partial" in row, f"{row_id} must remain pre-acceptance partial")
        require(row_id in acceptance, f"{row_id} must exist in acceptance matrix")

    for idx in range(1, 10):
        row_id = f"PRE-G{idx:02d}"
        row = table_row_for(coverage, row_id)
        require(row_id in audit, f"{row_id} must exist in pre-implementation audit")
        if row_id in {"PRE-G01", "PRE-G02"}:
            require("blocked by ADR" in row, f"{row_id} must stay blocked by ADR while ADR-0005 is proposed")
        else:
            require("pre-acceptance partial" in row, f"{row_id} must remain pre-acceptance partial")

    require_terms(
        COVERAGE,
        [
            "Funds and positions acceptance must come from an authorized TWS API login / owner runtime source / Account Mirror projection chain.",
            "Screenshots may confirm local operator/window state only",
            "they must not be used as funds truth, positions truth, account truth, execution report truth or trading-readiness evidence.",
            "positive per-currency funds evidence obtained through authorized TWS API / owner runtime source",
            "screenshot evidence is forbidden for funds and positions truth",
            "Funds and positions closeout requires TWS API / owner runtime source data",
            "Synthetic ready-path fixtures may prove contract mapping from TWS API query artifacts, normalized report batches and durable-store reload checkpoints into source packages and Account Mirror projections",
            "they cannot close real U3028269 funds parity, positions parity, real order/fill callback parity, UI parity, P018 owner source-package acceptance or ADR-0005 direct observation acceptance",
            "Synthetic ready-path fixtures are contract guards only",
            "P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=partial",
        ],
    )
    require_terms(
        ACCEPTANCE,
        [
            "pre-acceptance partial",
            "positive per-currency TWS parity remains required",
            "TWS U3028269 UI readback is compared against same-slice TWS/API/source data",
            "Screenshot evidence proves broker/account/order truth.",
        ],
    )
    require_terms(
        FOUNDATION,
        [
            "PREACCEPTANCE_COVERAGE",
            "P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=partial",
        ],
    )

    print("P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=partial")


if __name__ == "__main__":
    main()
