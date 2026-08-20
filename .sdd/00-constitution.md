# 📜 00 — Project Constitution

> **Project:** AML Alert Investigation Copilot  
> **Status:** Baselined & Non-Negotiable  
> **Authority:** Supreme Authority over all code and specifications.

---

## 1. Mission Statement

Build a robust, explainable, and secure AI Copilot that automates preliminary investigations of Anti-Money Laundering (AML) alerts for financial institution compliance analysts, evaluating evidence against configured institutional policies and recommending concrete next steps while enforcing strict human approval before any action with side-effects is executed.

---

## 2. Non-Negotiable Principles

1. **Principle 1 (Human Authority Over Autonomous Action):**  
   The AI agent possesses zero autonomous execution authority. All actions affecting alert status, customer standing, or financial accounts require explicit, validated human approval signed by an authorized compliance analyst (`INV-001`, `INV-002`).

2. **Principle 2 (Trusted Harness vs. Untrusted LLM):**  
   The LLM is an untrusted reasoning engine. Application security, authentication, tenant isolation, input/output validation, and state machine transitions are enforced deterministically by the Python/FastAPI Agent Harness (`INV-009`).

3. **Principle 3 (Grounding Over Speculation):**  
   Every risk finding and policy citation must link directly to structured data evidence retrieved via authorized tools. Hallucinated findings or ungrounded assertions are treated as test failures (`INV-007`).

4. **Principle 4 (Explicit Uncertainty & Missing Data):**  
   When evidence is missing or contradictory, the system must explicitly identify the gaps in `missing_information` and recommend `REQUEST_INFORMATION` or `ESCALATE_ALERT` rather than guessing or fabricating conclusions (`INV-008`).

5. **Principle 5 (Deterministic Computation for Financial Metrics):**  
   Percentages, volume increases, historical averages, and transactional velocities must be computed by deterministic tool services (`get_transaction_summary`), never calculated inside LLM prompts.

6. **Principle 6 (Prompt Injection Resilience):**  
   All text extracted from transaction descriptions, counterparty notes, or customer comments must be processed as passive data arguments, never interpreted as system directives or policy overrides (`INV-006`).

7. **Principle 7 (Evaluation-First & Zero Unauthorized Execution):**  
   The benchmark dataset (25 stratified scenarios) is immutable and defined upfront. The system's Unauthorized Action Rate must be strictly **0.0%**.

---

## 3. Technology Constraints

| Layer | Technology Choice | Version | Rationale |
|---|---|---|---|
| **Backend Language** | Python | `>= 3.11` | Native typing, modern async support, rich data & AI ecosystem |
| **API Framework** | FastAPI | `>= 0.110` | High performance, OpenAPI auto-generation, async-native |
| **Data Validation** | Pydantic | `>= 2.7` | High-speed Rust-core validation, strict structured output parsing |
| **Persistence / ORM** | PostgreSQL + SQLAlchemy / SQLModel | `PG 15+` | ACID compliance, JSONB capabilities, enterprise banking standard |
| **LLM Provider Layer** | Provider Abstraction (Ollama / OpenAI / Gemini) | - | Model agnostic, local testing with Ollama, extensible to cloud LLMs |
| **Frontend Framework** | React / Next.js | Modern | High-density compliance console, clean component hierarchy |
| **Test Framework** | Pytest + pytest-asyncio | Modern | Comprehensive unit, security, integration, and eval runner |

---

## 4. Architectural Rules

1. **Modular Monolith:** Single unified repository with clean domain boundaries (`backend/domain`, `backend/harness`, `backend/tools`, `backend/api`, `backend/evaluation`). No microservices overhead.
2. **Tool Sandboxing:** Tools are read-only interfaces to PostgreSQL repositories. The LLM has no raw SQL access.
3. **Tenant Isolation:** Every data access query and tool invocation must be scoped by `institution_id` (`INV-005`).

---

## 5. Quality Standards & Definition of Done

- **Code Quality:** Strict type hints in Python and TypeScript. Zero lint warnings.
- **Test Coverage:** 100% test pass rate for all 10 Invariants (`INV-001` to `INV-010`).
- **Evaluation Gate:** All 25 evaluation benchmark cases executed with automated report generation.
- **Security Gate:** Unauthorized Action Rate = `0.0%`, Prompt Injection Defense = `100% pass`.
