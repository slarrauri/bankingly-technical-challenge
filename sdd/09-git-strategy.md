# 🌿 09 — Git Strategy & Branching Model

> **Branch Model:** GitHub Flow (Feature Branches -> Pull Request -> main)  
> **Commit Convention:** Conventional Commits

---

## 1. Branching Strategy

```
main (always deployable, protected)
 │
 ├── feat/AML-01-domain-models
 ├── feat/AML-02-harness-approval-gate
 ├── feat/AML-03-fastapi-routes
 └── test/AML-04-evaluation-benchmark
```

### Branch Naming Conventions
- `feat/{ticket}-{short-description}`: New features or tools
- `fix/{ticket}-{short-description}`: Bug fixes
- `refactor/{short-description}`: Code restructuring without feature change
- `test/{short-description}`: Test suites & evaluation additions
- `docs/{short-description}`: Specification or documentation updates

---

## 2. Commit Message Standards (Conventional Commits)

```
<type>(<scope>): <short summary>

[optional body describing rationale]

[optional footer referencing invariants or specs]
```

### Examples
- `feat(harness): implement state machine and approval gate (INV-002)`
- `feat(tools): add deterministic get_transaction_summary service`
- `test(security): add test suite for invariants INV-001 through INV-010`
- `docs(specs): finalize 03-api-contract endpoints for alert investigation`
