from fastapi.testclient import TestClient

from nautilus_account_console.main import app


def test_accounts_fixture_exposes_demo_account() -> None:
    client = TestClient(app)
    response = client.get("/api/accounts")
    assert response.status_code == 200
    accounts = response.json()
    assert accounts[0]["account_id"] == "paper.demo-01"
    assert accounts[0]["account_kind"] == "real_feed_sandbox_paper"


def test_events_support_cursor() -> None:
    client = TestClient(app)
    response = client.get("/api/accounts/paper.demo-01/events?cursor=1")
    assert response.status_code == 200
    events = response.json()
    assert [event["seq"] for event in events] == [2, 3, 4]


def test_order_execution_reports_are_scoped_by_order_id() -> None:
    client = TestClient(app)
    response = client.get("/api/accounts/paper.demo-01/orders/C-0001/execution-reports")
    assert response.status_code == 200
    payload = response.json()
    assert payload["client_order_id"] == "C-0001"
    assert [report["seq"] for report in payload["reports"]] == [1, 2, 3]
    assert {report["client_order_id"] for report in payload["reports"]} == {"C-0001"}
