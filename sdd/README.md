# 📐 SDD Specification Suite — AML Alert Investigation Copilot

> **Project:** AML Alert Investigation Copilot (Banco Río Sur)  
> **Methodology:** Spec-Driven Development (SDD)  
> **Status:** Baselined & Active

---

## 1. Specification Index & Reading Order

The specifications in this directory form the single source of truth for the system architecture, contracts, safety rules, and implementation breakdown.

```
00-constitution.md ─────────────────┐
  │                                  │
  ▼                                  ▼
01-product-requirements.md     INVARIANTS.md
  │
  ├──▶ 02-data-model-spec.md ──────▶ SQLAlchemy/SQLModel Models + Migrations
  │
  ├──▶ 03-api-contract.md ─────────▶ FastAPI Routers & Pydantic Schemas
  │
  ├──▶ 04-ui-ux-spec.md ───────────▶ React Compliance Console
  │
  └──▶ 05-architecture.md ────────▶ Modular Monolith + Harness + Tool Services
        │
        ├──▶ 06-implementation-plan.md
        ├──▶ 07-task-breakdown.md
        └──▶ 08-verification-spec.md ──▶ Pytest Suite + 25-Case Evals
```

### Layer 1: Product Specifications

| File | Document | Focus | Key Output |
|---|---|---|---|
| [`00-constitution.md`](sdd/00-constitution.md) | **Constitution** | Non-negotiable principles & stack constraints | Core governance & quality gates |
| [`01-product-requirements.md`](sdd/01-product-requirements.md) | **PRD** | Problem, target persona, prioritized workflows | Workflows P1–P4 & Acceptance criteria |
| [`02-data-model-spec.md`](sdd/02-data-model-spec.md) | **Data Model Spec** | ERD, entity schemas, state guards, seed strategy | PostgreSQL schema & seed dataset |
| [`03-api-contract.md`](sdd/03-api-contract.md) | **API Contract** | Endpoints, request/response models, error codes | FastAPI REST contracts & Pydantic schemas |
| [`04-ui-ux-spec.md`](sdd/04-ui-ux-spec.md) | **UI/UX Spec** | Compliance console wireframes, tokens, approval modal | Frontend design & interaction specifications |
| [`05-architecture.md`](sdd/05-architecture.md) | **Architecture Spec** | 5-layer modular monolith, sequence flows, state machine | Architectural topology & directory structure |
| [`06-implementation-plan.md`](sdd/06-implementation-plan.md) | **Implementation Plan** | Phased engineering roadmap & risk management | Sequential build strategy |
| [`07-task-breakdown.md`](sdd/07-task-breakdown.md) | **Task Breakdown** | Atomic tasks (T-001..T-035) with traceability | Work item execution backlog |
| [`08-verification-spec.md`](sdd/08-verification-spec.md) | **Verification Spec** | Test matrix, 25-case eval suite, E2E demo script | Quality gates & benchmark metrics |

### Layer 2-6: Extended Enterprise Specs

- [`09-git-strategy.md`](sdd/09-git-strategy.md) — Git workflow & branch conventions.
- [`10-cicd-pipeline.md`](sdd/10-cicd-pipeline.md) — CI automated testing & lint pipeline.
- [`14-security-spec.md`](sdd/14-security-spec.md) — Threat model & prompt injection mitigation.
- [`16-observability-spec.md`](sdd/16-observability-spec.md) — Structured audit logging & monitoring.
- [`18-performance-spec.md`](sdd/18-performance-spec.md) — SLOs and latency targets.
- [`22-glossary.md`](sdd/22-glossary.md) — Banking, AML & agentic terminology.
