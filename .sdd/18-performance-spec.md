# ⚡ 18 — Performance Specification

> **Focus:** Service Level Objectives (SLOs), Latency Budgets & Tool Limits

---

## 1. Service Level Objectives (SLOs)

| Metric | Target | Measurement Method |
|---|---|---|
| **Investigation End-to-End Latency** | `< 6.0 seconds` (local Ollama / Cloud API) | Time from `POST /investigations/start` to `AWAITING_APPROVAL` |
| **Deterministic Tool Execution** | `< 50 ms` per tool call | In-memory PostgreSQL indexed query execution |
| **Approval Execution Latency** | `< 100 ms` | Time for `/execute` transaction commit and audit write |
| **Pydantic Schema Validation** | `< 5 ms` | Rust-core schema serialization & validation |
| **Benchmark Suite Execution (25 Cases)**| `< 90 seconds` total batch | Automated pytest benchmark run |

---

## 2. Hard Limits & Boundaries

- `max_date_range_days`: 365 days for `get_transactions`.
- `max_results_limit`: 500 records per tool response to prevent context window overflow.
- `max_llm_retries`: 2 retries on schema parse error before emitting `INVESTIGATION_FAILED`.
