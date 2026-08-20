# 🌐 03 — API Contract Specification

> **Base URL:** `/api/v1`  
> **Format:** JSON  
> **Headers:** `X-Institution-Id: {id}`, `X-Analyst-Id: {id}`

---

## 1. Global Conventions

### Response Envelopes

#### Success Envelope
```json
{
  "data": { ... },
  "metadata": {
    "timestamp": "2026-08-20T17:30:00Z",
    "institution_id": "BANK-RIO-SUR"
  }
}
```

#### List Envelope with Pagination
```json
{
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 12,
    "total_pages": 1
  }
}
```

#### Error Envelope
```json
{
  "error": {
    "code": "INVALID_STATE_TRANSITION",
    "message": "Cannot execute recommendation without prior human approval.",
    "details": {}
  }
}
```

---

## 2. Endpoints

### 2.1 Alerts

#### `GET /api/v1/alerts`
- **Description:** List AML alerts with optional status and risk filters.
- **Query Params:** `status` (string), `min_risk` (int), `page` (int, def 1), `limit` (int, def 20).
- **Response `200 OK`:**
```json
{
  "data": [
    {
      "id": "AML-00127",
      "customer_id": "CUST-0042",
      "customer_name": "Martín Pereira",
      "alert_type": "UNUSUAL_TRANSACTION_PATTERN",
      "trigger_reason": "Multiple high-value incoming transfers followed by rapid outgoing transfers.",
      "risk_score": 78,
      "status": "OPEN",
      "created_at": "2026-07-14T09:30:00Z"
    }
  ],
  "pagination": { "page": 1, "limit": 20, "total": 1, "total_pages": 1 }
}
```

#### `GET /api/v1/alerts/{id}`
- **Description:** Retrieve alert details and linked investigation status.
- **Response `200 OK`:** Alert object with customer snippet.

---

### 2.2 Investigation Flow

#### `POST /api/v1/investigations/start`
- **Description:** Trigger an automated Copilot investigation on an open alert.
- **Request Body:**
```json
{
  "alert_id": "AML-00127"
}
```
- **Response `202 Accepted` / `200 OK`:**
```json
{
  "data": {
    "investigation_id": "INV-2026-001",
    "alert_id": "AML-00127",
    "status": "AWAITING_APPROVAL",
    "summary": "Customer experienced a 342% volume surge inconsistent with declared consulting income of USD 4,500/mo. Incoming funds from Andes Trading Ltd were dispersed rapidly. No commercial contract on file.",
    "risk_assessment": "HIGH",
    "confidence_score": 0.84,
    "recommendation": {
      "id": "REC-001",
      "action": "ESCALATE_ALERT",
      "rationale": "High-velocity fund turnover without underlying supporting contracts violates Policy P-001 and P-003.",
      "findings": [
        {
          "finding": "Transaction volume increased 342% above 6-month historical baseline.",
          "evidence": [
            {
              "source_type": "transaction_summary",
              "field": "volume_change_percentage",
              "value": "342.0%"
            }
          ]
        }
      ],
      "missing_information": [
        "Consulting contract or invoice justifying USD 21,000 transfer from Andes Trading Ltd."
      ],
      "applicable_policies": ["P-001", "P-002", "P-003"],
      "limitations": [
        "Counterparty business nature could not be verified beyond registered sector."
      ]
    }
  }
}
```

#### `GET /api/v1/investigations/{id}`
- **Description:** Fetch complete investigation details, findings, evidence references, and current lifecycle state.

---

### 2.3 Human Decision & Controlled Execution

#### `POST /api/v1/investigations/{id}/decide`
- **Description:** Analyst submits an approval or rejection decision.
- **Request Body:**
```json
{
  "decision": "APPROVED",
  "notes": "Agree with Copilot findings. Transfer volume is disproportionate to declared profile. Escalating to Senior Compliance."
}
```
- **Response `200 OK`:**
```json
{
  "data": {
    "investigation_id": "INV-2026-001",
    "status": "APPROVED",
    "approval": {
      "id": "APP-001",
      "analyst_id": "ANA-0091",
      "decision": "APPROVED",
      "created_at": "2026-08-20T17:40:00Z"
    }
  }
}
```

#### `POST /api/v1/investigations/{id}/execute`
- **Description:** Executes the finalized decision on the alert. Requires prior valid `Approval`.
- **Response `200 OK`:**
```json
{
  "data": {
    "investigation_id": "INV-2026-001",
    "alert_id": "AML-00127",
    "status": "EXECUTED",
    "resulting_alert_status": "ESCALATED_SAR",
    "executed_at": "2026-08-20T17:40:05Z"
  }
}
```
- **Error `400 Bad Request` (INV-002 Violation):**
```json
{
  "error": {
    "code": "UNAPPROVED_EXECUTION_DENIED",
    "message": "Action cannot be executed without human approval."
  }
}
```

---

### 2.4 Internal Tool Contracts (Used by Agent Harness)

| Tool Name | Parameters | Output Shape |
|---|---|---|
| `get_alert` | `alert_id: str` | Full alert record |
| `get_customer_profile` | `customer_id: str` | Customer core + KYC profile |
| `get_transactions` | `customer_id: str, date_from: str, date_to: str` | Array of transaction records |
| `get_transaction_summary` | `customer_id: str, period_days: int` | Inflow/outflow stats, velocity, % change |
| `get_previous_alerts` | `customer_id: str` | Array of historical alerts & resolutions |
| `get_aml_policies` | `category: Optional[str]` | List of institutional AML policies |

---

### 2.5 Evaluation & Benchmark Endpoints

#### `POST /api/v1/evaluations/run`
- **Description:** Runs the 25-case evaluation suite against the active LLM provider.
- **Response `200 OK`:** Summary report with Recommendation Accuracy, Evidence Grounding, and Unauthorized Action Rate.
