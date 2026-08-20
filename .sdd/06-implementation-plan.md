# 📅 06 — Implementation Plan

> **Project:** AML Alert Investigation Copilot  
> **Methodology:** Spec-Driven Development (Phase 9 Execution)  
> **Strategy:** Phased Incremental Delivery with Continuous Quality Gates

---

## 1. Implementation Phases & Milestones

```mermaid
gantt
    title Implementation Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1: Core Setup
    Database & Models Setup          :p1_1, 2026-08-21, 1d
    Seed Data Ingestion              :p1_2, after p1_1, 1d
    section Phase 2: Tool Services
    Deterministic Tool Services      :p2_1, after p1_2, 1d
    Tool Registry & Tenant Filtering :p2_2, after p2_1, 1d
    section Phase 3: Agent Harness
    Pydantic Schemas & LLM Engine    :p3_1, after p2_2, 1d
    Approval Gate & State Machine    :p3_2, after p3_1, 1d
    section Phase 4: API & Evals
    FastAPI Endpoints                :p4_1, after p3_2, 1d
    25-Case Eval Benchmark Runner    :p4_2, after p4_1, 1d
    section Phase 5: UI & E2E
    Analyst Web Console              :p5_1, after p4_2, 1d
    E2E Verification & Audit Demo    :p5_2, after p5_1, 1d
```

---

## 2. Detailed Phase Breakdown

### Phase 1: Domain & Persistence Foundation
- **Goal:** Establish PostgreSQL schema, migrations, domain models, and load Banco Río Sur simulated seed universe.
- **Key Deliverables:** SQLAlchemy models in `backend/domain/` and seed script in `backend/data/seed.py`.
- **Quality Gate:** Database tables created, constraints active, and seed queries successfully verified.

### Phase 2: Tool Services & Isolation
- **Goal:** Implement the 6 read-only tool services with deterministic calculations (`get_transaction_summary`) and tenant scoping.
- **Key Deliverables:** Service modules in `backend/tools/services/` and unit test coverage in `tests/unit/test_tools.py`.
- **Quality Gate:** 100% unit test pass rate; verified that `institution_id` cannot be bypassed.

### Phase 3: Agent Harness & Security Boundary
- **Goal:** Implement LLM client abstraction, Pydantic `InvestigationResult` validation, prompt injection defense, and the state machine approval gate.
- **Key Deliverables:** `backend/harness/` orchestrator, validator, and approval gate.
- **Quality Gate:** `INV-001` (No autonomous action) and `INV-002` (Mandatory human approval) automated tests passing.

### Phase 4: REST API & Evaluation Suite
- **Goal:** Expose FastAPI routes and build the evaluation benchmark runner for the 25 stratified scenarios.
- **Key Deliverables:** `backend/api/` routers and `backend/evaluation/` benchmark engine with reporting.
- **Quality Gate:** Evaluation runner outputs metrics: Accuracy, Evidence Grounding, and 0% Unauthorized Action Rate.

### Phase 5: Compliance Web Console & E2E Walkthrough
- **Goal:** Build the React/Next.js console, connect to API, and conduct the end-to-end walkthrough.
- **Key Deliverables:** Frontend views in `frontend/src/` and verified E2E demo flow.
- **Quality Gate:** Complete E2E walkthrough script passing with full audit trail generated.
