from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _tracked(*patterns: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", *patterns],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def test_adr0010_wi2_output_artifacts_are_not_tracked() -> None:
    assert _tracked("output/**") == []


def test_adr0010_wi2_browser_evidence_artifacts_are_not_tracked() -> None:
    assert _tracked(
        ".pytest_tmp/**",
        "docs/acceptance/*browser-evidence.json",
        "docs/acceptance/*acceptance-evidence.json",
    ) == []


def test_adr0010_wi2_output_artifacts_are_ignored() -> None:
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "output/account_capability/future.json",
            ".pytest_tmp/future/source-package.json",
            "docs/acceptance/future-ui-browser-evidence.json",
            "docs/acceptance/future-ui-acceptance-evidence.json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
