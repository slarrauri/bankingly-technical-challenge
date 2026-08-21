# ⚙️ 10 — CI/CD Pipeline Specification

> **Automation Target:** GitHub Actions / Automated Quality Gates

---

## 1. Pipeline Stages

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. LINT &   │────▶│ 2. INVARIANT │────▶│  3. API &    │────▶│ 4. 25-CASE   │
│  TYPECHECK   │     │  TESTS (SEC) │     │  UNIT TESTS  │     │  EVAL BENCH  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Lint & Typecheck:**
   - Python: `ruff check .` and `mypy backend/`
   - Frontend: `npm run lint` and `tsc --noEmit`
2. **Security & Invariants Suite:**
   - `pytest tests/security/ -v` (Enforces 100% pass on `INV-001` through `INV-010`).
3. **Unit & Integration Tests:**
   - `pytest tests/unit/ tests/integration/ -v`
4. **Evaluation Benchmark:**
   - `python -m backend.evaluation.runner` (Verifies Unauthorized Action Rate == 0.0%).
