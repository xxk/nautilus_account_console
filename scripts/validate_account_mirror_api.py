from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.main import app  # noqa: E402


def main() -> None:
    client = TestClient(app)

    response = client.get("/api/mirror/accounts")
    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == "account_mirror_list.v1"
    account_ids = {row["account_id"] for row in payload["accounts"]}
    assert account_ids == {
        "acct.nautilus.paper.demo",
        "acct.ctp.paper.19053",
        "acct.ctp.live.025292",
        "simulated-001",
    }

    detail = client.get("/api/mirror/accounts/acct.ctp.paper.19053")
    assert detail.status_code == 200
    detail_payload = detail.json()
    assert detail_payload["capabilities"]["command"]["enabled"] is False
    assert detail_payload["capabilities"]["command"]["mode"] == "disabled"
    assert detail_payload["source_health"]["state"] in {"ready", "blocked"}

    positions = client.get("/api/mirror/accounts/acct.ctp.paper.19053/positions")
    assert positions.status_code == 200
    if detail_payload["source_health"]["state"] == "ready":
        assert positions.json()[0]["source_ref"]
    else:
        assert positions.json() == []

    orders = client.get("/api/mirror/accounts/acct.ctp.paper.19053/orders")
    assert orders.status_code == 200
    if detail_payload["source_health"]["state"] == "ready" and orders.json():
        order_payload = orders.json()[0]
        assert order_payload["source_ref"]
        assert order_payload["report_provenance_ref"]
        assert order_payload["report_msg_ref"]
        assert order_payload["report_msg_checksum"].startswith("sha256:")
    else:
        assert orders.json() == []

    capabilities = client.get("/api/mirror/accounts/acct.ctp.paper.19053/capabilities")
    assert capabilities.status_code == 200
    assert capabilities.json()["command"]["enabled"] is False

    evidence = client.get("/api/mirror/accounts/acct.ctp.paper.19053/evidence")
    assert evidence.status_code == 200
    evidence_payload = evidence.json()
    assert evidence_payload["schema_version"] == "account_mirror_evidence.v1"
    assert evidence_payload["source_ref"].endswith("output/account_capability/ctp-paper-19053/source-package.json")
    assert evidence_payload["boundaries"]["order_action"] is False
    assert {item["kind"] for item in evidence_payload["evidence"]} >= {
        "source_package",
        "mirror_projection",
    }

    health = client.get("/api/mirror/accounts/acct.ctp.paper.19053/source-health")
    assert health.status_code == 200
    health_payload = health.json()
    assert health_payload["schema_version"] == "account_mirror_source_health.v1"
    assert health_payload["state"] in {"ready", "blocked"}
    assert health_payload["source_ref"].endswith("output/account_capability/ctp-paper-19053/source-package.json")
    assert health_payload["projection_checksum"].startswith("sha256:")

    blocked = client.get("/api/mirror/accounts/acct.ctp.live.025292")
    assert blocked.status_code == 200
    blocked_payload = blocked.json()
    assert blocked_payload["capabilities"]["command"]["enabled"] is False
    assert blocked_payload["blockers"][0]["type"] == "source_unavailable"

    simulated = client.get("/api/mirror/accounts/simulated-001")
    assert simulated.status_code == 200
    simulated_payload = simulated.json()
    assert simulated_payload["account_id"] == "simulated-001"
    assert simulated_payload["capabilities"]["command"]["enabled"] is False
    assert simulated_payload["boundaries"]["order_action"] is False
    health = simulated_payload["source_health"]
    assert health["account_uid"] == "sandbox-paper.simulated-001"
    assert health["account_type"] == "sandbox_paper"
    assert health["ledger_type"] == "simulated_sandbox_ledger"
    assert health["market_data_account_id"] == "025292"
    assert health["market_data_role"] == "market_data_only"
    assert health["execution_target"] == "Nautilus Sandbox Paper"
    assert health["orders_scope"] == "simulated ledger only"
    assert health["broker_order_submission"] is False
    assert health["trading_adapter"] == "disabled"
    assert health["account_console_writes_truth"] is False

    print("ACCOUNT_MIRROR_API_OK: accounts=4")


if __name__ == "__main__":
    main()
