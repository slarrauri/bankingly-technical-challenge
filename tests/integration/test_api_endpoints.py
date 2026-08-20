import pytest


def test_health_endpoint(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"


def test_list_alerts_endpoint(client):
    res = client.get("/api/v1/alerts", headers={"X-Institution-Id": "BANK-RIO-SUR"})
    assert res.status_code == 200
    body = res.json()
    assert "data" in body
    assert len(body["data"]) == 12


def test_start_investigation_and_approval_flow(client):
    # 1. Start investigation for AML-001
    start_res = client.post(
        "/api/v1/investigations/start",
        json={"alert_id": "AML-001"},
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert start_res.status_code == 200
    inv_data = start_res.json()["data"]
    inv_id = inv_data["investigation_id"]
    assert inv_data["status"] == "AWAITING_APPROVAL"
    assert inv_data["recommendation"]["action"] in ["ESCALATE_ALERT", "REQUEST_INFORMATION"]

    # 2. Attempt unapproved execution -> Must fail (INV-002)
    exec_unapproved_res = client.post(
        f"/api/v1/investigations/{inv_id}/execute",
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert exec_unapproved_res.status_code == 400

    # 3. Analyst submits approval
    decide_res = client.post(
        f"/api/v1/investigations/{inv_id}/decide",
        json={"decision": "APPROVED", "notes": "Approved by compliance senior."},
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert decide_res.status_code == 200
    assert decide_res.json()["data"]["status"] == "APPROVED"

    # 4. Execute approved action
    exec_res = client.post(
        f"/api/v1/investigations/{inv_id}/execute",
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert exec_res.status_code == 200
    assert exec_res.json()["data"]["status"] == "EXECUTED"

    # 5. Attempt duplicate execution -> Must fail (INV-004)
    exec_dup_res = client.post(
        f"/api/v1/investigations/{inv_id}/execute",
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert exec_dup_res.status_code == 409
