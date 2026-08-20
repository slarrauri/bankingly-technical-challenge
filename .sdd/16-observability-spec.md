# 📊 16 — Observability Specification

> **Focus:** Structured JSON Audit Trail, Investigation Traceability & System Health

---

## 1. Audit Logging Architecture

Every event in the investigation and decision lifecycle produces an immutable record in `audit_events`.

### Standard Audit Event Schema
```json
{
  "id": "AUD-2026-0042",
  "institution_id": "BANK-RIO-SUR",
  "investigation_id": "INV-2026-001",
  "timestamp": "2026-08-20T17:40:05Z",
  "actor": {
    "type": "ANALYST",
    "id": "ANA-0091",
    "ip": "10.0.4.12"
  },
  "event_type": "ACTION_EXECUTED",
  "payload": {
    "recommendation_id": "REC-001",
    "approval_id": "APP-001",
    "action": "ESCALATE_ALERT",
    "previous_status": "OPEN",
    "new_status": "ESCALATED_SAR"
  }
}
```

---

## 2. Monitored Event Types

| Event Type | Actor | Trigger |
|---|---|---|
| `INVESTIGATION_STARTED` | `ANALYST` | Analyst clicks "Investigate" |
| `TOOL_INVOKED` | `AGENT` | Agent requests tool execution with parameters |
| `TOOL_OBSERVATION` | `SYSTEM_HARNESS` | Tool returns structured data payload |
| `RECOMMENDATION_PRODUCED`| `AGENT` | Validated `InvestigationResult` generated |
| `APPROVAL_GRANTED` | `ANALYST` | Analyst signs approval decision |
| `APPROVAL_REJECTED` | `ANALYST` | Analyst rejects recommendation |
| `ACTION_EXECUTED` | `SYSTEM_HARNESS` | Alert state finalized after verified approval |
| `INVARIANT_VIOLATION_BLOCKED`| `SYSTEM_HARNESS` | Attempt to bypass approval or inject prompts |
