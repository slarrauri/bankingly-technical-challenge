# 🏦 AML Alert Investigation Copilot — Bankingly Technical Challenge

> **Technical Product Manager Challenge**  
> **Institution:** Banco Río Sur (Simulated Banking Context, Uruguay)  
> **Methodology:** Spec-Driven Development (SDD) & Enterprise AI Governance  
> **Status:** Phase 1–8 Specifications Baselined & Ready for Build (Phase 9)

---

## 1. Executive Summary & Problem

Financial institution compliance analysts spend excessive hours manually compiling data across core banking, KYC records, and transactional databases to investigate AML monitoring alerts.

The **AML Alert Investigation Copilot** automates the preliminary investigation workflow:
1. Gathers context using authorized read-only data tools.
2. Identifies anomalies, velocity spikes, and counterparty risks.
3. Evaluates evidence against institutional policies (`P-001` to `P-004`).
4. Generates an explainable structured recommendation (`CLOSE_ALERT`, `ESCALATE_ALERT`, `REQUEST_INFORMATION`).
5. Enforces **strict Human-in-the-Loop approval**: No state mutation occurs without verified analyst authorization.

```
                          INVESTIGATION LIFECYCLE
  Alert Selected ──▶ Agent Gathers Evidence ──▶ Evaluates Policies ──┐
                                                                     │
  Action Executed ◀── Human Approves/Rejects ◀── Formulates Rec. ────┘
```

---

## 2. System Architecture & Safety Model

The system is built as a **5-Layer Modular Monolith** in **Python / FastAPI / PostgreSQL** with a React compliance console.

```
                    TRUSTED vs. UNTRUSTED BOUNDARY

    [ UNTRUSTED AI AGENT (LLM) ]
    (Probabilistic reasoning, prompt engine, tool request generation)
               │ (Outputs Pydantic JSON Recommendation only)
               ▼
    ════════════════════════════════════════════════════════════════
           TRUSTED AGENT HARNESS (Python / FastAPI Application)
    ════════════════════════════════════════════════════════════════
               │ 1. Schema Validation (InvestigationResult)
               │ 2. Tenant Isolation Filter (institution_id)
               │ 3. State Machine Transition Guard
               │ 4. Mandatory Human Approval Verification (INV-002)
               ▼
    [ CONTROLLED POSTGRESQL MUTATION & AUDIT LOG ]
```

---

## 3. Formal Invariants (`INVARIANTS.md`)

All system operations conform to 10 non-negotiable invariants with 100% automated test verification:
- `INV-001`: The agent cannot execute side-effecting actions.
- `INV-002`: Every executed action requires valid human approval.
- `INV-003`: Approval must belong to an authorized analyst.
- `INV-004`: Idempotent action execution.
- `INV-005`: Strict tenant isolation (`institution_id`).
- `INV-006`: Prompt injection in transaction text treated as inert data.
- `INV-007`: Findings must cite verifiable evidence references.
- `INV-008`: Missing evidence produces explicit uncertainty state.
- `INV-009`: Schema conformance gate (Pydantic validation).
- `INV-010`: Tool failures surfaced cleanly, never fabricating evidence.

---

## 4. Spec-Driven Development (SDD) Artifact Map

All system specifications live in the [`.sdd/`](file:///f:/documents/bankingly-technical-challenge/.sdd/) directory:

| Layer | Specification Document | Key Focus |
|---|---|---|
| **Layer 1: Product** | [`00-constitution.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/00-constitution.md) | Non-negotiable principles & stack constraints |
| | [`01-product-requirements.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/01-product-requirements.md) | Workflows P1–P4, persona & acceptance criteria |
| | [`02-data-model-spec.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/02-data-model-spec.md) | PostgreSQL ERD, table schemas & seed strategy |
| | [`03-api-contract.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/03-api-contract.md) | REST API endpoints, envelopes & tool contracts |
| | [`04-ui-ux-spec.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/04-ui-ux-spec.md) | Analyst workspace wireframes & design tokens |
| | [`05-architecture.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/05-architecture.md) | 5-layer modular monolith, sequence flows & state machine |
| | [`06-implementation-plan.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/06-implementation-plan.md) | Phased engineering roadmap & quality gates |
| | [`07-task-breakdown.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/07-task-breakdown.md) | Atomic tasks (T-001..T-033) backlog |
| | [`08-verification-spec.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/08-verification-spec.md) | Test matrix, 25-case eval suite & E2E walkthrough |
| **Layer 2: Process** | [`09-git-strategy.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/09-git-strategy.md) & [`10-cicd-pipeline.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/10-cicd-pipeline.md) | Branching standards & automated CI quality gates |
| **Layer 3: Security**| [`14-security-spec.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/14-security-spec.md) | Threat model, prompt injection defense & RBAC |
| **Layer 4: Ops** | [`16-observability-spec.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/16-observability-spec.md) & [`18-performance-spec.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/18-performance-spec.md) | Audit trail schema & latency SLOs |
| **Layer 5: AI Config**| [`AGENTS.md`](file:///f:/documents/bankingly-technical-challenge/AGENTS.md) & [`.gemini/rules.md`](file:///f:/documents/bankingly-technical-challenge/.gemini/rules.md) | Multi-agent scopes, coding rules & skill templates |
| **Layer 6: Knowledge**| [`DECISIONS.md`](file:///f:/documents/bankingly-technical-challenge/DECISIONS.md) & [`22-glossary.md`](file:///f:/documents/bankingly-technical-challenge/.sdd/22-glossary.md) | Architecture Decision Records (ADR-001..005) & Glossary |

---

## 5. AI Agent Configuration Ecosystem

This repository is pre-configured for AI coding assistants:
- **Universal Orchestration:** [`AGENTS.md`](file:///f:/documents/bankingly-technical-challenge/AGENTS.md) defines Architect, Harness, Backend, Frontend, and Evaluation agent personas.
- **Rules & Constraints:** [`.gemini/rules.md`](file:///f:/documents/bankingly-technical-challenge/.gemini/rules.md), [`.cursor/rules/aml-copilot.mdc`](file:///f:/documents/bankingly-technical-challenge/.cursor/rules/aml-copilot.mdc), and [`.github/copilot-instructions.md`](file:///f:/documents/bankingly-technical-challenge/.github/copilot-instructions.md).
- **Reusable Playbooks:** [`.gemini/skills.md`](file:///f:/documents/bankingly-technical-challenge/.gemini/skills.md) (`add-aml-tool`, `add-evaluation-scenario`, `verify-invariants`).
- **AI Governance:** [`AI_USE_PROTOCOL.md`](file:///f:/documents/bankingly-technical-challenge/AI_USE_PROTOCOL.md) aligned with fintech regulatory standards.

---

## 6. Evaluation Benchmark (25 Stratified Scenarios)

The evaluation suite (`data/evaluation/`) validates:
1. **Clear AML Violations (5):** Escalation accuracy on severe pattern mismatches.
2. **Legitimate Unusual Activity (4):** False positive avoidance on documented large transactions.
3. **Ambiguous Patterns (4):** Requesting further information when evidence is incomplete.
4. **Contradictory Information (4):** Detecting discrepancies between declared KYC and actual behavior.
5. **Missing Critical Data (3):** Surfacing analytical limitations without guessing.
6. **Adversarial / Prompt Injection (3):** Ignoring malicious instructions inside transaction text.
7. **Security Gate Validation (2):** Blocking unauthorized execution attempts (**Target: 0.0%**).