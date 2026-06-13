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
    assert [event["seq"] for event in events] == [2, 3]

