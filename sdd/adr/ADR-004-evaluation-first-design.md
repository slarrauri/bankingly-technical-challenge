# ADR-004: Evaluation-First Benchmark Design (25 Stratified Cases)

- **Date:** 2026-08-20  
- **Status:** Accepted  
- **Deciders:** Sebastián Larrauri (Technical Product Manager)

---

## 1. Context

AI agent demos often risk being tuned exclusively for a single "happy path" case, masking failure modes, hallucinations, and security vulnerabilities.

---

## 2. Decision

We adopted an **Evaluation-First design**:
- Designed and locked a 25-case stratified evaluation dataset (`data/evaluation/`) *before* finalizing agent implementation.
- Scenarios cover: Clear Violations (5), Legitimate Unusual (4), Ambiguous (4), Contradictory Data (4), Missing Critical Data (3), Adversarial / Prompt Injection (3), Unauthorized Execution Attempts (2).
- Established formal metrics: Recommendation Accuracy, Evidence Grounding, Missing Information Precision, and **Unauthorized Action Rate (target: 0.0%)**.

---

## 3. Consequences

- **Positive:** Objectively measures both success modes and failure boundaries; ensures evaluation cannot be retrofitted to fit model idiosyncrasies.
- **Trade-off:** Requires upfront effort to create coherent ground-truth data and custom graders.
