# 🏢 Guide: Enterprise SDD - Extended Artifact Catalog

> **Version:** 1.0  
> **Last Updated:** 2026-04-23  
> **Status:** Active

> **Purpose:** Map ALL artifacts needed for an enterprise-ready project beyond the base SDD specs.  
> **Audience:** Teams building production software with AI-assisted development workflows.

---
## 1. Artifact Landscape — What You Have vs. What You Need


```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ENTERPRISE SDD ARTIFACT MAP                         │
│                                                                        │
│  ┌─── LAYER 1: PRODUCT ─────────────────────────────────────────────┐ │
│  │  ✅ 00-constitution.md        ✅ 01-product-requirements.md       │ │
│  │  ✅ 02-data-model-spec.md     ✅ 03-api-contract.md              │ │
│  │  ✅ 04-ui-ux-spec.md          ✅ 05-architecture.md              │ │
│  │  ✅ 06-implementation-plan.md ✅ 07-task-breakdown.md             │ │
│  │  ✅ 08-verification-spec.md   ✅ GUIDE-ai-sdd-workflow.md        │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌─── LAYER 2: ENGINEERING PROCESS ─────────────────────────────────┐ │
│  │  🆕 09-git-strategy.md           Branch model, commit conventions │ │
│  │  🆕 10-cicd-pipeline.md          Build, test, deploy automation   │ │
│  │  🆕 11-environment-strategy.md   Dev→Staging→Prod matrix          │ │
│  │  🆕 12-release-management.md     Versioning, changelogs, rollback │ │
│  │  🆕 13-code-review-standards.md  PR process, review checklist     │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌─── LAYER 3: SECURITY & COMPLIANCE ───────────────────────────────┐ │
│  │  🆕 14-security-spec.md          Auth, RBAC, encryption, OWASP   │ │
│  │  🆕 15-data-governance.md        PII, retention, GDPR, backups   │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌─── LAYER 4: OPERATIONS ──────────────────────────────────────────┐ │
│  │  🆕 16-observability-spec.md     Logging, monitoring, alerting    │ │
│  │  🆕 17-incident-response.md      Runbooks, escalation, postmortem│ │
│  │  🆕 18-performance-spec.md       SLOs, load targets, scaling      │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌─── LAYER 5: AI AGENT CONFIGURATION ──────────────────────────────┐ │
│  │  🆕 .gemini/agents.md            Agent personas & capabilities    │ │
│  │  🆕 .gemini/rules.md             Global coding rules for AI      │ │
│  │  🆕 .gemini/skills.md            Reusable task templates          │ │
│  │  🆕 .github/copilot-instructions.md  GitHub Copilot context      │ │
│  │  🆕 .cursor/rules/               Cursor AI rules                 │ │
│  │  🆕 AGENTS.md                     Root-level agent orchestration  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌─── LAYER 6: KNOWLEDGE & ONBOARDING ──────────────────────────────┐ │
│  │  🆕 19-onboarding-guide.md       New developer quick-start        │ │
│  │  🆕 20-adr/                       Architecture Decision Records   │ │
│  │  🆕 21-dependency-policy.md      Package management, auditing     │ │
│  │  🆕 22-glossary.md               Domain terms & definitions       │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. When Do You Need What?

| Artifact | Solo MVP | Small Team (2-5) | Enterprise | Why |
|----------|:--------:|:-----------------:|:----------:|-----|
| **Layer 1: Product Specs** | ✅ | ✅ | ✅ | Always needed |
| 09 Git Strategy | ⚪ Simple | ✅ | ✅ | >1 developer = need branch rules |
| 10 CI/CD Pipeline | ⚪ Manual | ✅ | ✅ | Repeatable builds = fewer bugs |
| 11 Environment Strategy | ⚪ localhost | ✅ | ✅ | Staging catches prod issues |
| 12 Release Management | ⚪ Ship trunk | ⚪ Tags | ✅ | Versioning matters for customers |
| 13 Code Review Standards | ⚪ Self-review | ✅ | ✅ | PR quality = code quality |
| 14 Security Spec | ⚪ Basic | ✅ | ✅ | Auth + RBAC = non-negotiable |
| 15 Data Governance | ⚪ | ⚪ Basic | ✅ | GDPR/SOC2 compliance |
| 16 Observability | ⚪ console.log | ⚪ Basic | ✅ | Can't fix what you can't see |
| 17 Incident Response | ⚪ | ⚪ | ✅ | Outages need structured response |
| 18 Performance Spec | ⚪ | ⚪ SLOs | ✅ | Scale requirements need targets |
| **Layer 5: AI Agent Config** | ✅ | ✅ | ✅ | **Every project with AI dev** |
| 19 Onboarding Guide | ⚪ | ✅ | ✅ | New devs need fast ramp-up |
| 20 ADRs | ⚪ | ✅ | ✅ | "Why did we choose X?" |
| 21 Dependency Policy | ⚪ | ⚪ | ✅ | Supply chain security |
| 22 Glossary | ⚪ | ⚪ | ✅ | Domain language consistency |

---

## 3. Layer 2: Engineering Process

---

### 📄 09 — Git Strategy & Branch Model

```markdown
# Git Strategy

## Branch Model: GitHub Flow (Simplified)

For most projects, use GitHub Flow (not full GitFlow):

┌─────────────────────────────────────────────────┐
│                                                  │
│  main ──●──●──●──●──●──●──●──●──●──▶ (production)
│              \     /   \        /                 │
│          feat/auth  feat/dashboard               │
│                                                  │
│  • main is always deployable                     │
│  • Feature branches from main                    │
│  • Merge via PR with required reviews            │
│  • Delete branch after merge                     │
└─────────────────────────────────────────────────┘

## When to Use Full GitFlow Instead

Use GitFlow (main + develop + release branches) when:
- You have scheduled release cycles (not continuous delivery)
- You maintain multiple versions simultaneously (v1.x, v2.x)
- You need hotfix branches for emergency patches

┌─────────────────────────────────────────────────┐
│  main ────●─────────────●────────▶ (releases)    │
│           │             ↑                        │
│  release/ │     release/1.0                      │
│           │       ↑       \                      │
│  develop ─●──●──●──●──●──●──●──▶ (integration)  │
│              \  /  \     /                       │
│           feat/X  feat/Y                         │
│                                                  │
│  hotfix/ ────────────────────▶ (emergency only)  │
└─────────────────────────────────────────────────┘

## Branch Naming Convention

| Pattern | Example | Use |
|---------|---------|-----|
| `feat/{ticket}-{desc}` | `feat/BP-42-bill-lifecycle` | New features |
| `fix/{ticket}-{desc}` | `fix/BP-99-overdue-calc` | Bug fixes |
| `refactor/{desc}` | `refactor/extract-state-machine` | Code improvement |
| `docs/{desc}` | `docs/api-contract-v2` | Documentation |
| `chore/{desc}` | `chore/upgrade-prisma` | Maintenance |
| `hotfix/{desc}` | `hotfix/payment-race-condition` | Emergency production fix |

## Commit Message Convention (Conventional Commits)


<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code change that neither fixes bug nor adds feature |
| `test` | Adding or fixing tests |
| `chore` | Build process, dependencies, tooling |
| `perf` | Performance improvement |

Examples:
```
feat(bills): add bulk approve action
fix(dashboard): correct overdue count excluding archived bills
docs(api): update payment cancel endpoint schema
refactor(routes): extract state machine validation to shared module
chore(deps): upgrade prisma to 6.7.0
```

## Merge Strategy

| Scenario | Strategy | Why |
|----------|----------|-----|
| Feature → main | **Squash merge** | Clean history, one commit per feature |
| Release → main | **Merge commit** | Preserve full history for audit |
| Hotfix → main | **Merge commit** | Traceability for post-mortems |

## Protected Branch Rules (main)

- [ ] Require pull request before merging
- [ ] Require at least 1 approval
- [ ] Require status checks to pass (CI/CD)
- [ ] Require branches to be up to date before merging
- [ ] Require linear history (squash merges)
- [ ] Do not allow force pushes
- [ ] Do not allow deletions
---

### 📄 10 — CI/CD Pipeline

```markdown
# CI/CD Pipeline Specification

## Pipeline Stages

```yaml
# .github/workflows/ci.yml (conceptual)

trigger: push to any branch + PR to main

stages:
  ┌─── LINT ──────────────────────────┐
  │ • TypeScript type-check (tsc)     │
  │ • ESLint (if configured)          │
  │ • Prettier format check           │
  └──────────┬────────────────────────┘
             ↓
  ┌─── TEST ──────────────────────────┐
  │ • Unit tests (Vitest/Jest)        │
  │ • API integration tests           │
  │ • Component tests                 │
  └──────────┬────────────────────────┘
             ↓
  ┌─── BUILD ─────────────────────────┐
  │ • Vite production build (client)  │
  │ • TypeScript compile (server)     │
  │ • Docker image build              │
  └──────────┬────────────────────────┘
             ↓ (only on main)
  ┌─── DEPLOY ────────────────────────┐
  │ • Push Docker image to registry   │
  │ • Deploy to staging (auto)        │
  │ • Deploy to production (manual)   │
  └───────────────────────────────────┘
```

## Environment Matrix

| Branch | Lint | Test | Build | Deploy |
|--------|:----:|:----:|:-----:|:------:|
| Feature branch | ✅ | ✅ | ✅ | ❌ |
| PR to main | ✅ | ✅ | ✅ | Preview |
| main (merged) | ✅ | ✅ | ✅ | Staging (auto) |
| Release tag | ✅ | ✅ | ✅ | Production (manual gate) |


---

### 📄 11 — Environment Strategy

```markdown
# Environment Strategy

| Environment | Purpose | URL | Database | Deploy Trigger |
|-------------|---------|-----|----------|----------------|
| **Local** | Individual development | localhost:5173 | Docker Compose (local PG) | Manual |
| **Preview** | PR review | pr-{n}.preview.app.com | Ephemeral DB (seeded) | Auto on PR |
| **Staging** | Pre-production validation | staging.app.com | Persistent (copy of prod schema) | Auto on main merge |
| **Production** | Live users | app.com | Production DB (managed) | Manual gate after staging ✅ |

## Environment Variables Per Stage

| Variable | Local | Staging | Production |
|----------|-------|---------|------------|
| `DATABASE_URL` | localhost:5432 | staging-db.internal | prod-db.internal |
| `NODE_ENV` | development | staging | production |
| `CORS_ORIGIN` | http://localhost:5173 | https://staging.app.com | https://app.com |
| `LOG_LEVEL` | debug | info | warn |
| `SEED_DATA` | true | true | **false** |
```

---

### 📄 12-13 — Release Management & Code Review

```markdown
# Release Management

## Versioning: Semantic Versioning (SemVer)

MAJOR.MINOR.PATCH (e.g., 1.4.2)

| Increment | When | Example |
|-----------|------|---------|
| MAJOR | Breaking API changes | 1.0.0 → 2.0.0 |
| MINOR | New features (backward compatible) | 1.0.0 → 1.1.0 |
| PATCH | Bug fixes | 1.0.0 → 1.0.1 |

## Release Process

1. Create release branch from `main`
2. Update version in `package.json`
3. Generate changelog from conventional commits
4. Create GitHub Release with tag `v{version}`
5. CI/CD builds + pushes Docker image tagged with version
6. Deploy to staging → smoke test → deploy to production

---

# Code Review Standards

## PR Requirements

- [ ] Title follows conventional commit format
- [ ] Description explains WHAT and WHY (not just HOW)
- [ ] Links to spec artifact (e.g., "Implements API Contract §2.6")
- [ ] Self-reviewed before requesting review
- [ ] No console.log / debug artifacts
- [ ] No commented-out code
- [ ] All CI checks passing

## Reviewer Checklist

- [ ] Code matches the spec
- [ ] Error handling covers edge cases
- [ ] No security vulnerabilities (SQL injection, XSS, etc.)
- [ ] Types are correct (no `any` without justification)
- [ ] State machine transitions are validated
- [ ] Responsive behavior is correct
- [ ] Loading/empty/error states present
```

---

## 4. Layer 3: Security & Compliance

```markdown
# 14 — Security Specification

## Authentication

| Aspect | Specification |
|--------|---------------|
| Method | JWT (access + refresh tokens) |
| Access token TTL | 15 minutes |
| Refresh token TTL | 7 days |
| Storage | HttpOnly, Secure, SameSite=Strict cookies |
| Password hashing | bcrypt (cost factor 12) |
| MFA | TOTP (optional, recommended for admin) |

## Authorization (RBAC)

| Role | Bills | Payments | Vendors | Dashboard | Users |
|------|-------|----------|---------|-----------|-------|
| **Admin** | Full CRUD + lifecycle | Full + cancel | Full CRUD | View | Manage |
| **AP Manager** | Full CRUD + lifecycle | View + cancel | View | View | ❌ |
| **AP Clerk** | Create + submit | View | View | View | ❌ |
| **Approver** | View + approve/reject | View | View | View | ❌ |
| **Viewer** | Read-only | Read-only | Read-only | View | ❌ |

## OWASP Top 10 Mitigations

| Threat | Mitigation |
|--------|------------|
| Injection | Prisma parameterized queries (never raw SQL) |
| Broken Auth | JWT + HttpOnly cookies + rate limiting |
| Sensitive Data Exposure | HTTPS everywhere, no secrets in code |
| XSS | React auto-escapes, CSP headers |
| CSRF | SameSite cookies + CSRF tokens on mutations |
| Mass Assignment | Explicit field picking in PATCH handlers |
| Security Misconfiguration | Helmet.js, no stack traces in production |

## API Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```
```

---

## 5. Layer 4: Operations

```markdown
# 16 — Observability Specification

## Logging

| Level | When | Example |
|-------|------|---------|
| `error` | Something broke | Failed DB query, unhandled exception |
| `warn` | Something unexpected but handled | Invalid state transition attempt |
| `info` | Significant business event | Bill approved, payment completed |
| `debug` | Developer troubleshooting | Query parameters, response timing |

Format: Structured JSON logs
```json
{
  "timestamp": "2026-04-17T10:00:00Z",
  "level": "info",
  "message": "Bill approved",
  "billId": "uuid",
  "userId": "uuid",
  "duration_ms": 45
}
```

## Monitoring & Alerting

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API response time (p95) | < 200ms | > 500ms for 5 min |
| Error rate | < 0.1% | > 1% for 5 min |
| Database connections | < 80% pool | > 90% pool |
| Disk usage | < 70% | > 85% |
| Uptime | 99.9% | Any downtime |

## Health Check Endpoint

```
GET /api/health → { status: "ok", db: "connected", uptime: "12h 30m" }
```

---

# 18 — Performance Specification

## SLOs (Service Level Objectives)

| Metric | SLO | Measurement |
|--------|-----|-------------|
| **Availability** | 99.9% uptime | Synthetic monitoring, 1-min intervals |
| **Latency** | p95 < 200ms | APM tracing on all API endpoints |
| **Throughput** | 100 req/sec sustained | Load testing (k6/Artillery) |
| **Time to First Byte** | < 500ms | Real User Monitoring |

## Scaling Strategy

| Component | Strategy | Trigger |
|-----------|----------|---------|
| API Server | Horizontal (add replicas) | CPU > 70% or req/sec > 80 |
| Database | Vertical first, then read replicas | Connection pool > 80% |
| Static Assets | CDN (CloudFront/Cloudflare) | Always-on |
```

---

## 6. Layer 5: AI Agent Configuration 🤖

This is **the most important new layer** for modern AI-assisted development. These files tell AI coding agents how to work in YOUR specific project.

---

### 📄 AGENTS.md — Agent Orchestration

Place at project root. Defines which AI agents exist and what they can do.

```markdown
# AGENTS.md

## Project: Bill Pay — Accounts Payable Management

### Available Agents

#### 🏗️ Architect Agent
- **Scope:** System design, data modeling, API design
- **Can modify:** `.sdd/` specs, `prisma/schema.prisma`, architecture docs
- **Cannot modify:** Implementation code directly
- **Consult when:** Evaluating new features, schema changes, breaking changes
- **References:** `.sdd/00-constitution.md`, `.sdd/05-architecture.md`

#### 💻 Backend Agent
- **Scope:** Server-side code (Express routes, Prisma queries, middleware)
- **Can modify:** `server/src/**/*.ts`, `server/prisma/seed.ts`
- **Cannot modify:** Client code, Prisma schema (propose changes to Architect)
- **Rules file:** `.gemini/rules.md` → Backend section
- **References:** `.sdd/03-api-contract.md`, `.sdd/02-data-model-spec.md`

#### 🎨 Frontend Agent
- **Scope:** React components, pages, styling, client-side logic
- **Can modify:** `client/src/**/*.tsx`, `client/src/**/*.css`
- **Cannot modify:** Server code, API contracts
- **Rules file:** `.gemini/rules.md` → Frontend section
- **References:** `.sdd/04-ui-ux-spec.md`, `.sdd/03-api-contract.md`

#### 🧪 QA Agent
- **Scope:** Test writing, verification, bug detection
- **Can modify:** `**/*.test.ts`, `**/*.spec.ts`, test utilities
- **Cannot modify:** Production code
- **References:** `.sdd/08-verification-spec.md`

#### 📝 Docs Agent
- **Scope:** README, changelogs, API docs, onboarding guides
- **Can modify:** `*.md`, `docs/**`
- **Cannot modify:** Source code
- **References:** All `.sdd/` files

### Agent Interaction Rules

1. **Spec-first:** Before modifying code, check if relevant spec exists.
   If it does, follow it. If it needs updating, propose the spec change first.
2. **Constitution compliance:** Every change must comply with `00-constitution.md`.
3. **Cross-boundary changes:** If a task spans multiple agents' scopes,
   the Architect Agent coordinates.
4. **Traceability:** Every PR should reference the spec it implements:
   "Implements `.sdd/03-api-contract.md` §2.6 (Bill Submit)"
```

---

### 📄 .gemini/rules.md — Global AI Coding Rules

These rules are injected into every AI session automatically.

```markdown
# Project Rules for AI Coding Assistants

## Identity
- Project: Bill Pay (Trashlab)
- Stack: TypeScript, Express 5, React 19, Prisma, PostgreSQL, Vanilla CSS
- Monorepo: `server/` (backend) + `client/` (frontend)

## Universal Rules

### Code Style
- TypeScript strict mode. No `any` without a `// justified:` comment.
- Functional components only (React). No class components.
- Named exports only. No default exports.
- Use `const` by default. `let` only when reassignment is needed.
- Async/await over `.then()` chains.
- Destructure function parameters when >2 properties.

### Error Handling
- API routes: try/catch → `res.status(XXX).json({ error: message })`.
- Frontend: Loading, Empty, and Error states for EVERY data-fetching view.
- Never swallow errors silently. At minimum, `console.error()` in development.

### State Machine
- Bill status transitions MUST be validated on the backend.
- Frontend MUST use `getAvailableActions(status)` to determine valid buttons.
- Never hardcode status strings — use the enum/type definitions.

### Styling
- All styles in `client/src/index.css`. No inline styles except layout.
- Use CSS custom properties from `:root`. Never hardcode colors.
- Every interactive element needs: hover, focus, disabled states.

### API Conventions
- Base path: `/api`
- List endpoints return: `{ data: T[], pagination: {...} }`
- Error responses return: `{ error: string }`
- Use PATCH for partial updates, not PUT.
- Status transitions: `POST /api/{entity}/:id/{action}`

### Documentation
- Preserve all existing comments when modifying files.
- Do NOT add AI boilerplate comments ("This function does X").
- Only add comments that explain WHY, not WHAT.

### Git
- Commit messages: Conventional Commits format.
- One logical change per commit. No "fix everything" commits.

## Backend-Specific Rules

### Prisma
- Always use `include` for related entities in responses.
- Use `Prisma.Decimal` for monetary values, never `parseFloat`.
- Seed data must use `deleteMany` before creating (idempotent).

### Express
- Route handlers: validate required fields → check preconditions → execute → respond.
- Use `Router()` per entity. Mount on `app.use("/api/{entity}", router)`.
- Never send a response after another response (no double `res.json()`).

## Frontend-Specific Rules

### React
- No `useEffect` for derived state — compute directly in render.
- URL-driven state for table views (searchParams, not useState).
- Fetch data in page components, pass down to display components.
- No global state library — useState + prop drilling for MVP.

### CSS
- Mobile-first is NOT required (desktop-first is fine for admin tools).
- Tables transform to cards on mobile via `data-label` + `::before`.
- Modals become fullscreen on small mobile with sticky header/footer.
```

---

### 📄 .gemini/skills.md — Reusable Task Templates

Skills are **parameterized prompt templates** that agents can invoke.

```markdown
# Skills — Reusable AI Task Templates

## Skill: Add CRUD Endpoint

### Parameters
- `{entity}`: Entity name (e.g., "Vendor")
- `{fields}`: List of fields from data model spec
- `{guards}`: Business rules for create/update/delete

### Instructions
1. Open `.sdd/03-api-contract.md` and find the `{entity}` section.
2. Create route file: `server/src/routes/{entity_lowercase}.ts`
3. Implement endpoints following API contract exactly:
   - GET / (list with pagination)
   - GET /:id (single with includes)
   - POST / (create with field validation)
   - PATCH /:id (update with guards: {guards})
   - DELETE /:id (with guards: {guards})
4. Mount router in `server/src/index.ts`
5. Add TypeScript interface in `client/src/types/index.ts`

---

## Skill: Add Page with Table

### Parameters
- `{pageName}`: e.g., "VendorsPage"
- `{entity}`: e.g., "Vendor"
- `{columns}`: Columns to display
- `{actions}`: Row-level actions available

### Instructions
1. Open `.sdd/04-ui-ux-spec.md` § Page Specifications for `{pageName}`.
2. Create `client/src/pages/{pageName}.tsx`
3. Implement:
   - Data fetching with `api.get` + loading/empty/error states
   - Table with columns: {columns}
   - Row actions: {actions}
   - Header with title, count, and "Create" button
4. Add route in `client/src/App.tsx`
5. Add NavLink in `client/src/components/Layout.tsx`

---

## Skill: Add State Transition

### Parameters
- `{action}`: e.g., "approve"
- `{sourceStatus}`: e.g., "PENDING_APPROVAL"
- `{targetStatus}`: e.g., "APPROVED"
- `{timestampField}`: e.g., "approvedAt"

### Instructions
1. Add backend route: `POST /api/bills/:id/{action}`
   - Validate current status is `{sourceStatus}`
   - Update to `{targetStatus}`, set `{timestampField}` to `new Date()`
   - Return updated bill with includes
2. Add to `getAvailableActions()` in `BillDetailPage.tsx`
3. Add to `ACTION_CONFIG` with label, button class, and optional confirm message
4. Add to bulk action handler if applicable
5. Update `.sdd/08-verification-spec.md` with test case

---

## Skill: Add Responsive Breakpoint

### Parameters
- `{width}`: e.g., "768px"
- `{changes}`: What transforms at this width

### Instructions
1. Add `@media (max-width: {width})` section to `client/src/index.css`
2. Implement {changes}
3. Test at exactly {width} and 1px below
4. Verify no horizontal overflow
5. Update `.sdd/04-ui-ux-spec.md` § Responsive Behavior table
```

---

### 📄 Other AI Tool Configurations

#### `.github/copilot-instructions.md` (GitHub Copilot)

```markdown
# GitHub Copilot Instructions

This is a TypeScript monorepo with Express 5 backend and React 19 frontend.

When generating code:
- Use TypeScript strict mode, no `any`
- Use named exports, not default exports
- Use async/await, not .then() chains
- API error responses: `{ error: string }` with appropriate HTTP status
- Use Prisma for all database operations
- Use CSS custom properties for all colors/spacing
- Follow Conventional Commits for commit messages

Key files to reference:
- Data model: server/prisma/schema.prisma
- API patterns: server/src/routes/bills.ts
- Component patterns: client/src/components/StatusBadge.tsx
- Style tokens: client/src/index.css (:root block)
- Types: client/src/types/index.ts
```

#### `.cursor/rules/project.mdc` (Cursor AI)

```markdown
---
description: Bill Pay project rules
globs: ["**/*.ts", "**/*.tsx", "**/*.css"]
---

# Project Rules
- TypeScript strict, no `any`
- Express 5 with Router pattern
- React 19 functional components, named exports
- Vanilla CSS with custom properties
- Prisma ORM, PostgreSQL
- API: /api prefix, { data, pagination } envelope for lists
- Errors: { error: string } with HTTP status codes
- State machine: validate transitions on backend, reflect on frontend
- Styling: use CSS variables from :root, never hardcode colors
```

---

## 7. Layer 6: Knowledge & Onboarding

```markdown
# 19 — Onboarding Guide

## First Day Checklist

1. [ ] Clone the repository
2. [ ] Read `README.md` (10 min)
3. [ ] Read `.sdd/README.md` — understand the SDD artifact structure (5 min)
4. [ ] Read `.sdd/00-constitution.md` — the rules (10 min)
5. [ ] Read `.sdd/01-product-requirements.md` — what we're building (10 min)
6. [ ] Run the app: `docker compose up -d && npm run install:all && npm run db:setup && npm run dev`
7. [ ] Walk through the E2E scenario in `.sdd/08-verification-spec.md` §6 (15 min)
8. [ ] Read `.gemini/rules.md` to understand AI coding conventions
9. [ ] Pick your first task from `.sdd/07-task-breakdown.md`
10. [ ] Create a feature branch following `09-git-strategy.md` naming conventions

## Key Files to Know

| File | Why |
|------|-----|
| `server/prisma/schema.prisma` | The data model — everything starts here |
| `server/src/routes/bills.ts` | The largest, most complex route file — good reference |
| `client/src/index.css` | The entire design system in one file |
| `client/src/types/index.ts` | All TypeScript interfaces |
| `client/src/pages/BillDetailPage.tsx` | Most complex frontend component |

---

# 20 — Architecture Decision Records (ADR) Template

## ADR-{NNN}: {Title}

**Date:** YYYY-MM-DD  
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX  
**Deciders:** {names}

### Context
What is the problem or decision we need to make?

### Decision
What did we decide and why?

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Option A | ... | ... |
| Option B | ... | ... |

### Consequences
What are the positive and negative impacts of this decision?

---

# 22 — Glossary

| Term | Definition |
|------|------------|
| **Bill** | An invoice from a vendor representing money owed by the company |
| **Vendor** | A supplier or service provider that the company pays |
| **Payment** | The record of money transferred to settle a bill |
| **AP** | Accounts Payable — the department/function managing outgoing payments |
| **Draft** | A bill that has been entered but not yet submitted for review |
| **Lifecycle** | The sequence of status transitions a bill goes through |
| **Overdue** | A bill whose due date has passed without being paid |
| **Bulk Action** | Applying a status transition to multiple bills simultaneously |
```

---

## 8. Complete File Tree — Enterprise Project

```
project-root/
├── .sdd/                              # SDD Specifications (Layer 1)
│   ├── README.md                      # Index + methodology
│   ├── GUIDE-ai-sdd-workflow.md       # AI interaction guide
│   ├── 00-constitution.md
│   ├── 01-product-requirements.md
│   ├── 02-data-model-spec.md
│   ├── 03-api-contract.md
│   ├── 04-ui-ux-spec.md
│   ├── 05-architecture.md
│   ├── 06-implementation-plan.md
│   ├── 07-task-breakdown.md
│   ├── 08-verification-spec.md
│   ├── 09-git-strategy.md             # Layer 2: Process
│   ├── 10-cicd-pipeline.md
│   ├── 11-environment-strategy.md
│   ├── 12-release-management.md
│   ├── 13-code-review-standards.md
│   ├── 14-security-spec.md            # Layer 3: Security
│   ├── 15-data-governance.md
│   ├── 16-observability-spec.md       # Layer 4: Operations
│   ├── 17-incident-response.md
│   ├── 18-performance-spec.md
│   ├── 19-onboarding-guide.md         # Layer 6: Knowledge
│   ├── 20-adr/                        # Architecture Decision Records
│   │   ├── ADR-001-prisma-over-typeorm.md
│   │   ├── ADR-002-vanilla-css-over-tailwind.md
│   │   └── ...
│   ├── 21-dependency-policy.md
│   └── 22-glossary.md
│
├── .gemini/                           # Layer 5: AI Agent Config (Gemini)
│   ├── rules.md                       # Global coding rules
│   └── skills.md                      # Reusable task templates
│
├── .github/
│   ├── copilot-instructions.md        # GitHub Copilot context
│   └── workflows/
│       ├── ci.yml                     # CI pipeline
│       ├── deploy-staging.yml         # Staging deployment
│       └── deploy-production.yml      # Production deployment
│
├── .cursor/rules/                     # Cursor AI rules
│   └── project.mdc
│
├── AGENTS.md                          # Agent orchestration (root-level)
├── CHANGELOG.md                       # Release history
├── README.md                          # Product + setup docs
├── client/                            # Frontend
├── server/                            # Backend
├── docker-compose.yml                 # Dev environment
├── docker-compose.prod.yml            # Production environment
└── Dockerfile                         # Container build
```

---

## 9. Summary: What to Create and When

### For your NEXT project, create artifacts in this order:

```
START HERE
    │
    ▼
┌─ Phase A: Before ANY Code ──────────────────────────────┐
│  1. AGENTS.md + .gemini/rules.md  (AI knows your project)│
│  2. 00-constitution.md            (rules of the game)    │
│  3. 01-product-requirements.md    (what to build)        │
│  4. 02-data-model-spec.md         (domain model)         │
│  5. 03-api-contract.md            (backend interface)    │
│  6. 04-ui-ux-spec.md              (frontend design)      │
│  7. 05-architecture.md            (how it fits together)  │
│  8. 09-git-strategy.md            (how we collaborate)    │
└──────────────────────────────────────────────────────────┘
    │
    ▼
┌─ Phase B: Before First Sprint ──────────────────────────┐
│  9. 06-implementation-plan.md     (phased roadmap)       │
│ 10. 07-task-breakdown.md          (sprint backlog)       │
│ 11. 08-verification-spec.md       (acceptance tests)     │
│ 12. .gemini/skills.md             (reusable AI patterns) │
│ 13. 10-cicd-pipeline.md           (automation)           │
│ 14. 11-environment-strategy.md    (deploy targets)       │
└──────────────────────────────────────────────────────────┘
    │
    ▼
┌─ Phase C: Before Going to Production ───────────────────┐
│ 15. 14-security-spec.md           (auth + RBAC + OWASP)  │
│ 16. 16-observability-spec.md      (logging + monitoring)  │
│ 17. 18-performance-spec.md        (SLOs + load targets)   │
│ 18. 12-release-management.md      (versioning + changelog)│
│ 19. 13-code-review-standards.md   (PR quality)            │
│ 20. 19-onboarding-guide.md        (team scaling)          │
└──────────────────────────────────────────────────────────┘
    │
    ▼
┌─ Phase D: Ongoing ──────────────────────────────────────┐
│ 21. 20-adr/ (as decisions are made)                      │
│ 22. 15-data-governance.md (when handling PII)            │
│ 23. 17-incident-response.md (after first incident)       │
│ 24. 21-dependency-policy.md (when team grows)            │
│ 25. 22-glossary.md (when onboarding frequently)          │
└──────────────────────────────────────────────────────────┘
```

> **The key insight:** AI agent configuration (AGENTS.md, rules.md, skills.md) should be created **FIRST** — even before the constitution. This ensures that from the very first prompt, the AI is aligned with your project's standards.
