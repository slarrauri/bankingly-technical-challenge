# 🤖 Guide: Configuring AI Coding Agents for Your Project

> **Version:** 1.0  
> **Last Updated:** 2026-04-23  
> **Status:** Active

> **Objective:** Define how to create, structure, and maintain AI agent configuration files (`AGENTS.md`, `rules.md`, `skills.md`, and tool-specific configs) so that every AI coding assistant that touches your project produces consistent, spec-compliant code from day one.
>
> **Audience:** Developers and tech leads who use AI coding assistants (Gemini, Copilot, Cursor, Claude, etc.) and want to standardize how those agents behave in their specific codebase.

---

## Table of Contents

1. [Why Configure AI Agents?](#1-why-configure-ai-agents)
2. [The Agent Configuration Landscape](#2-the-agent-configuration-landscape)
3. [File Placement & Discovery](#3-file-placement--discovery)
4. [AGENTS.md — Agent Orchestration](#4-agentsmd--agent-orchestration)
5. [rules.md — Global Coding Rules](#5-rulesmd--global-coding-rules)
6. [skills.md — Reusable Task Templates](#6-skillsmd--reusable-task-templates)
7. [Tool-Specific Configurations](#7-tool-specific-configurations)
8. [Writing Effective Rules](#8-writing-effective-rules)
9. [Writing Effective Skills](#9-writing-effective-skills)
10. [The Configuration Workflow](#10-the-configuration-workflow)
11. [Prompt Templates for Generating Configs](#11-prompt-templates-for-generating-configs)
12. [Anti-Patterns to Avoid](#12-anti-patterns-to-avoid)
13. [Maintaining Configs Over Time](#13-maintaining-configs-over-time)
14. [Cross-Tool Compatibility Matrix](#14-cross-tool-compatibility-matrix)
15. [Checklist: Agent Configuration Completeness](#15-checklist-agent-configuration-completeness)
16. [Real-World Examples](#16-real-world-examples)

---

## 1. Why Configure AI Agents?

Without configuration, every AI coding assistant starts from zero context. It guesses your conventions, invents patterns, and produces code that *works* but doesn't *fit*.

| Without Agent Config | With Agent Config |
|---------------------|-------------------|
| AI uses `default export` | AI knows you use `named exports` |
| AI picks Tailwind CSS | AI knows you use vanilla CSS custom properties |
| AI writes `console.log` for errors | AI writes structured JSON logs with your format |
| AI creates flat route files | AI follows your Router pattern with your middleware stack |
| AI names branches `fix-stuff` | AI names branches `fix/BP-42-overdue-calc` |
| AI adds boilerplate comments | AI only adds comments that explain *why* |
| Every developer gets different AI output | Everyone gets consistent, project-aligned output |

### The Core Principle

> **Agent configs are your project's "onboarding document" for AI.**
>
> Just as you'd give a new developer a style guide, coding standards, and
> architecture overview — agent configs give the same context to your AI.
>
> The difference: humans can infer. AI needs explicit instruction.

### The ROI

```
Time to write agent configs:     ~1-2 hours
Time saved per AI interaction:   ~5-15 minutes
Break-even after:                ~10-20 interactions
Lifetime savings across team:    Hundreds of hours
```

---

## 2. The Agent Configuration Landscape

```
┌─────────────────────────────────────────────────────────────────────┐
│                  AI AGENT CONFIG ECOSYSTEM                          │
│                                                                     │
│  ┌─── LAYER A: Universal (All AI Tools) ────────────────────────┐  │
│  │                                                               │  │
│  │  AGENTS.md          WHO does what, scope, permissions         │  │
│  │  rules.md           HOW to write code (conventions, patterns) │  │
│  │  skills.md          WHAT to do (reusable task templates)      │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                          ↓ consumed by ↓                            │
│  ┌─── LAYER B: Tool-Specific Configs ───────────────────────────┐  │
│  │                                                               │  │
│  │  .gemini/rules.md            Gemini Code Assist / Antigravity │  │
│  │  .gemini/settings.json       Gemini tool settings             │  │
│  │  .github/copilot-instructions.md    GitHub Copilot            │  │
│  │  .cursor/rules/*.mdc         Cursor AI rules                  │  │
│  │  .claude/project-instructions.md    Claude Code               │  │
│  │  .windsurfrules              Windsurf/Codeium                 │  │
│  │  .aider.conf.yml             Aider                            │  │
│  │  cline_docs/                 Cline                            │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                          ↓ references ↓                             │
│  ┌─── LAYER C: SDD Specs (Source of Truth) ─────────────────────┐  │
│  │                                                               │  │
│  │  .sdd/00-constitution.md     Principles AI must follow        │  │
│  │  .sdd/02-data-model-spec.md  Schema AI must match             │  │
│  │  .sdd/03-api-contract.md     Endpoints AI must implement      │  │
│  │  .sdd/04-ui-ux-spec.md       Design tokens AI must use        │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### The Three Questions

| File | Answers | Analogy |
|------|---------|---------|
| **AGENTS.md** | *Who* does what? | Org chart |
| **rules.md** | *How* should code be written? | Style guide |
| **skills.md** | *What* are the recurring tasks? | Playbook |

---

## 3. File Placement & Discovery

AI tools discover config files by scanning known paths. Here's where each tool looks:

```
project-root/
│
├── AGENTS.md                    # Root-level (all tools can find it)
│
├── .gemini/                     # Gemini-specific
│   ├── rules.md                 # Auto-loaded by Gemini
│   ├── skills.md                # Referenced by Gemini agents
│   └── settings.json            # Tool behavior settings
│
├── .github/
│   └── copilot-instructions.md  # Auto-loaded by GitHub Copilot
│
├── .cursor/
│   └── rules/
│       ├── global.mdc           # Applied to all files
│       ├── backend.mdc          # Applied to server/**
│       └── frontend.mdc         # Applied to client/**
│
├── .claude/
│   └── project-instructions.md  # Auto-loaded by Claude Code
│
├── .windsurfrules               # Auto-loaded by Windsurf
├── .aider.conf.yml              # Auto-loaded by Aider
│
├── cline_docs/                  # Cline memory bank
│   ├── projectBrief.md
│   ├── techContext.md
│   └── codebaseSummary.md
│
└── .sdd/                        # SDD specs (referenced by all configs)
    ├── 00-constitution.md
    └── ...
```

### Discovery Priority

When an AI tool starts a session, it typically reads configs in this order:

```
1. Tool-specific config (e.g., .gemini/rules.md)
2. Root-level configs (AGENTS.md)
3. User-level rules (global settings outside the repo)
4. File-level context (open files, cursor position)
```

### 🔑 Key Principle: Write Once, Adapt Per Tool

Write your conventions in **universal format** (AGENTS.md + rules.md + skills.md), then create thin **tool-specific adapters** that reference or excerpt from the universal files. This avoids maintaining duplicated rules across 5 different tools.

---

## 4. AGENTS.md — Agent Orchestration

### Purpose

Define **who** the agents are, what each is responsible for, what files they can touch, and how they should coordinate. Think of it as the **org chart** for AI in your project.

### When You Need It

- Always, if you use any AI coding assistant
- Especially when multiple people (or multiple AI tools) work on the same codebase
- Critical when AI has different roles (architect vs implementer vs reviewer)

### Structure Template

```markdown
# AGENTS.md

## Project Context

- **Project:** [name] — [one-line description]
- **Stack:** [languages, frameworks, database]
- **Architecture:** [monorepo/monolith/microservices]
- **SDD Specs:** `.sdd/` directory contains all specifications

---

## Agent Definitions

### 🏗️ [Agent Name]

- **Role:** [What this agent persona does]
- **Scope:** [Which parts of the codebase]
- **Can Modify:** [file patterns: `server/src/**/*.ts`]
- **Cannot Modify:** [file patterns or areas]
- **Must Reference:** [spec files to consult before acting]
- **Key Rules:**
  - [Rule 1 specific to this agent]
  - [Rule 2 specific to this agent]

---

## Interaction Protocol

### Before Any Code Change
1. Check if a relevant SDD spec exists in `.sdd/`
2. Read `.gemini/rules.md` for coding conventions
3. If the change spans multiple agent scopes, coordinate via spec update first

### Conflict Resolution
- SDD specs override agent judgment
- Constitution (`00-constitution.md`) is supreme authority
- When specs conflict, ask the human — don't guess
```

### How Many Agents Do You Need?

| Project Size | Recommended Agents |
|-------------|-------------------|
| Solo / MVP | 1 general-purpose agent (just use rules.md) |
| Small team (2-5) | 2-3 agents: Backend, Frontend, Ops |
| Enterprise | 4-6 agents: Architect, Backend, Frontend, QA, Docs, DevOps |

### Prompt to Generate AGENTS.md

```markdown
I need an AGENTS.md for my project. Here's the context:

**Project:** [name and description]
**Stack:** [full tech stack]
**Team Structure:** [who works on what]
**Codebase Structure:**
- `server/` — Backend (Express + Prisma)
- `client/` — Frontend (React + Vite)
- `infra/` — Docker + CI/CD

**AI Tools Used:** [Gemini, Copilot, Cursor, etc.]

Define agents with:
1. Clear scope boundaries (which files each agent owns)
2. Explicit permissions (can/cannot modify)
3. Required spec references before acting
4. Interaction protocols for cross-boundary changes

Make the agents map to the natural boundaries of the codebase,
not to artificial roles.
```

### Review Checklist
- [ ] Every source file is covered by at least one agent's scope
- [ ] No two agents have overlapping "can modify" permissions for the same file
- [ ] Every agent has at least one "must reference" spec
- [ ] Cross-boundary protocol is explicitly defined
- [ ] Agent roles match your actual workflow (not theoretical)

---

## 5. rules.md — Global Coding Rules

### Purpose

Define **how** code should be written in this project. Rules are **conventions that apply to every line of code**, regardless of which agent or developer writes it. Think of it as the **style guide + architectural guard rails**.

### When You Need It

- Always. This is the single most impactful agent config file.
- Even a 20-line rules.md dramatically improves AI output quality.

### Anatomy of a Good rules.md

A rules.md has **7 sections**, each answering a specific question:

```
┌─────────────────────────────────────────────────────┐
│                    rules.md                          │
│                                                      │
│  §1  IDENTITY         What is this project?          │
│  §2  UNIVERSAL RULES  Rules for ALL code             │
│  §3  BACKEND RULES    Server-specific patterns       │
│  §4  FRONTEND RULES   Client-specific patterns       │
│  §5  STYLING RULES    CSS/design conventions         │
│  §6  TESTING RULES    Test conventions               │
│  §7  FORBIDDEN        Things AI must NEVER do        │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Complete Template

```markdown
# Project Rules for AI Coding Assistants

## §1 — Project Identity

- **Name:** [Project Name]
- **Description:** [What it does, in one sentence]
- **Stack:** [TypeScript, Express 5, React 19, Prisma, PostgreSQL, Vanilla CSS]
- **Architecture:** [Monorepo: `server/` + `client/`]
- **SDD Specs:** [`.sdd/` directory — consult before any structural change]

## §2 — Universal Rules

### Language & Types
- TypeScript strict mode everywhere. No `any` without `// @justified: reason`.
- Use `const` by default. `let` only for reassignment. Never `var`.
- Use `interface` for object shapes. Use `type` for unions and intersections.
- Named exports only. No `export default`.

### Functions
- Async/await over `.then()` chains.
- Destructure parameters when ≥3 properties.
- Arrow functions for callbacks. Named `function` for top-level declarations.
- Error-first pattern: validate input → check preconditions → execute → return.

### Naming
- Files: `kebab-case.ts` (server), `PascalCase.tsx` (React components)
- Variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Types/Interfaces: `PascalCase`
- Database columns: `snake_case` (via Prisma @@map)
- API paths: `kebab-case` (`/api/bills/bulk/action`)
- CSS classes: `kebab-case` (`.metric-card`, `.btn-primary`)

### Comments
- Only comment WHY, never WHAT.
- No AI boilerplate ("This function does X", "This is the main component").
- Preserve all existing comments when modifying files.
- TODOs must include ticket reference: `// TODO(BP-42): implement pagination`

### Error Handling
- Never swallow errors silently. At minimum: `console.error(err)`.
- API errors: `res.status(XXX).json({ error: "human-readable message" })`.
- Frontend: try/catch in async handlers, display errors to user.

### Git
- Conventional Commits: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore, perf
- One logical change per commit. Keep diffs reviewable.

## §3 — Backend Rules (server/)

### Express
- Use `Router()` per entity. Mount on `app.use("/api/{entity}", router)`.
- Route handler pattern: `validate → precondition check → execute → respond`.
- Always include `{ vendor: true, payment: true }` in bill queries.
- Never send a response after another response (no double `res.json()`).

### Prisma
- Use `Prisma.Decimal` for monetary values. Never `parseFloat` for amounts.
- Always use `include` for related entities in API responses.
- Seed data: `deleteMany` before `create` (idempotent seeds).
- Use `@@map("snake_case")` for table and column names.

### API Conventions
- Base path: `/api`
- List endpoints: return `{ data: T[], pagination: { page, limit, total, totalPages } }`
- Error responses: return `{ error: string }` with appropriate HTTP status.
- Actions (state transitions): `POST /api/{entity}/:id/{action}`
- Use PATCH for partial updates. Not PUT.
- Validate request body before database operations.

## §4 — Frontend Rules (client/)

### React
- Functional components only. No class components.
- No `useEffect` for derived state — compute inline.
- URL-driven state for table views (useSearchParams, not useState).
- Fetch data in page components, pass down to display components.
- No global state manager. useState + prop drilling for MVP scope.
- Use `useCallback` for functions passed to children or used in useEffect deps.

### Routing
- All routes defined in `App.tsx`.
- Use `NavLink` (not `Link`) for navigation with active state.
- Catch-all route redirects to `/`.

### Data Fetching Pattern
```typescript
const [data, setData] = useState<T | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");

useEffect(() => {
  api.get<T>("/endpoint")
    .then(setData)
    .catch(err => setError(err.message))
    .finally(() => setLoading(false));
}, []);

if (loading) return <div className="loading">Loading…</div>;
if (error) return <div className="error-message">{error}</div>;
```

## §5 — Styling Rules

- All styles in `client/src/index.css`. One file, no CSS modules.
- Use CSS custom properties from `:root`. Never hardcode colors.
- Design tokens: `--color-*`, `--space-*`, `--font-*`, `--radius-*`, `--shadow-*`.
- Every interactive element: hover, focus, disabled, active states.
- Mobile tables: use `data-label` attribute + `::before` pseudo-element.
- No inline styles except one-off layout (grid templates, flex alignment).

## §6 — Testing Rules

- Test files: `*.test.ts` / `*.spec.ts` colocated with source.
- Test names: `"should [expected behavior] when [condition]"`.
- API tests: verify status code, response shape, and error cases.
- UI tests: verify rendering, user interactions, and state changes.
- Every test must be independent — no shared mutable state between tests.

## §7 — Forbidden Patterns

These will be rejected in code review. Do NOT generate code that does any of these:

- ❌ `export default` (use named exports)
- ❌ `any` type without justification comment
- ❌ `var` keyword
- ❌ `console.log` in production code (use proper error handling)
- ❌ Inline styles for colors or spacing (use CSS custom properties)
- ❌ AI-generated boilerplate comments
- ❌ Raw SQL queries (use Prisma)
- ❌ `eval()` or `Function()` constructor
- ❌ Disabled TypeScript checks (`// @ts-ignore`, `// @ts-nocheck`)
- ❌ Hardcoded secrets or API keys
- ❌ `!important` in CSS
- ❌ Direct DOM manipulation in React (`document.getElementById`)
```

### Prompt to Generate rules.md

```markdown
Generate a rules.md for my project's AI coding assistants.

**Project Context:**
[paste your constitution or project summary]

**Tech Stack:**
[exact versions of every technology]

**Existing Patterns:**
Here are examples of existing code that shows our conventions:
- Backend route example: [paste a representative route handler]
- Frontend component example: [paste a representative component]
- CSS example: [paste representative CSS]

**Pain Points I've Had With AI:**
- [e.g., "AI keeps using default exports"]
- [e.g., "AI adds unnecessary comments"]
- [e.g., "AI uses Tailwind when I want vanilla CSS"]

Generate rules organized into 7 sections:
§1 Identity, §2 Universal, §3 Backend, §4 Frontend,
§5 Styling, §6 Testing, §7 Forbidden

Each rule must be:
- Specific enough to be mechanically followed
- Derived from my actual patterns (not generic best practices)
- Written as an imperative ("Use X", "Do not Y")
```

### Review Checklist
- [ ] §1 Identity is factually correct (stack, architecture)
- [ ] §2 Universal rules don't contradict each other
- [ ] §3-§5 rules match patterns actually used in the codebase
- [ ] §7 Forbidden list includes every pattern that's caused problems
- [ ] Rules are imperative ("Use X") not advisory ("Consider using X")
- [ ] No rules are so vague they can't be verified
- [ ] Total length is <500 lines (agents lose focus on very long rule files)

---

## 6. skills.md — Reusable Task Templates

### Purpose

Define **what** common tasks look like in this project. Skills are **parameterized recipe templates** that an agent follows step-by-step when performing a recurring task. Think of them as the **playbook**.

### When You Need It

- When you find yourself giving the same instructions repeatedly
- When multiple developers need AI to produce identical results for the same task type
- When onboarding new team members who'll use AI

### The Difference: Rules vs Skills

| Aspect | Rules | Skills |
|--------|-------|--------|
| **Apply** | Always, to all code | When explicitly invoked |
| **Scope** | Conventions and constraints | Step-by-step task recipes |
| **Granularity** | One line per rule | 10-30 lines per skill |
| **Example** | "Use named exports" | "How to add a new CRUD entity end-to-end" |
| **Analogy** | Grammar | Recipe |

### Anatomy of a Skill

Every skill has 5 parts:

```markdown
## Skill: [Verb + Object]

### Description
[One sentence: when to use this skill]

### Parameters
- `{param1}`: [Description — what the user provides]
- `{param2}`: [Description]

### Prerequisites
- [What must exist before running this skill]
- [Files that must be in place]

### Steps
1. [Specific action with file path]
2. [Another specific action]
3. [Validation/verification step]

### Result
[What the codebase looks like after this skill runs]
```

### Complete Template

```markdown
# Skills — Reusable AI Task Templates

> When performing a common task, invoke the matching skill below.
> Follow every step in order. Do not skip steps.
> Replace `{parameters}` with actual values.

---

## Skill: Add New Entity (Full Stack)

### Description
Creates a complete new entity from data model through UI, following
all project conventions.

### Parameters
- `{Entity}`: PascalCase entity name (e.g., `Invoice`)
- `{entity}`: camelCase (e.g., `invoice`)
- `{entities}`: plural (e.g., `invoices`)
- `{fields}`: Field definitions from data model spec

### Prerequisites
- `.sdd/02-data-model-spec.md` has the entity defined
- `.sdd/03-api-contract.md` has all endpoints documented
- Database is running (`docker compose up -d`)

### Steps

**Phase 1 — Database**
1. Add model to `server/prisma/schema.prisma` per data model spec
2. Run `npx prisma migrate dev --name add-{entity}`
3. Add seed data to `server/prisma/seed.ts`

**Phase 2 — Backend**
4. Create `server/src/routes/{entities}.ts` with Router()
5. Implement all endpoints per API contract:
   - GET / (list with pagination)
   - GET /:id (detail with includes)
   - POST / (create with validation)
   - PATCH /:id (update with guards)
   - DELETE /:id (with guards)
6. Mount router in `server/src/index.ts`:
   `app.use("/api/{entities}", {entities}Router)`

**Phase 3 — Frontend Types**
7. Add TypeScript interface to `client/src/types/index.ts`
8. Add label maps if entity has enum fields

**Phase 4 — Frontend Page**
9. Create `client/src/pages/{Entity}sPage.tsx`
10. Implement: data fetching, table, create form, edit form, delete
11. Add route to `client/src/App.tsx`
12. Add NavLink to `client/src/components/Layout.tsx`

**Phase 5 — Verification**
13. Test API: `curl http://localhost:3001/api/{entities}`
14. Test UI: Navigate in browser, create/edit/delete
15. Update `.sdd/08-verification-spec.md` with new test cases

### Result
- New database table with migration
- Full CRUD API at `/api/{entities}`
- UI page with table, forms, and navigation link
- All tests passing

---

## Skill: Add State Transition

### Description
Adds a new lifecycle action to an entity (e.g., approve, reject, archive).

### Parameters
- `{action}`: lowercase action name (e.g., `approve`)
- `{entity}`: entity name (e.g., `bill`)
- `{sourceStatus}`: valid starting status (e.g., `PENDING_APPROVAL`)
- `{targetStatus}`: resulting status (e.g., `APPROVED`)
- `{timestampField}`: field to set (e.g., `approvedAt`)
- `{confirmMessage}`: optional confirmation dialog text

### Steps
1. **Backend:** Add handler in `server/src/routes/{entity}s.ts`:
   ```
   POST /api/{entity}s/:id/{action}
   - Validate status is {sourceStatus}
   - Update to {targetStatus}, set {timestampField} = new Date()
   - Return updated entity with includes
   ```
2. **Frontend Detail Page:** In `{Entity}DetailPage.tsx`:
   - Add `"{action}"` to `getAvailableActions()`
     for status `{sourceStatus}`
   - Add entry to `ACTION_CONFIG`:
     ```
     {action}: {
       label: "{Action Label}",
       cls: "btn-{variant}",
       confirm: "{confirmMessage}" // if needed
     }
     ```
3. **Bulk Actions:** If applicable, add to bulk handler in
   `server/src/routes/{entity}s.ts` bulk/action endpoint
4. **Verify:** Test on detail page, observe status badge change

---

## Skill: Add Table Filter

### Description
Adds a new filter option to a table page.

### Parameters
- `{page}`: page component name (e.g., `BillsPage`)
- `{filterField}`: field to filter on (e.g., `vendorId`)
- `{filterType}`: UI element (`select`, `input`, `daterange`)
- `{options}`: where options come from (e.g., "fetch from /api/vendors")

### Steps
1. Add URL param reading: `const current{Filter} = searchParams.get("{filterField}") || ""`
2. Pass to API: `if (current{Filter}) params.set("{filterField}", current{Filter})`
3. Add UI element to `.table-toolbar`:
   - If `select`: fetch options on mount, render `<select>`
   - If `input`: render `<input>` with debounce
4. Wire to `setParam("{filterField}", value)` onChange
5. Backend: ensure `GET /api/{entities}` handles the query param

---

## Skill: Add Responsive Breakpoint

### Description
Adds mobile responsiveness for a specific width.

### Parameters
- `{width}`: breakpoint (e.g., `768px`)
- `{transformations}`: list of CSS changes

### Steps
1. Add `@media (max-width: {width})` section to
   `client/src/index.css` (insert before next smaller breakpoint)
2. Implement each transformation from {transformations}
3. Test at exactly {width} and {width - 1}px
4. Verify no horizontal overflow (`document.body.scrollWidth === window.innerWidth`)
5. Update `.sdd/04-ui-ux-spec.md` responsive table

---

## Skill: Add Environment Variable

### Description
Adds a new configuration value across all environments.

### Parameters
- `{varName}`: environment variable name (SCREAMING_SNAKE)
- `{defaultValue}`: development default
- `{usage}`: what it controls

### Steps
1. Add to `server/.env`: `{varName}={defaultValue}`
2. Read in code: `const val = process.env.{varName} || "{defaultValue}"`
3. Add to `docker-compose.yml` → app service → environment
4. Add to `docker-compose.prod.yml` → app service → environment
5. Add to `.sdd/11-environment-strategy.md` variable table
6. Add to `Dockerfile` if needed (ARG/ENV)
7. Document in `README.md` setup instructions

---

## Skill: Fix a Bug

### Description
Standard workflow for diagnosing and fixing a reported bug.

### Parameters
- `{symptom}`: what the user observes
- `{expectedBehavior}`: what should happen instead

### Steps
1. **Reproduce:** Find the exact steps that trigger `{symptom}`
2. **Locate:** Trace from UI → API call → route handler → DB query
3. **Root cause:** Identify the specific line(s) causing the issue
4. **Check spec:** Verify what `.sdd/` specs say the behavior should be
5. **Fix:** Make the minimal change that resolves the root cause
6. **Verify:** Confirm `{expectedBehavior}` now occurs
7. **Regression check:** Ensure no other functionality broke
8. **Commit:** `fix({scope}): {description of what was wrong}`
```

### Prompt to Generate skills.md

```markdown
Generate a skills.md for my project's AI coding assistants.

**Project Context:**
[paste constitution or architecture summary]

**Recurring Tasks I Do:**
1. [e.g., "Add a new database entity with full CRUD"]
2. [e.g., "Add a new page with a data table"]
3. [e.g., "Add a new status transition to the bill lifecycle"]
4. [e.g., "Fix a reported bug"]
5. [e.g., "Add a new filter to a table page"]

**For each task, I want a skill that includes:**
- Parameters (what I need to provide)
- Step-by-step instructions (referencing actual file paths)
- Verification step (how to confirm it worked)

The skills should reference my actual project structure:
- server/src/routes/ for backend routes
- client/src/pages/ for frontend pages
- client/src/index.css for styling
- .sdd/ for specifications

Make each skill follow the exact patterns already in my codebase.
```

### Review Checklist
- [ ] Every recurring task you've done >3 times has a skill
- [ ] Each skill has clear parameters (no ambiguity in what to provide)
- [ ] File paths reference your actual project structure
- [ ] Steps reference actual patterns from your codebase
- [ ] Every skill has a verification/testing step at the end
- [ ] Skills don't duplicate what's already in rules.md

---

## 7. Tool-Specific Configurations

Each AI tool reads from its own config file. Here's how to create each one:

### Gemini (.gemini/rules.md)

```markdown
# .gemini/rules.md

# This is the primary config for Google Gemini Code Assist.
# It is automatically loaded at the start of every session.

[Paste your full rules.md content here]

# Additionally, consult these files for context:
# - AGENTS.md for scope boundaries
# - .sdd/*.md for specifications
# - .gemini/skills.md for task templates
```

**Settings file (.gemini/settings.json):**
```json
{
  "codeAssist": {
    "contextFiles": [
      "AGENTS.md",
      ".sdd/00-constitution.md",
      ".sdd/03-api-contract.md"
    ]
  }
}
```

### GitHub Copilot (.github/copilot-instructions.md)

Copilot has a **2000-token limit** for instructions, so be concise:

```markdown
# Copilot Instructions

TypeScript monorepo: `server/` (Express 5 + Prisma) + `client/` (React 19 + Vite).

## Must follow:
- Named exports only (no `export default`)
- `const` by default, `let` for reassignment, never `var`
- Async/await, not `.then()` chains
- TypeScript strict: no `any` without `// @justified:` comment
- API errors: `{ error: string }` with HTTP status code
- Lists: `{ data: T[], pagination: {...} }` envelope
- Status transitions: `POST /api/{entity}/:id/{action}`
- CSS: use `--color-*`, `--space-*` custom properties, never hardcode
- Comments: only WHY, never WHAT. No AI boilerplate.
- Commits: Conventional Commits (`type(scope): description`)

## Key files:
- Schema: `server/prisma/schema.prisma`
- Route pattern: `server/src/routes/bills.ts`
- Component pattern: `client/src/components/StatusBadge.tsx`
- Design tokens: `client/src/index.css` (`:root` block)
- Types: `client/src/types/index.ts`
```

### Cursor (.cursor/rules/)

Cursor supports **glob-scoped rules**. Create separate files per domain:

**`.cursor/rules/global.mdc`**
```markdown
---
description: Global project rules
globs: ["**/*.ts", "**/*.tsx", "**/*.css"]
---
[Paste §1 Identity and §2 Universal from rules.md]
```

**`.cursor/rules/backend.mdc`**
```markdown
---
description: Backend rules for Express + Prisma
globs: ["server/**/*.ts"]
---
[Paste §3 Backend from rules.md]
```

**`.cursor/rules/frontend.mdc`**
```markdown
---
description: Frontend rules for React + CSS
globs: ["client/**/*.tsx", "client/**/*.css"]
---
[Paste §4 Frontend and §5 Styling from rules.md]
```

### Claude Code (.claude/project-instructions.md)

```markdown
# Project Instructions for Claude

[Paste your full rules.md and relevant AGENTS.md sections here.
Claude supports long context, so no need to abbreviate.]

## When asked to implement a feature:
1. First check `.sdd/` for an existing spec
2. Follow the spec exactly — do not add undocumented features
3. Reference the relevant spec section in your response

## When asked to fix a bug:
1. Follow the "Fix a Bug" skill in `.gemini/skills.md`
```

### Windsurf (.windsurfrules)

```markdown
[Paste your rules.md content here — Windsurf reads a single flat file]
```

---

## 8. Writing Effective Rules

### The Rule Quality Spectrum

```
❌ Vague                                              ✅ Precise
──────────────────────────────────────────────────────────────
"Write clean code"          →  "Use const by default, let only
                                for reassignment, never var"

"Handle errors properly"    →  "API routes: catch all errors,
                                return { error: message } with
                                appropriate HTTP status code"

"Follow best practices"     →  "Named exports only. No export
                                default in any file."

"Use good naming"           →  "Files: kebab-case.ts (server),
                                PascalCase.tsx (components).
                                Variables: camelCase."
```

### Rule Writing Formula

Every rule should follow this pattern:

```
[ACTION] + [SPECIFIC TARGET] + [OPTIONAL: WHY or INSTEAD OF]
```

Examples:
```
Use Prisma.Decimal for monetary values. Never parseFloat for amounts.
     ↑                    ↑                        ↑
   ACTION           SPECIFIC TARGET          INSTEAD OF

Return { error: string } for all API errors. Include HTTP status code.
  ↑              ↑                                    ↑
ACTION     SPECIFIC TARGET                       ADDITIONAL DETAIL

Destructure function parameters when 3 or more properties.
      ↑                                 ↑
    ACTION                         CONDITION
```

### Rules to Write First (Highest Impact)

| Priority | Rule Category | Example |
|----------|--------------|---------|
| 1️⃣ | **Export style** | Named exports only |
| 2️⃣ | **Type strictness** | No `any`, use proper interfaces |
| 3️⃣ | **Error handling pattern** | Return `{ error }` with status code |
| 4️⃣ | **Styling approach** | CSS custom properties, no Tailwind |
| 5️⃣ | **File naming** | kebab-case for server, PascalCase for components |
| 6️⃣ | **State management** | URL params for tables, no global store |
| 7️⃣ | **Comment policy** | Only WHY, never WHAT |
| 8️⃣ | **Import style** | Explicit `.tsx` extensions, no barrel files |

### How Many Rules?

| Count | Quality | Effect |
|-------|---------|--------|
| < 10 | Too few | AI still guesses most conventions |
| 20-50 | Sweet spot | Covers 90% of decisions |
| 50-100 | Thorough | Good for large/complex projects |
| > 100 | Diminishing returns | AI may lose focus on important rules |

---

## 9. Writing Effective Skills

### Skill Sizing Guide

| Size | Steps | When to Use |
|------|-------|-------------|
| **Micro** (3-5 steps) | Single file change | "Add env variable", "Add CSS class" |
| **Small** (5-10 steps) | Single-concern task | "Add API endpoint", "Add table filter" |
| **Medium** (10-20 steps) | Cross-file task | "Add state transition", "Add new page" |
| **Large** (20+ steps) | Full-stack feature | "Add new entity", "Implement new workflow" |

### Skill Parameterization

Good parameters make skills reusable:

```markdown
# ❌ Bad: Hardcoded values
## Skill: Add Vendor Endpoint
1. Create server/src/routes/vendors.ts

# ✅ Good: Parameterized
## Skill: Add CRUD Endpoint
### Parameters
- `{Entity}`: PascalCase name (e.g., Vendor)
- `{entities}`: plural lowercase (e.g., vendors)
1. Create server/src/routes/{entities}.ts
```

### When to Create a New Skill

Use the **Rule of Three**: If you've given the same instructions to AI three times, extract it into a skill.

```
First time:    Just do it inline
Second time:   Notice the pattern
Third time:    Create the skill ← HERE
```

---

## 10. The Configuration Workflow

### Initial Setup (New Project)

```
Step 1: Create rules.md                              [30-45 min]
        Start with §1 Identity and §7 Forbidden.
        Add §2-§6 as you encounter decisions.
        ↓
Step 2: Create AGENTS.md                              [15-20 min]
        Define 2-3 agents matching your architecture.
        ↓
Step 3: Create tool-specific configs                  [15-20 min]
        Excerpt from rules.md into each tool's format.
        ↓
Step 4: Start coding with AI                          [ongoing]
        Every time AI gets something wrong → add a rule.
        ↓
Step 5: After 1-2 weeks, create skills.md             [30-45 min]
        Identify recurring tasks → write skill templates.
```

### Existing Project (Retroactive Setup)

```
Step 1: Review existing code for patterns             [30 min]
        Look at 3-5 representative files per layer.
        ↓
Step 2: Generate rules.md from patterns               [20 min]
        Prompt: "Given these code examples, extract
        the coding conventions into a rules.md"
        ↓
Step 3: Test with a real task                          [15 min]
        Ask AI to implement something. Check if it
        follows the rules. If not → add missing rules.
        ↓
Step 4: Iterate for 1 week                            [ongoing]
        Every correction you make → becomes a rule.
        ↓
Step 5: Extract skills from repeated prompts          [30 min]
```

### The Feedback Loop

```
┌────────────────────────────────────────┐
│                                        │
│   AI writes code                       │
│        ↓                               │
│   You review code                      │
│        ↓                               │
│   ┌─ Follows rules → ✅ Accept        │
│   │                                    │
│   └─ Breaks a convention → ❌ Reject   │
│        ↓                               │
│   Ask: "Is this rule in my rules.md?"  │
│        ↓                               │
│   ┌─ Yes → AI bug, rephrase the rule   │
│   │                                    │
│   └─ No → Add the missing rule         │
│        ↓                               │
│   rules.md gets better over time       │
│        ↓                               │
│   AI makes fewer mistakes              │
│        ↓                               │
│   (back to top)                        │
│                                        │
└────────────────────────────────────────┘
```

---

## 11. Prompt Templates for Generating Configs

### Generate rules.md from Existing Code

```markdown
I have an existing project and need to create a rules.md
for AI coding assistants.

Here are representative files from my codebase:

**Backend route example:**
```
[paste 50-100 lines of a typical route file]
```

**Frontend component example:**
```
[paste 50-100 lines of a typical component]
```

**CSS example:**
```
[paste 30-50 lines showing your design token usage]
```

**package.json:**
```
[paste to show dependencies]
```

Analyze these files and extract:
1. All coding conventions (exports, naming, error handling, types)
2. All architectural patterns (route structure, component patterns)
3. All styling conventions (CSS approach, class naming, tokens)
4. Any "forbidden" patterns I'm clearly avoiding

Generate a rules.md with 7 sections: Identity, Universal,
Backend, Frontend, Styling, Testing, Forbidden.

Every rule must be derived from the actual code — not generic
best practices. If you can't find evidence for a rule, don't include it.
```

### Generate AGENTS.md from Architecture

```markdown
Generate an AGENTS.md based on my project structure:

```
[paste your file tree]
```

**Team roles:**
- [e.g., "1 fullstack developer" or "2 backend + 1 frontend"]

**AI tools used:**
- [e.g., "Gemini for architecture, Copilot for inline completion"]

Define agents that map to the natural boundaries of the codebase.
Each agent should own specific directories and file types.
Include interaction protocols for cross-boundary changes.
```

### Generate skills.md from Task History

```markdown
Here are the last 10 tasks I asked AI to help with:

1. "Add a dueDate filter to the bills table"
2. "Create the vendors CRUD endpoint"
3. "Add an 'archive' action to bills"
4. "Fix the overdue calculation to exclude paid bills"
5. "Add a mobile breakpoint at 768px"
6. "Create the dashboard aggregation endpoint"
7. "Add a confirmation dialog for delete"
8. "Add a new vendor with seed data"
9. "Create a form component for bill creation"
10. "Fix pagination not resetting on filter change"

Identify the common patterns and create parameterized skills for
the 5-6 most repeatable task types. Each skill should:
- Name the task (verb + noun)
- Define parameters
- List step-by-step instructions using my file paths
- Include a verification step
```

### Adapt rules.md to a New Tool

```markdown
I have a universal rules.md for my project:

```
[paste rules.md]
```

Create a {tool-name} config file that:
1. Follows the {tool's config format and path}
2. Respects the {tool's token/size limits}
3. Preserves the most important rules if truncation is needed
4. Prioritizes: §7 Forbidden > §2 Universal > §3-§5 Domain-specific
```

---

## 12. Anti-Patterns to Avoid

### ❌ Don't: Copy generic rules from the internet

**Why it fails:** Generic rules like "write clean code" or "follow SOLID principles" are too vague for AI. They don't change behavior.

**Do instead:** Extract rules from YOUR actual codebase. If you can't point to a file that demonstrates the rule, it's not a real rule.

---

### ❌ Don't: Write rules as suggestions

**Why it fails:** "Consider using TypeScript interfaces" → AI treats this as optional.

**Do instead:** Write rules as imperatives: "Use TypeScript interfaces for all object shapes. Use type for unions and intersections."

---

### ❌ Don't: Duplicate rules across tool configs

**Why it fails:** When you update a rule, you forget to update it in 4 other tool config files. Rules drift and contradict.

**Do instead:** Maintain ONE canonical rules.md. Create tool-specific configs that reference or excerpt from it.

---

### ❌ Don't: Write all rules on day one

**Why it fails:** You'll write rules for problems you don't have yet, and miss rules for problems you encounter daily.

**Do instead:** Start with 10-15 rules. Add one rule every time AI gets something wrong. After 2 weeks, you'll have a comprehensive set derived from real problems.

---

### ❌ Don't: Make rules.md a novel

**Why it fails:** AI tools have context limits. A 2000-line rules file means the AI might skip or deprioritize important rules.

**Do instead:** Keep under 500 lines. Use the §7 Forbidden section for the most critical rules — AI tends to weight negative rules more heavily.

---

### ❌ Don't: Include implementation code in rules

**Why it fails:** Rules should define patterns, not specific implementations. Code examples belong in skills.md.

**Do instead:** Rules = "what to do". Skills = "how to do it step by step".

```markdown
# ❌ In rules.md (too specific)
"When creating a bill, use this exact code:
const bill = await prisma.bill.create({ data: { ... } })"

# ✅ In rules.md (convention)
"Use Prisma client for all database operations. Never raw SQL."

# ✅ In skills.md (recipe)
"## Skill: Add CRUD Endpoint
Step 3: Create handler using prisma.{entity}.create({ data: { ... } })"
```

---

## 13. Maintaining Configs Over Time

### When to Update

| Trigger | Action |
|---------|--------|
| AI produces code that breaks a convention | Add the missing rule to rules.md |
| You refactor and patterns change | Update rules.md to match new patterns |
| New dependency added | Update §1 Identity and relevant rules |
| New team member joins | Verify onboarding covers agent configs |
| New AI tool adopted | Create tool-specific config from rules.md |
| Major version upgrade (React 19→20) | Update stack versions and any API changes |
| You do a task for the 3rd time | Create a new skill in skills.md |

### Version Control

Agent configs should be **committed to the repository** alongside code:

```bash
git add .gemini/rules.md AGENTS.md
git commit -m "chore(agents): add rule for named exports over default"
```

This means:
- Rules are reviewed in PRs like any other code change
- Rules are versioned and have history
- Every developer gets the same AI behavior
- Rules can be reverted if problematic

### Review Cadence

| Frequency | What |
|-----------|------|
| **Weekly** | Scan for new rules needed (from code review feedback) |
| **Monthly** | Audit skills.md — are all skills still accurate? |
| **Quarterly** | Full review: remove obsolete rules, consolidate duplicates |
| **Per release** | Update §1 Identity with new versions |

---

## 14. Cross-Tool Compatibility Matrix

| Feature | Gemini | Copilot | Cursor | Claude | Windsurf | Aider |
|---------|:------:|:-------:|:------:|:------:|:--------:|:-----:|
| **Auto-loaded config** | ✅ `.gemini/rules.md` | ✅ `.github/copilot-instructions.md` | ✅ `.cursor/rules/*.mdc` | ✅ `.claude/project-instructions.md` | ✅ `.windsurfrules` | ✅ `.aider.conf.yml` |
| **Max config size** | Large | ~2000 tokens | Medium per file | Large | Medium | Medium |
| **Glob-scoped rules** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Multi-file rules** | ✅ (rules + skills) | ❌ (single file) | ✅ (multiple .mdc) | ❌ (single file) | ❌ (single file) | ❌ |
| **Reads AGENTS.md** | ✅ (if referenced) | ❌ | ✅ (if in rules) | ✅ (if referenced) | ❌ | ❌ |
| **Skills support** | ✅ native | ❌ | ❌ | ✅ (via instructions) | ❌ | ❌ |
| **Agent personas** | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |

### Strategy: Maximum Compatibility

```
1. Write ONE canonical rules.md (universal format)
2. For each tool:
   a. Copy/excerpt relevant sections into tool's config file
   b. Respect the tool's size limits (truncate for Copilot)
   c. Use the tool's specific syntax (globs for Cursor)
3. Keep tool configs as thin adapters — not independent documents
```

---

## 15. Checklist: Agent Configuration Completeness

### AGENTS.md
- [ ] Project context section with stack and architecture
- [ ] 2+ agent definitions with clear scope boundaries
- [ ] Every agent has "can modify" and "cannot modify" permissions
- [ ] Every agent has "must reference" spec files
- [ ] Cross-boundary interaction protocol defined
- [ ] Conflict resolution protocol defined

### rules.md
- [ ] §1 Identity — project name, stack, architecture
- [ ] §2 Universal — ≥10 rules covering types, naming, errors, comments
- [ ] §3 Backend — ORM patterns, API conventions, route structure
- [ ] §4 Frontend — component patterns, state management, routing
- [ ] §5 Styling — CSS approach, design tokens, responsive strategy
- [ ] §6 Testing — test file naming, assertion patterns
- [ ] §7 Forbidden — ≥8 explicitly banned patterns
- [ ] Total length < 500 lines
- [ ] Every rule is imperative (not advisory)
- [ ] Every rule is verifiable (not vague)

### skills.md
- [ ] ≥3 skills covering the most common recurring tasks
- [ ] Each skill has parameters, prerequisites, and steps
- [ ] Steps reference actual file paths in the project
- [ ] Each skill has a verification/testing step
- [ ] Skills don't duplicate rules.md content

### Tool-Specific Configs
- [ ] Config exists for every AI tool used by the team
- [ ] Each config references or excerpts the canonical rules.md
- [ ] Each config respects the tool's size and format limits
- [ ] Configs are committed to version control
- [ ] Configs have been tested (AI produces correct output)

---

## 16. Real-World Examples

### Minimal Setup (Solo Developer, 1 AI Tool)

```
project/
├── .gemini/
│   └── rules.md          # 50-80 lines, §1 + §2 + §7 only
└── ...
```

**Time to create:** 20 minutes

### Standard Setup (Small Team, 2-3 AI Tools)

```
project/
├── AGENTS.md              # 2-3 agent definitions
├── .gemini/
│   ├── rules.md           # Full 7-section rules
│   └── skills.md          # 4-6 common skills
├── .github/
│   └── copilot-instructions.md  # Condensed rules (2000 tokens)
├── .cursor/rules/
│   ├── global.mdc          # Universal rules
│   └── backend.mdc         # Backend-specific rules
└── ...
```

**Time to create:** 2 hours

### Enterprise Setup (Large Team, Full AI Stack)

```
project/
├── AGENTS.md              # 5-6 agents with detailed protocols
├── .gemini/
│   ├── rules.md           # Full rules + team workflow rules
│   ├── skills.md          # 10+ skills covering all common tasks
│   └── settings.json      # Tool settings
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
│       └── lint-agent-configs.yml  # CI check that configs are valid
├── .cursor/rules/
│   ├── global.mdc
│   ├── backend.mdc
│   ├── frontend.mdc
│   └── testing.mdc
├── .claude/
│   └── project-instructions.md
├── .windsurfrules
├── .sdd/                  # Full SDD spec suite
│   └── ...
└── ...
```

**Time to create:** 4-5 hours (then ongoing maintenance)

---

## Appendix A: Quick-Start — Create Your Config in 15 Minutes

If you want to start immediately with the minimum viable agent config:

```markdown
# Paste this into .gemini/rules.md (or your tool's config file)
# Then customize the [BRACKETS] for your project

# Project Rules

## Identity
- Project: [Project Name]
- Stack: [e.g., TypeScript, React, Node.js, PostgreSQL]
- Structure: [e.g., Monorepo with client/ and server/]

## Rules
- TypeScript strict. No `any`.
- Named exports only. No `export default`.
- Async/await over .then() chains.
- [Your most important convention #1]
- [Your most important convention #2]
- [Your most important convention #3]

## Forbidden
- ❌ `var` keyword
- ❌ `any` type without justification
- ❌ Inline styles for colors (use CSS variables)
- ❌ AI boilerplate comments
- ❌ console.log in production code
```

**That's it.** 15 lines. Start here, add rules as you encounter AI mistakes, and grow it organically over the next 2 weeks.

---

## Appendix B: Config File Cheat Sheet

| Tool | Config Path | Format | Auto-loaded? | Max Size |
|------|-------------|--------|:------------:|----------|
| **Gemini** | `.gemini/rules.md` | Markdown | ✅ | Large |
| **Gemini Skills** | `.gemini/skills.md` | Markdown | On reference | Large |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Markdown | ✅ | ~2000 tokens |
| **Cursor** | `.cursor/rules/*.mdc` | MDC (frontmatter + MD) | ✅ | Medium per file |
| **Claude Code** | `.claude/project-instructions.md` | Markdown | ✅ | Large |
| **Windsurf** | `.windsurfrules` | Markdown | ✅ | Medium |
| **Aider** | `.aider.conf.yml` | YAML | ✅ | Small |
| **Cline** | `cline_docs/*.md` | Markdown | ✅ | Multiple files |

---

*Agent configs are the highest-leverage investment in AI-assisted development. 2 hours of setup → thousands of hours of consistent output.* ⚡
