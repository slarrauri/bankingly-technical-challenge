# ADR-002: Modular Monolith Architecture over Microservices

- **Date:** 2026-08-20  
- **Status:** Accepted  
- **Deciders:** Sebastián Larrauri (Technical Product Manager)

---

## 1. Context

We needed to select an architectural pattern for the PoC. Options considered were:
- **Option A:** Microservices architecture (separate services for Agent, Tools, Auth, Persistence).
- **Option B:** Modular Monolith (single codebase with explicit module boundaries in Python/FastAPI).

---

## 2. Decision

We chose a **Modular Monolith** structure (`backend/api`, `backend/harness`, `backend/agent`, `backend/tools`, `backend/domain`, `backend/evaluation`).

### Rationale:
- The dominant challenge is validating the cognitive workflow, agent harness security properties, and evaluation metrics, not solving distributed systems complexity or network latency overhead.
- High cohesion and shared in-process typing (Pydantic models) accelerate iteration and provide stronger safety guarantees.
- Modular design maintains clean domain boundaries that can be extracted into independent services in the future if required.

---

## 3. Consequences

- **Positive:** Fast build time, unified type checking, zero network serialization latency between harness and tools, simple local running via Docker Compose.
- **Trade-off:** Single deployment unit, which is optimal for MVP and PoC validation.
