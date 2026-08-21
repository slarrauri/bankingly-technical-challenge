# ADR-003: Trusted Agent Harness Boundary & Pydantic Validation Gate

- **Date:** 2026-08-20  
- **Status:** Accepted  
- **Deciders:** Sebastián Larrauri (Technical Product Manager)

---

## 1. Context

AI models (LLMs) are probabilistic and susceptible to prompt injection, hallucinations, and non-deterministic behavior. In banking compliance, system actions must be strictly deterministic, authorized, and compliant with safety invariants.

---

## 2. Decision

We established a strict architectural boundary:
- **Untrusted Layer:** The LLM and any raw string extracted from external data.
- **Trusted Layer (Agent Harness):** Python code responsible for authentication, state transitions, tool permissions, output validation, approval verification, and execution.

All LLM responses must strictly validate against the Pydantic `InvestigationResult` schema. Any failure triggers a controlled retry (max 2) or safe transition to `INVESTIGATION_FAILED`.

No direct tool exists for executing side-effects (`INV-001`). State transition to `EXECUTED` strictly requires a pre-existing human `Approval` record (`INV-002`).

---

## 3. Consequences

- **Positive:** Mathematically and architecturally prevents the LLM from executing unauthorized actions regardless of prompt injection attacks or hallucinations.
- **Trade-off:** Requires rigorous schema definition and rejection handling in the Harness.
