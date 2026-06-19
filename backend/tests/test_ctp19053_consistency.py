from __future__ import annotations

import json

import pytest

from nautilus_account_console.ctp19053_consistency import (
    Ctp19053ConsistencyError,
    evaluate_ctp19053_source_package,
)
from nautilus_account_console.source_bridge import SourceBridgeError


def test_ctp19053_consistency_blocks_when_source_package_missing(tmp_path):
    result = evaluate_ctp19053_source_package(tmp_path / "missing.json")

    assert result.verdict == "blocked"
    assert result.blocker_id == "ctp19053_source_unavailable"
    assert result.command_disabled == "pass"


def test_ctp19053_consistency_accepts_sample_source_package(tmp_path):
    source = (
        {
            "schema_version": "account_source_artifact.v1",
            "artifact_id": "source.ctp.paper.19053.test",
            "account_id": "acct.ctp.paper.19053",
            "display_alias": "19053",
            "source_owner": "nautilus_ctp_adapter",
            "source_kind": "ctp_trader_api",
            "source_mode": "paper_observation",
            "account_domain": "paper",
            "observation_mode": "snapshot",
            "event_stream": "not_implemented",
            "trading_day": "2026-06-15",
            "query_window_id": "ctp19053.test.window.001",
            "query_started_at": "2026-06-15T00:00:00Z",
            "query_completed_at": "2026-06-15T00:00:01Z",
            "observed_at": "2026-06-15T00:00:01Z",
            "source_ref": "tmp/ctp19053/source-package.json",
            "source_checksum": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "balances": [
                {
                    "currency": "CNY",
                    "equity": 500000.0,
                    "available_cash": 420000.0,
                    "margin_used": 80000.0,
                    "frozen_cash": 0.0,
                    "position_profit": 0.0,
                }
            ],
            "positions": [
                {
                    "instrument": "rb2610",
                    "exchange": "SHFE",
                    "direction": "long",
                    "net_qty": 1,
                    "today_qty": 1,
                    "yesterday_qty": 0,
                    "available_qty": 1,
                    "frozen_qty": 0,
                    "avg_price": 3500.0,
                    "unrealized_pnl": 0.0,
                }
            ],
            "orders": [],
            "fills": [],
            "source_health": {
                "state": "ready",
                "lag_ms": 0,
                "observation_mode": "snapshot",
                "event_stream": "not_implemented",
            },
            "blockers": [],
        }
    )
    path = tmp_path / "source-package.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    result = evaluate_ctp19053_source_package(path)

    assert result.verdict == "passed"
    assert result.account_id == "acct.ctp.paper.19053"
    assert result.funds_match == "pass"
    assert result.positions_match == "pass"
    assert result.command_disabled == "pass"


def test_ctp19053_consistency_rejects_command_capability(tmp_path):
    source = {
        "schema_version": "account_source_artifact.v1",
        "account_id": "acct.ctp.paper.19053",
        "display_alias": "19053",
        "source_owner": "nautilus_ctp_adapter",
        "source_kind": "ctp_trader_api",
        "source_mode": "paper_observation",
        "account_domain": "paper",
        "observation_mode": "snapshot",
        "event_stream": "not_implemented",
        "trading_day": "2026-06-15",
        "query_window_id": "ctp19053.test.window.002",
        "query_started_at": "2026-06-15T00:00:00Z",
        "query_completed_at": "2026-06-15T00:00:01Z",
        "observed_at": "2026-06-15T00:00:01Z",
        "source_ref": "tmp/ctp19053/source-package.json",
        "source_checksum": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        "balances": [],
        "positions": [],
        "orders": [],
        "fills": [],
        "source_health": {"state": "ready"},
        "blockers": [],
        "command": {"enabled": True},
    }
    path = tmp_path / "source-package.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(SourceBridgeError):
        evaluate_ctp19053_source_package(path)


def test_ctp19053_consistency_rejects_sensitive_fields(tmp_path):
    source = {
        "schema_version": "account_source_artifact.v1",
        "account_id": "acct.ctp.paper.19053",
        "display_alias": "19053",
        "source_owner": "nautilus_ctp_adapter",
        "source_kind": "ctp_trader_api",
        "source_mode": "paper_observation",
        "account_domain": "paper",
        "observation_mode": "snapshot",
        "event_stream": "not_implemented",
        "trading_day": "2026-06-15",
        "query_window_id": "ctp19053.test.window.003",
        "query_started_at": "2026-06-15T00:00:00Z",
        "query_completed_at": "2026-06-15T00:00:01Z",
        "observed_at": "2026-06-15T00:00:01Z",
        "source_ref": "tmp/ctp19053/source-package.json",
        "source_checksum": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        "balances": [],
        "positions": [],
        "orders": [],
        "fills": [],
        "source_health": {"state": "ready"},
        "blockers": [],
        "session_password": "do-not-store",
    }
    path = tmp_path / "source-package.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(Ctp19053ConsistencyError):
        evaluate_ctp19053_source_package(path)
