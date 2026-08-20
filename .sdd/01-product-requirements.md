# 📋 01 — Product Requirements Document (PRD)

> **Product:** AML Alert Investigation Copilot  
> **Target Institution:** Banco Río Sur (Retail & Commercial Banking, Uruguay)  
> **Primary User:** Compliance / AML Analyst

---

## 1. Problem Statement

Financial institution compliance analysts face high operational workloads investigating AML monitoring alerts. The investigation process requires manually querying and correlating customer KYC information, recent and historical transactions, counterparties, previous alerts, and applicable institutional policies before deciding whether to close an alert, escalate it, or request further information.

This process is cognitively demanding, repetitive, and vulnerable to missed evidence or inconsistent policy enforcement.

---

## 2. Product Vision & Value Proposition

An internal **Agentic Banking Copilot** that autonomously conducts structured preliminary investigations of designated AML alerts:
1. Gathers relevant context via authorized read-only tools.
2. Identifies inconsistencies, anomalies, and policy triggers.
3. Explicitly flags missing information or evidentiary limitations.
4. Generates an explainable recommendation with full citation of evidence.
5. Presents the complete case to the human analyst for approval/rejection before any action is executed.

```
                      INVESTIGATION WORKFLOW
  Alert Selected ──▶ Agent Gathers Evidence ──▶ Evaluates Policies ──┐
                                                                     │
  Action Executed ◀── Human Approves/Rejects ◀── Formulates Rec. ────┘
```

---

## 3. User Persona

- **Name:** Andrea Silva
- **Role:** AML / Compliance Analyst (Banco Río Sur)
- **Goals:** Quickly understand why an alert triggered, inspect correlated evidence without querying 4 separate systems, make an informed decision, and maintain a full audit trail.
- **Frustrations:** Time wasted pulling data manually; lack of standardized case summaries; pressure to maintain zero false negative rates.

---

## 4. Core Workflows & Prioritization

### Workflow P1: Targeted Alert Investigation (Highest Priority)
- **Description:** Analyst selects an open alert (e.g. `AML-00127`) and requests an automated investigation.
- **Acceptance Criteria:**
  - [ ] Agent initiates investigation in state `INVESTIGATING`.
  - [ ] Agent invokes tools: `get_alert`, `get_customer_profile`, `get_transaction_summary`, `get_transactions`, `get_previous_alerts`, `get_aml_policies`.
  - [ ] Agent reasons over observations and constructs an `InvestigationResult` JSON payload conforming to schema.
  - [ ] State advances to `RECOMMENDATION_READY` and then `AWAITING_APPROVAL`.

### Workflow P2: Evidence Correlation & Policy Evaluation
- **Description:** Agent correlates observed transactional patterns with declared customer KYC profile and checks against institution AML policies (`P-001` to `P-004`).
- **Acceptance Criteria:**
  - [ ] Detects velocity increases (e.g. `>300%` historical average).
  - [ ] Detects new or unverified high-risk counterparties.
  - [ ] Cites exact policy identifiers triggered by the observed evidence.
  - [ ] Identifies missing documentation (e.g. invoice or contract for sudden consulting funds) and lists it under `missing_information`.

### Workflow P3: Human Review, Approval & Controlled Execution
- **Description:** Analyst inspects findings and decides whether to approve, reject, or request more information.
- **Acceptance Criteria:**
  - [ ] UI displays executive summary, risk level, confidence score, findings with evidence sources, missing information, and recommended action.
  - [ ] Available actions restricted to: `CLOSE_ALERT`, `ESCALATE_ALERT`, `REQUEST_INFORMATION`.
  - [ ] Analyst submits approval/rejection decision with optional notes.
  - [ ] Harness validates analyst identity and status before executing the transition to `EXECUTED` (`INV-002`, `INV-003`, `INV-004`).
  - [ ] Audit trail record is generated in `AuditEvent`.

### Workflow P4: Evaluation Benchmark & Quality Governance
- **Description:** System automated evaluation over a 25-case stratified test suite.
- **Acceptance Criteria:**
  - [ ] Runs benchmark across 7 scenario categories (Clear, Legitimate Unusual, Ambiguous, Contradictory, Missing Data, Adversarial Prompt Injection, Security Gate).
  - [ ] Calculates metrics: Recommendation Accuracy, Evidence Grounding, Missing Info Detection, and Unauthorized Action Rate.
  - [ ] Verifies Unauthorized Action Rate is exactly 0.0%.

---

## 5. Scope Boundaries (In-Scope vs. Out-of-Scope)

| In-Scope (MVP PoC) | Out-of-Scope (Future Roadmap) | Rationale for Exclusion |
|---|---|---|
| Single targeted alert investigation | Automated queue triage / prioritization | Keep focus on depth of investigation slice |
| Simulated banking dataset (Banco Río Sur) | Live core banking / core AML integrations | Avoid external infrastructure dependencies |
| 6 read-only tools | Real KYC/Sanctions API integrations | Sufficient to demonstrate tool-calling pattern |
| 3 actions (`CLOSE`, `ESCALATE`, `REQUEST_INFO`) | Account blocking / freezing funds | Avoid unnecessary regulatory/legal complexity |
| 25-case evaluation benchmark | Automated prompt fine-tuning | Focus on measuring rather than training |
| Modular monolith (FastAPI + React) | Microservices & distributed orchestration | Unnecessary architectural overhead for PoC |

---

## 6. Product Success Metrics & Hypotheses

- **H1 (Efficiency):** Copilot reduces investigation time per alert from ~15 minutes to <2 minutes.
- **H2 (Quality):** >85% recommendation accuracy and >90% evidence grounding across the benchmark.
- **H3 (Security):** 0% unauthorized actions and 100% prompt injection resistance.
- **H4 (Multi-tenant Reusability):** System adapts to another institution's policies via configuration data without modifying core code.
