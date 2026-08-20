# ADR-005: Deterministic Calculation for Financial Metrics & Aggregations

- **Date:** 2026-08-20  
- **Status:** Accepted  
- **Deciders:** Sebastián Larrauri (Technical Product Manager)

---

## 1. Context

LLMs are notoriously unreliable at arithmetic, currency sums, percentage calculations, and aggregation over large arrays of transactions. Prompting an LLM to sum 50 transactions frequently produces arithmetic errors and hallucinations.

---

## 2. Decision

We mandated that all numerical aggregations, historical baselines, and percentage volume changes must be computed **deterministically** by a specialized tool service (`get_transaction_summary`) using Python / SQL Decimal logic.

The LLM is responsible for **interpreting** the computed result (e.g. comparing `+342%` against policy thresholds), but **never calculating** the raw statistics.

---

## 3. Consequences

- **Positive:** 100% reproducible and accurate financial metrics; drastically reduced token consumption and prompt complexity.
- **Trade-off:** Requires writing dedicated aggregation service functions in the tool layer.
