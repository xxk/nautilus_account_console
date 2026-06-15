from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PROPOSAL_FILES = ["README.md", "phase-plan.md", "acceptance.md"]
WORKFLOW_MANIFEST = Path("docs/workflows/proposal-gates/proposal_gate_manifest.yaml")
WORKFLOW_BOARD = Path("docs/workflows/proposal-gates/proposal_gate_board.md")
ROUTE_MATRIX = Path("docs/acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md")


class ProposalDocsError(Exception):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_exists(path: Path) -> None:
    if not path.exists():
        raise ProposalDocsError(f"missing required path: {path}")


def require_terms(path: Path, terms: list[str]) -> None:
    content = read_text(path)
    missing = [term for term in terms if term not in content]
    if missing:
        raise ProposalDocsError(f"{path} missing required terms: {', '.join(missing)}")


def iter_proposals(root: Path, proposal_id: str | None) -> list[Path]:
    proposals_dir = root / "docs" / "proposals"
    require_exists(proposals_dir)
    if proposal_id:
        proposal = proposals_dir / proposal_id
        require_exists(proposal)
        return [proposal]
    return sorted(
        path
        for path in proposals_dir.iterdir()
        if path.is_dir()
        and not path.name.startswith("_")
        and ((path / "phase-plan.md").exists() or (path / "acceptance.md").exists())
    )


def validate_workflow_contract(root: Path) -> None:
    manifest = root / WORKFLOW_MANIFEST
    board = root / WORKFLOW_BOARD
    require_exists(manifest)
    require_exists(board)
    require_terms(
        manifest,
        [
            "schema_id: account_console_proposal_workflow_stage_contract",
            "PG-S0-SCAFFOLD",
            "PG-S1-WORKFLOW-CONTRACT",
            "PG-S2-UI-DESIGN-ACCEPTANCE",
            "PG-S6-CLOSEOUT",
            "Proposal Gate must not write",
        ],
    )
    require_terms(
        board,
        [
            "Proposal Workflow Stage Contract Board",
            "PG-S0-SCAFFOLD",
            "PG-S2-UI-DESIGN-ACCEPTANCE",
            "UI design text cannot count as browser-render evidence",
        ],
    )


def validate_proposal(root: Path, proposal: Path) -> None:
    for filename in REQUIRED_PROPOSAL_FILES:
        require_exists(proposal / filename)

    readme = proposal / "README.md"
    phase_plan = proposal / "phase-plan.md"
    acceptance = proposal / "acceptance.md"

    require_terms(readme, ["Proposal ID", "Status"])
    require_terms(phase_plan, ["Proposal ID", "Status", "Phase"])
    require_terms(acceptance, ["Proposal ID", "Status"])

    readme_text = read_text(readme)
    acceptance_text = read_text(acceptance)
    is_ui_proposal = "UI design" in readme_text or "ui-design.md" in readme_text or "UI Anti-Drift" in acceptance_text
    if is_ui_proposal:
        require_exists(proposal / "ui-design.md")
        require_exists(proposal / "ui-acceptance.md")
        require_terms(proposal / "ui-design.md", ["Data Test ID"])
        require_terms(proposal / "ui-acceptance.md", ["Negative UI Acceptance", "Browser Acceptance", "Blocker"])
        require_terms(acceptance, ["UI Anti-Drift Acceptance", "forbidden_actions", "forbidden_claims"])
        require_exists(root / ROUTE_MATRIX)

    if "Owner Boundary:" in readme_text:
        require_terms(readme, ["write_authority", "forbidden", "second_implementation_rejected"])

    if "design_gate_ready" in readme_text or "design_gate_ready" in acceptance_text:
        require_terms(
            acceptance,
            [
                "Implementation/browser evidence",
                "required before implementation closeout",
            ],
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Account Console proposal docs.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--proposal-id", help="Validate one proposal directory")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    try:
        validate_workflow_contract(root)
        proposals = iter_proposals(root, args.proposal_id)
        for proposal in proposals:
            validate_proposal(root, proposal)
    except ProposalDocsError as exc:
        print(f"PROPOSAL_DOCS_ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"PROPOSAL_DOCS_OK: proposals={len(proposals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())