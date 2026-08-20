# ADR-001: Selection of AML Alert Investigation Copilot as Core PoC

- **Date:** 2026-08-20  
- **Status:** Accepted  
- **Deciders:** Sebastián Larrauri (Technical Product Manager)

---

## 1. Context

The Bankingly technical challenge calls for demonstrating an internal Agentic Banking capability with strict human-in-the-loop controls, simulated data, measurable evaluations, and separation of model reasoning from code-enforced safety controls.

We evaluated 5 candidate use cases:
1. AML Alert Investigation Copilot
2. Credit Application Review
3. KYC Identity Verification
4. Early Debt Collections
5. Portfolio Risk Monitoring

---

## 2. Decision

We decided to build the **AML Alert Investigation Copilot** for internal compliance analysts of Banco Río Sur.

### Rationale:
1. **Strong Agentic Fit:** Naturally involves inspecting an alert, planning which tools to call, correlating evidence across KYC and transactions, reasoning over institutional policies, and formulating structured recommendations.
2. **Explicit Human-in-the-Loop Boundary:** The separation `Agent Recommendation -> Human Approval -> Controlled Execution` is unambiguous and directly testable.
3. **High Evaluation Potential:** Enables constructing a rich evaluation set covering clear cases, ambiguous patterns, contradictory data, missing documentation, and adversarial prompt injections.
4. **Appropriate Risk Profile:** Demonstrates governance, explainability, auditability, and safety without requiring live core banking connections.

---

## 3. Consequences

- **Positive:** Clear vertical slice, high testability, strong alignment with challenge criteria.
- **Trade-off:** Excludes end-customer conversational banking features in favor of a deeper, safer internal operations agent.
