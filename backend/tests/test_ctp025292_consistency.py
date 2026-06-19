from pathlib import Path

from nautilus_account_console.ctp025292_consistency import (
    DEFAULT_SOURCE_PACKAGE,
    evaluate_ctp025292_source_package,
)


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_SOURCE = ROOT / "contracts" / "source_artifacts" / "samples" / "ctp_live_025292_sample_source.json"


def test_ctp025292_missing_default_source_package_blocks() -> None:
    result = evaluate_ctp025292_source_package(DEFAULT_SOURCE_PACKAGE)

    assert result.verdict == "blocked"
    assert result.blocker_id == "ctp025292_source_unavailable"
    assert result.command_disabled == "pass"


def test_ctp025292_sample_source_package_can_pass_harness() -> None:
    result = evaluate_ctp025292_source_package(SAMPLE_SOURCE)

    assert result.verdict == "passed"
    assert result.account_id == "acct.ctp.live.025292"
    assert result.source_ref.endswith("ctp_live_025292_sample_source.json")
    assert result.projection_checksum is not None
    assert result.funds_match == "pass"
    assert result.orders_match == "pass"
    assert result.command_disabled == "pass"
