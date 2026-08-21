# 📝 07 — Task Breakdown

> **Traceability:** Every task maps to PRD workflows (`01-product-requirements.md`), API endpoints (`03-api-contract.md`), and System Invariants (`INVARIANTS.md`).

---

## 1. Phase 1: Foundation & Persistence

- [ ] **T-001** (`backend/domain/models.py`): Define SQLAlchemy / SQLModel database entities (`Customer`, `CustomerKYC`, `Transaction`, `Counterparty`, `AMLAlert`, `AMLPolicy`, `Investigation`, `Recommendation`, `Approval`, `AuditEvent`).  
  *Traces to: `.sdd/02-data-model-spec.md` §3.*
- [ ] **T-002** (`backend/data/database.py`): Implement async PostgreSQL engine and session factory with connection pooling.
- [ ] **T-003** (`backend/data/seed.py`): Ingest Banco Río Sur seed universe (12 customers, 18 counterparties, ~400 transactions, 4 policies, 12 alerts).  
  *Traces to: `.sdd/02-data-model-spec.md` §4.*
- [ ] **T-004** (`tests/unit/test_persistence.py`): Write unit tests to verify seed idempotency and database relational constraints.

---

## 2. Phase 2: Tool Services & Isolation

- [ ] **T-005** (`backend/tools/schemas.py`): Define Pydantic request and response schemas for all 6 tools.  
  *Traces to: `.sdd/03-api-contract.md` §2.4.*
- [ ] **T-006** (`backend/tools/services/alert_service.py`): Implement `get_alert(alert_id)` with institution scope.
- [ ] **T-007** (`backend/tools/services/customer_service.py`): Implement `get_customer_profile(customer_id)` returning customer and KYC details.
- [ ] **T-008** (`backend/tools/services/transaction_service.py`): Implement `get_transactions` with date bounds and limit constraints.
- [ ] **T-009** (`backend/tools/services/summary_service.py`): Implement deterministic `get_transaction_summary` calculating velocity, total inflow/outflow, and % variance.
- [ ] **T-010** (`backend/tools/services/policy_service.py`): Implement `get_aml_policies(category)` and `get_previous_alerts`.
- [ ] **T-011** (`tests/unit/test_tools.py`): Test tool calculations, boundary parameters, and tenant isolation (`INV-005`).

---

## 3. Phase 3: Agent Harness & Security Boundary

- [ ] **T-012** (`backend/agent/schemas.py`): Implement Pydantic `InvestigationResult`, `Finding`, `EvidenceReference`, `Recommendation` models with enum guards.  
  *Traces to: `.sdd/02-data-model-spec.md` §3.8.*
- [ ] **T-013** (`backend/agent/prompt_engine.py`): Design system prompt defining investigator role, tools instructions, and prompt injection demarcation tags (`INV-006`).
- [ ] **T-014** (`backend/agent/llm_client.py`): Implement LLM abstraction layer with Ollama / OpenAI providers and structured output parsing.
- [ ] **T-015** (`backend/harness/orchestrator.py`): Implement investigation loop (receive alert -> call tools -> compile observations -> request structured recommendation).
- [ ] **T-016** (`backend/harness/validator.py`): Implement schema validation gate with max 2 retries on malformed JSON (`INV-009`).
- [ ] **T-017** (`backend/harness/state_machine.py`): Implement investigation state transitions enforcing `AWAITING_APPROVAL -> APPROVED -> EXECUTED`.
- [ ] **T-018** (`backend/harness/approval_gate.py`): Implement approval validation gate blocking unapproved execution (`INV-001`, `INV-002`, `INV-003`, `INV-004`).
- [ ] **T-019** (`backend/harness/audit_service.py`): Implement structured event logging to `audit_events`.
- [ ] **T-020** (`tests/security/test_invariants.py`): Write security test suite for Invariants `INV-001` through `INV-010`.

---

## 4. Phase 4: REST API & Evaluation Benchmark

- [ ] **T-021** (`backend/api/alerts.py`): Implement `GET /api/v1/alerts` and `GET /api/v1/alerts/{id}`.  
  *Traces to: `.sdd/03-api-contract.md` §2.1.*
- [ ] **T-022** (`backend/api/investigations.py`): Implement `POST /api/v1/investigations/start` and `GET /api/v1/investigations/{id}`.  
  *Traces to: `.sdd/03-api-contract.md` §2.2.*
- [ ] **T-023** (`backend/api/decisions.py`): Implement `POST /api/v1/investigations/{id}/decide` and `POST /api/v1/investigations/{id}/execute`.  
  *Traces to: `.sdd/03-api-contract.md` §2.3.*
- [ ] **T-024** (`backend/evaluation/dataset.py`): Load the 25 stratified evaluation scenarios with ground-truth labels.
- [ ] **T-025** (`backend/evaluation/graders.py`): Implement evaluation graders (Recommendation Accuracy, Evidence Grounding, Missing Info, Security Gate).
- [ ] **T-026** (`backend/evaluation/runner.py`): Implement benchmark runner and metrics report generator (`evals/benchmark_report.json`).
- [ ] **T-027** (`tests/integration/test_api_endpoints.py`): Write integration tests for all REST API endpoints.

---

## 5. Phase 5: Web Compliance Console & E2E Verification

- [ ] **T-028** (`frontend/src/components/AlertList.tsx`): Implement alert queue with risk badges and status filters.  
  *Traces to: `.sdd/04-ui-ux-spec.md` §2.*
- [ ] **T-029** (`frontend/src/components/InvestigationWorkspace.tsx`): Implement investigation report layout with findings, evidence tags, and missing info warnings.
- [ ] **T-030** (`frontend/src/components/DecisionModal.tsx`): Implement approval/rejection modal with confirmation gate.
- [ ] **T-031** (`frontend/src/index.css`): Implement responsive design system and fintech styling tokens.
- [ ] **T-032** (`tests/e2e/test_walkthrough.py`): Implement automated E2E script executing the full end-to-end investigation and approval scenario.
- [ ] **T-033** (`README.md`): Update master documentation with architecture diagrams, evaluation metrics, and local execution instructions.
