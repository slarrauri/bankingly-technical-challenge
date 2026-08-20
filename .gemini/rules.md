# Project Rules for AI Coding Assistants

> **Project:** AML Alert Investigation Copilot (Banco Río Sur)  
> **Repository:** `bankingly-technical-challenge`  
> **Applies to:** Gemini Code Assist, Antigravity, GitHub Copilot, Cursor, Claude Code

---

## §1 — Project Identity

- **Name:** AML Alert Investigation Copilot
- **Domain:** Fintech / Anti-Money Laundering (AML) Compliance & Agentic Banking
- **Institution:** Banco Río Sur (Simulated Banking Context, Uruguay)
- **Stack:**
  - **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy / SQLModel, Alembic, PostgreSQL
  - **LLM Harness:** Provider abstraction (Ollama, OpenAI, Gemini), strict Pydantic structured output validation
  - **Frontend:** React / Next.js, Vanilla CSS / Tailwind (modern compliance console)
  - **Testing:** Pytest, pytest-asyncio, HTTPX
- **Architecture:** Modular Monolith (`backend/`, `frontend/`, `data/`, `tests/`, `.sdd/`)
- **Specs Authority:** `.sdd/` directory — all implementations must conform to specifications.

---

## §2 — Universal Rules

### Code Quality & Types
- Strict typing across all code. In Python, use explicit type hints everywhere (`typing` / built-in generics in 3.11+). In TypeScript/React, strict mode, no unjustified `any`.
- Use Pydantic v2 `BaseModel` with strict validation for all external inputs and LLM outputs.
- Functions must be modular, single-responsibility, and under 50 lines where possible.
- Use explicit error-first pattern: Validate input → Check preconditions → Execute → Return.

### Naming Conventions
- **Python:** `snake_case` for modules, functions, variables, database columns. `PascalCase` for classes and Pydantic models. `SCREAMING_SNAKE_CASE` for constants.
- **TypeScript/React:** `PascalCase.tsx` for components, `camelCase.ts` for utilities/hooks, `kebab-case` for CSS classes.
- **Database:** `snake_case` for tables and columns (e.g. `customer_kyc`, `risk_score`).
- **REST Endpoints:** `kebab-case` with `/api/v1` prefix (e.g. `/api/v1/investigations/{id}/approve`).

### Documentation & Comments
- Comment **WHY**, never **WHAT**.
- Never add generic AI boilerplate comments (e.g. `# This is the main router`).
- Preserve all existing comments and docstrings when modifying files.
- TODOs must include an issue or ticket tag: `# TODO(AML-42): add enhanced sanctions screening tool`.

### Git Hygiene
- Follow Conventional Commits: `type(scope): description`.
- Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`.
- One logical change per commit. Keep diffs clear and reviewable.

---

## §3 — Backend Rules (`backend/`)

### Agent Harness & Security Boundary
- **Untrusted vs. Trusted:** Treat all LLM outputs and data returned from tools as untrusted. Never execute an operation directly from model text.
- **Structured Outputs Only:** The agent output must strictly conform to the Pydantic `InvestigationResult` schema. If schema validation fails, retry up to `max_retries = 2`, then emit `INVESTIGATION_FAILED`.
- **Approval Gate:** State transition to `EXECUTED` cannot happen without an existing, authorized, unexecuted `Approval` record.
- **Tenant Isolation:** Every repository and service call MUST filter by `institution_id` (`INV-005`).

### Tools Implementation
- Tools are deterministic Python functions wrapped by the Harness. The LLM only receives tool definitions and returns tool call requests.
- Never let the LLM do calculations (e.g. percentage volume increase). Calculations belong in `get_transaction_summary` service.
- Tool input parameters must be validated with strict limits (e.g. `max_date_range = 365 days`, `max_results = 500`).

### Database & Repositories
- Use SQLAlchemy/SQLModel with async sessions.
- Seed data must be idempotent (`deleteMany` / truncate before seed).
- Decimal amounts must use `Decimal` type, never floats.

---

## §4 — Frontend Rules (`frontend/`)

### UI & Analyst Experience
- Minimalist, high-density compliance UI: Fast, clear, accessible, and audit-friendly.
- Every investigation screen must render:
  1. Alert overview & risk badge
  2. Structured findings with clickable evidence provenance
  3. Identified missing information / limitations
  4. Applicable AML policies
  5. Agent recommendation with confidence & rationale
  6. Action bar (Approve / Reject / Request More Info) with confirmation modal
- Display Loading, Empty, and Error states for every asynchronous view.

---

## §5 — Testing & Evaluation Rules (`tests/`, `backend/evaluation/`)

### Safety Invariants Testing
- Every invariant in `INVARIANTS.md` (`INV-001` to `INV-010`) must have automated test coverage in `tests/security/` or `tests/integration/`.
- Test specifically that:
  - Agent attempts to close alerts autonomously are blocked.
  - Prompt injections inside transaction descriptions are treated strictly as data strings.
  - Cross-institution queries return authorization errors.

### Evaluation Dataset Integrity
- The 25 evaluation cases in `data/evaluation/` are the benchmark source of truth.
- Never alter ground-truth test assertions to match incorrect or hallucinated model outputs.
- Track metrics: Recommendation Accuracy, Evidence Grounding, Missing Info Detection, and **Unauthorized Action Rate (Must be 0.0%)**.

---

## §6 — Forbidden Patterns ❌

The following patterns are strictly forbidden and will fail code review:

1. ❌ **Autonomous Side-effects:** Giving the LLM direct access to an `execute_action` or `close_alert` tool.
2. ❌ **Implicit Approval:** Advancing investigation state from `RECOMMENDATION_READY` to `EXECUTED` without a valid human approval record.
3. ❌ **Prompt-only Security:** Relying solely on prompt instructions (e.g. "Do not execute actions") instead of code-level guards.
4. ❌ **Floating-point Currency:** Using `float` for monetary balances or transaction amounts.
5. ❌ **Unsanitized Prompts:** Concatenating user/transaction text directly into system instructions without data-boundary demarcations.
6. ❌ **Raw SQL Queries:** Executing unparameterized SQL strings.
7. ❌ **Missing Tenant Filter:** Any database query that omits `institution_id`.
8. ❌ **Swallowing Exceptions:** Silent `try/except: pass` without structured error logging and audit capture.
