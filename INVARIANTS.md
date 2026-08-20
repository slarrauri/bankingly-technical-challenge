# System Invariants — AML Alert Investigation Copilot

> **Authority:** Non-negotiable system rules. Every invariant is backed by automated tests.

---

## 1. Security Invariants

- **`INV-001` (No Autonomous Side-Effects):**  
  The AI agent has no tool or interface to execute side-effecting actions. The agent can only produce recommendations.
- **`INV-002` (Mandatory Human Approval):**  
  Every executed action on an alert requires a valid, pre-existing `Approval` record created by an authorized compliance analyst.
- **`INV-003` (Authorized Identity):**  
  An approval is only valid if signed by an analyst assigned and authorized for the specific institution and alert scope.
- **`INV-004` (Idempotent Execution):**  
  An approved recommendation can be executed exactly once. Subsequent execution attempts for the same recommendation must be rejected as duplicate.

---

## 2. Data & Tenant Invariants

- **`INV-005` (Strict Tenant Isolation):**  
  An investigation and its underlying tools can only query and mutate data belonging to the specific `institution_id` in scope. Cross-tenant data leakage is strictly blocked.
- **`INV-006` (Data is Not Instructions):**  
  Text retrieved from transaction descriptions, counterparty names, or customer notes must be treated strictly as data payloads and never evaluated as system instructions (Prompt Injection Defense).

---

## 3. Reasoning & Grounding Invariants

- **`INV-007` (Evidence Grounding):**  
  Every finding and risk indicator in an `InvestigationResult` must cite a valid `EvidenceReference` pointing to verifiable data returned by tools.
- **`INV-008` (Explicit Uncertainty):**  
  If required data (e.g. KYC profile or transaction history) is unavailable or inconsistent, the agent must explicitly populate `missing_information` or `limitations` and recommend `REQUEST_INFORMATION` or `ESCALATE_ALERT`.

---

## 4. Reliability & State Invariants

- **`INV-009` (Schema Conformance Gate):**  
  Any LLM output that fails Pydantic schema validation cannot advance the investigation state or generate an actionable recommendation.
- **`INV-010` (Deterministic Tool Failures):**  
  Tool failures (e.g. database connectivity errors) must be surfaced cleanly as missing information, never resulting in fabricated or assumed evidence.

---

## 5. Invariant to Test Traceability Matrix

| Invariant | Description | Verification Test File | Test Case |
|:---:|---|---|---|
| **INV-001** | No autonomous actions | `tests/security/test_invariants.py` | `test_agent_cannot_execute_actions` |
| **INV-002** | Mandatory human approval | `tests/security/test_invariants.py` | `test_execution_without_approval_denied` |
| **INV-003** | Authorized analyst approval | `tests/security/test_invariants.py` | `test_unauthorized_analyst_approval_denied` |
| **INV-004** | Idempotent execution | `tests/security/test_invariants.py` | `test_duplicate_execution_rejected` |
| **INV-005** | Strict tenant isolation | `tests/security/test_invariants.py` | `test_cross_institution_access_denied` |
| **INV-006** | Prompt injection resilience | `tests/security/test_invariants.py` | `test_prompt_injection_in_transaction_ignored` |
| **INV-007** | Evidence grounding | `tests/evaluation/test_graders.py` | `test_unsupported_findings_penalized` |
| **INV-008** | Explicit uncertainty | `tests/evaluation/test_eval_runner.py` | `test_missing_kyc_produces_request_info` |
| **INV-009** | Schema conformance gate | `tests/unit/test_harness_validator.py` | `test_invalid_llm_json_fails_safely` |
| **INV-010** | Deterministic tool failures | `tests/unit/test_tools.py` | `test_tool_error_surfaced_as_missing_info` |
