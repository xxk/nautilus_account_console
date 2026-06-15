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
    ready_accounts = ["acct.nautilus.paper.demo", "simulated-001"]
    blocked_accounts = ["acct.ctp.paper.19053", "acct.ctp.live.025292"]

    for account_id in ready_accounts:
        health = client.get(f"/api/mirror/accounts/{account_id}/source-health")
        assert health.status_code == 200, account_id
        health_payload = health.json()
        assert health_payload["schema_version"] == "account_mirror_source_health.v1", account_id
        assert health_payload["state"] == "ready", account_id
        assert health_payload["source_ref"], account_id
        assert health_payload["source_checksum"].startswith("sha256:"), account_id
        assert health_payload["projection_checksum"].startswith("sha256:"), account_id
        assert health_payload["boundaries"]["order_action"] is False, account_id
        if account_id == "simulated-001":
            assert health_payload["state"] == "ready", account_id
            assert health_payload["blockers"][0]["type"] == "fixture_only_read_model", account_id
            assert health_payload["blockers"][0]["blocker_id"] == "simulated001_stage2_fixture_only", account_id

        evidence = client.get(f"/api/mirror/accounts/{account_id}/evidence")
        assert evidence.status_code == 200, account_id
        evidence_payload = evidence.json()
        assert evidence_payload["schema_version"] == "account_mirror_evidence.v1", account_id
        kinds = {item["kind"] for item in evidence_payload["evidence"]}
        assert "source_package" in kinds, account_id
        assert "mirror_projection" in kinds, account_id
        for item in evidence_payload["evidence"]:
            assert item["owner"], (account_id, item)
            assert item["source_ref"], (account_id, item)
            assert item["checksum"].startswith("sha256:"), (account_id, item)
            assert (
                "truth" in item["authority"]
                or "projection" in item["authority"]
                or ("fail closed" in item["authority"] and item["kind"] == "typed_blocker")
            ), (account_id, item)
        assert evidence_payload["boundaries"]["read_only_projection"] is True, account_id
        assert evidence_payload["boundaries"]["broker_truth"] is False, account_id
        assert evidence_payload["boundaries"]["order_action"] is False, account_id
        if account_id == "simulated-001":
            kinds = {item["kind"] for item in evidence_payload["evidence"]}
            assert "typed_blocker" in kinds, account_id
            assert evidence_payload["blockers"][0]["type"] == "fixture_only_read_model", account_id

    for account_id in blocked_accounts:
        health = client.get(f"/api/mirror/accounts/{account_id}/source-health")
        assert health.status_code == 200, account_id
        health_payload = health.json()
        assert health_payload["schema_version"] == "account_mirror_source_health.v1", account_id
        assert health_payload["state"] == "blocked", account_id
        assert health_payload["blockers"], account_id
        assert health_payload["boundaries"]["order_action"] is False, account_id

        evidence = client.get(f"/api/mirror/accounts/{account_id}/evidence")
        assert evidence.status_code == 200, account_id
        evidence_payload = evidence.json()
        assert evidence_payload["schema_version"] == "account_mirror_evidence.v1", account_id
        kinds = {item["kind"] for item in evidence_payload["evidence"]}
        assert "typed_blocker" in kinds, account_id
        assert evidence_payload["blockers"][0]["type"] == "source_unavailable", account_id
        assert evidence_payload["boundaries"]["order_action"] is False, account_id

    print("ACCOUNT_SOURCE_HEALTH_EVIDENCE_OK: ready=2 blocked=2")


if __name__ == "__main__":
    main()
