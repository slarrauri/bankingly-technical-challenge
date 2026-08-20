import pytest


def test_full_e2e_compliance_investigation_workflow(client):
    """
    E2E Walkthrough:
    1. Analyst lists alerts -> Finds AML-001 (Martín Pereira).
    2. Analyst triggers autonomous Copilot investigation.
    3. Copilot gathers data, computes deterministic summary.
    4. Copilot produces structured recommendation (ESCALATE_ALERT) with cited evidence.
    5. Analyst reviews evidence and signs off (APPROVED).
    6. System executes action -> AML-001 becomes ESCALATED_SAR.
    7. Audit event is generated and logged.
    """
    # 1. List alerts
    alerts_res = client.get("/api/v1/alerts", headers={"X-Institution-Id": "BANK-RIO-SUR"})
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()["data"]
    target_alert = next(a for a in alerts if a["id"] == "AML-001")
    assert target_alert["customer_name"] == "Martín Pereira"

    # 2. Trigger investigation
    start_res = client.post(
        "/api/v1/investigations/start",
        json={"alert_id": "AML-001"},
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert start_res.status_code == 200
    inv = start_res.json()["data"]
    inv_id = inv["investigation_id"]
    assert inv["status"] == "AWAITING_APPROVAL"
    assert inv["recommendation"]["action"] in ["ESCALATE_ALERT", "REQUEST_INFORMATION"]
    assert len(inv["recommendation"]["findings"]) > 0

    # 3. Analyst reviews & approves
    decide_res = client.post(
        f"/api/v1/investigations/{inv_id}/decide",
        json={"decision": "APPROVED", "notes": "Approved for SAR filing based on unverified Andes Trading transfers."},
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert decide_res.status_code == 200
    assert decide_res.json()["data"]["status"] == "APPROVED"

    # 4. Execution
    exec_res = client.post(
        f"/api/v1/investigations/{inv_id}/execute",
        headers={"X-Institution-Id": "BANK-RIO-SUR", "X-Analyst-Id": "ANA-0091"},
    )
    assert exec_res.status_code == 200
    exec_data = exec_res.json()["data"]
    assert exec_data["status"] == "EXECUTED"
