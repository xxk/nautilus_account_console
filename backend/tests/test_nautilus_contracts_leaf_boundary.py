"""Cross-repo import guard for ADR-A59 / P213 (nautilus_strategies).

A59/P213 extracted the shared portfolio/signal/lens domain contracts out of
``nautilus_strategies`` into the leaf package ``nautilus_contracts``. Account
Console is a downstream consumer. The Phase 3b inventory found it imports
**none** of the moved contracts (only a JSON fixture and an owner-map doc
mention ``strategies.vnpy_portfolio`` as a string), consistent with its
read-only boundary. Phase 3b is therefore a verified no-op here.

This guard locks that no-op from Account Console's own gate (A59 §4.7 / §5.2.2:
cross-repo completion must be proven by the counterpart repo's own import
guard). If Account Console ever needs one of these contracts it must import it
from ``nautilus_contracts``, never from the retired ``strategies.*`` paths.
"""

from __future__ import annotations

import ast
from pathlib import Path

# backend/tests/<this file> -> backend/src/nautilus_account_console
_SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

# Contract modules that moved to the nautilus_contracts leaf (A59/P213).
_RETIRED_CONTRACT_MODULES = (
    "strategies.vnpy_portfolio.contracts.specs",
    "strategies.vnpy_portfolio.contracts.lens",
    "strategies.vnpy_portfolio.contracts._parse_helpers",
    "strategies.shared.contracts.selection_mode_contract",
    "strategies.shared.contracts.signal_rule_contract",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_account_console_does_not_import_retired_nautilus_strategies_contracts() -> None:
    offenders: list[str] = []
    if _SRC_ROOT.is_dir():
        for path in _SRC_ROOT.rglob("*.py"):
            for module in _imported_modules(path):
                if module.startswith(_RETIRED_CONTRACT_MODULES):
                    offenders.append(f"{path.relative_to(_SRC_ROOT)} -> {module}")
    assert offenders == [], (
        "Account Console must consume A59/P213 domain contracts from "
        "nautilus_contracts, not the retired strategies.* contract paths: "
        + "; ".join(offenders)
    )  # [CONTRACT-LOCK: A59/P213 Phase 3b — Account Console uses nautilus_contracts; retired strategies contract paths forbidden]
