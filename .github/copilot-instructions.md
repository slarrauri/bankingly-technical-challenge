# GitHub Copilot Instructions — AML Alert Investigation Copilot

This repository implements an internal AML Alert Investigation Copilot for compliance analysts.

### Core Architectural Principles
- **Strict Human-in-the-Loop:** The LLM investigates and recommends; it NEVER executes actions. The Harness enforces approval gates (`INV-001`, `INV-002`).
- **Untrusted Model vs. Trusted Harness:** All LLM outputs must be validated by Pydantic v2 schemas (`InvestigationResult`).
- **Deterministic Math:** Aggregations and percentages must be computed in tool services, never in prompts.
- **Tenant Isolation:** All database queries must include `institution_id`.

### Tech Stack
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy/SQLModel, PostgreSQL.
- **Frontend:** React/Next.js, TypeScript strict mode.
- **Testing:** Pytest, pytest-asyncio, 25-case stratified evaluation dataset.

### Key Spec References
- Constitution & Invariants: `INVARIANTS.md`, `.sdd/00-constitution.md`
- Data Model: `.sdd/02-data-model-spec.md`
- API Contracts: `.sdd/03-api-contract.md`
- Architecture: `.sdd/05-architecture.md`
