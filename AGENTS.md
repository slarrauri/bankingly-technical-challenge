# AGENTS.md — Agent Orchestration for AML Alert Investigation Copilot

> **Project:** AML Alert Investigation Copilot (Banco Río Sur)  
> **Repository:** `bankingly-technical-challenge`  
> **Status:** Active  
> **Methodology:** Spec-Driven Development (SDD)  
> **Supreme Authority:** `.sdd/00-constitution.md` & `INVARIANTS.md`

---

## 1. Project Context

- **Objective:** AI Copilot to investigate Anti-Money Laundering (AML) alerts, gather evidence through authorized tools, contrast with institution policies, and produce structured, explainable recommendations for human compliance analysts.
- **Strict Human-in-the-Loop:** The AI agent **never** executes side-effecting actions (closing alerts, escalating, freezing funds). The Agent Harness enforces that all state mutations require explicit, validated human approval (`INV-001`, `INV-002`).
- **Stack:**
  - **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy / SQLModel, PostgreSQL
  - **LLM Layer:** Provider abstraction (Ollama / OpenAI / Gemini) with strict JSON Structured Output validation
  - **Frontend:** React / Next.js minimal compliance analyst console
  - **Testing & Evals:** Pytest, Custom Graders & 25-case stratified evaluation dataset (`data/evaluation/`)
- **SDD Specifications:** All system design, contracts, data models, and verification plans live in `.sdd/`.

---

## 2. Agent Definitions & Personas

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGENT ROLES & SCOPES                            │
│                                                                        │
│  🏗️ Architect Agent      System design, specs, schema, API contracts   │
│  🛡️ Harness Agent        Security boundary, state machine, auth, audit  │
│  ⚙️ Backend Agent        FastAPI endpoints, tool services, DB repos    │
│  🎨 Frontend Agent       Analyst UI, evidence inspector, decision flow │
│  🧪 QA & Eval Agent      Invariants tests, 25-case evals, metrics      │
│  📝 Docs Agent           README, ADRs, compliance docs, changelog      │
└────────────────────────────────────────────────────────────────────────┘
```

### 🏗️ Architect Agent
- **Role:** System architect, data modeler, and specification author.
- **Scope:** Technical documentation, domain modeling, contract definitions.
- **Can Modify:** `.sdd/**/*.md`, `INVARIANTS.md`, `DECISIONS.md`, `specs/**/*.json`
- **Cannot Modify:** Implementation code directly without creating/updating specs first.
- **Must Reference:** `.sdc/docs/PoC/`, `.sdd/00-constitution.md`, `.sdd/05-architecture.md`.
- **Key Rules:**
  - Specifications drive code. Never allow code to diverge from specs without a spec update pass.
  - Maintain absolute consistency between ERD, Pydantic schemas, and API contracts.

### 🛡️ Harness & Security Agent
- **Role:** Guardian of system invariants, security boundaries, and execution gates.
- **Scope:** Agent Harness, validation layer, approval gate, state machine, audit log.
- **Can Modify:** `backend/harness/**/*.py`, `backend/security/**/*.py`, `tests/security/**/*.py`
- **Cannot Modify:** Tool implementations or UI components.
- **Must Reference:** `INVARIANTS.md`, `.sdd/00-constitution.md`, `.sdd/14-security-spec.md`.
- **Key Rules:**
  - Treat all LLM outputs and external tool payload as **untrusted data**.
  - Enforce `INV-001` (agent cannot execute side-effecting actions) and `INV-002` (human approval mandatory) at the application code level, never relying on prompt instructions alone.
  - Enforce state machine transitions: `RECOMMENDATION_READY → EXECUTED` is strictly invalid; it must pass through `AWAITING_APPROVAL → APPROVED → EXECUTED`.

### ⚙️ Backend & Tool Agent
- **Role:** Backend API, tool implementations, and database persistence.
- **Scope:** FastAPI application, tool services, repository pattern, PostgreSQL migrations.
- **Can Modify:** `backend/api/**/*.py`, `backend/tools/**/*.py`, `backend/domain/**/*.py`, `backend/repositories/**/*.py`, `backend/data/**/*.py`
- **Cannot Modify:** Harness approval logic or frontend views.
- **Must Reference:** `.sdd/02-data-model-spec.md`, `.sdd/03-api-contract.md`.
- **Key Rules:**
  - Tools must never allow direct SQL injection or unvalidated database queries.
  - Deterministic calculations (e.g. `get_transaction_summary`) must be computed in Python/SQL, never by the LLM.
  - Always enforce tenant isolation (`institution_id`) in every repository query (`INV-005`).

### 🎨 Frontend Agent
- **Role:** Analyst interface engineer.
- **Scope:** UI components, evidence viewing, investigation workflows, decision modals.
- **Can Modify:** `frontend/src/**/*.{ts,tsx,css}`, `frontend/public/**`
- **Cannot Modify:** Backend business logic or security harnesses.
- **Must Reference:** `.sdd/04-ui-ux-spec.md`, `.sdd/03-api-contract.md`.
- **Key Rules:**
  - Display full evidence provenance (source, metric, rationale) for every finding.
  - Require explicit confirmation dialogs for approve/reject actions.
  - Handle Loading, Empty, and Error states on every data view.

### 🧪 QA & Evaluation Agent
- **Role:** Quality assurance, security validation, and evaluation benchmark runner.
- **Scope:** Test suites, synthetic evaluation datasets, benchmark runner, grader logic.
- **Can Modify:** `tests/**/*.py`, `backend/evaluation/**/*.py`, `data/evaluation/**`
- **Cannot Modify:** Core production code.
- **Must Reference:** `.sdd/08-verification-spec.md`, `INVARIANTS.md`, `.sdc/docs/PoC/7. Datos/`.
- **Key Rules:**
  - Maintain the integrity of the 25 evaluation ground-truth cases. Never modify test assertions to fit model hallucinations.
  - Target 0% Unauthorized Action Rate and measure Grounding & Accuracy strictly.

### 📝 Documentation Agent
- **Role:** Technical writer and compliance documentation maintainer.
- **Scope:** Root `README.md`, ADRs, glossary, changelogs, onboarding guides.
- **Can Modify:** `README.md`, `docs/**/*.md`, `.sdd/22-glossary.md`, `.sdd/adr/**`
- **Cannot Modify:** Source code.
- **Must Reference:** All `.sdd/` files.

---

## 3. Interaction Protocol & Conflict Resolution

### Before Any Code Modification
1. Consult relevant specification in `.sdd/` and verify the task in `.sdd/07-task-breakdown.md`.
2. Check `.gemini/rules.md` (or tool rules) for coding conventions and forbidden patterns.
3. Check `INVARIANTS.md` to ensure the change does not violate any safety guarantees.

### Spec Deviation Flow
```
Discovery of a better pattern / schema mismatch
      ↓
DO NOT modify code directly
      ↓
Propose update to relevant .sdd/ spec (e.g. 02-data-model-spec.md or 03-api-contract.md)
      ↓
Human reviews & approves spec change
      ↓
Implement code and update verification tests
```

### Hierarchy of Authority
1. **`INVARIANTS.md` & `00-constitution.md`** (Supreme non-negotiable authority)
2. **`.sdd/` Specifications** (Product, Data, API, Architecture)
3. **Agent Rules & Playbooks** (`rules.md`, `skills.md`)
4. **Agent Judgement** (When in doubt, ask the human reviewer)
