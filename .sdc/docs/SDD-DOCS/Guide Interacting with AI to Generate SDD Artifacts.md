# 🤖 Guide: Interacting with AI to Generate SDD Artifacts

> **Version:** 1.0  
> **Last Updated:** 2026-04-23  
> **Status:** Active

> **Objective:** Define how a user should interact with an AI coding assistant to generate complete documentation based on Spec-Driven Development (SDD) in a structured, consistent, and traceable way.
>
> **Audience:** Developers, tech leads, and product managers who want to use AI as a co-author for SDD specifications before writing any code.

---

## Table of Contents

1. [Why Use AI for SDD?](#1-why-use-ai-for-sdd)
2. [The SDD-AI Workflow Overview](#2-the-sdd-ai-workflow-overview)
3. [Phase 0 — Context Loading](#3-phase-0--context-loading)
4. [Phase 1 — Constitution](#4-phase-1--constitution)
5. [Phase 2 — Product Requirements](#5-phase-2--product-requirements)
6. [Phase 3 — Data Model](#6-phase-3--data-model)
7. [Phase 4 — API Contract](#7-phase-4--api-contract)
8. [Phase 5 — UI/UX Specification](#8-phase-5--uiux-specification)
9. [Phase 6 — Architecture](#9-phase-6--architecture)
10. [Phase 7 — Implementation Plan & Tasks](#10-phase-7--implementation-plan--tasks)
11. [Phase 8 — Verification Specification](#11-phase-8--verification-specification)
12. [Phase 9 — Implementation with AI](#12-phase-9--implementation-with-ai)
13. [Prompt Templates](#13-prompt-templates)
14. [Anti-Patterns to Avoid](#14-anti-patterns-to-avoid)
15. [Artifact Traceability Matrix](#15-artifact-traceability-matrix)
16. [Checklist: SDD Completeness](#16-checklist-sdd-completeness)

---

## 1. Why Use AI for SDD?

Traditional SDD requires significant upfront writing effort, which discourages adoption. AI changes the equation:

| Without AI | With AI |
|------------|---------|
| Specs take 2-3x longer to write than code | Specs take ~30% of the code-writing time |
| Specs feel like "extra work" | Specs become the fastest path to code |
| Specs go stale because updating is tedious | AI can regenerate/update specs from changes |
| Junior devs struggle with spec writing | AI scaffolds, human refines |
| Specs lack consistency across projects | AI follows templates for uniform output |

### The Core Principle

> **You are the product thinker. The AI is the technical writer.**
>
> You provide the *intent*, *constraints*, and *decisions*.
> The AI produces the *structured, traceable documentation*.

---

## 2. The SDD-AI Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     SDD-AI WORKFLOW                          │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ Phase 0  │──▶│ Phase 1  │──▶│ Phase 2  │──▶│ Phase 3  │   │
│  │ Context  │   │ Constit. │   │   PRD    │   │  Data    │   │
│  │ Loading  │   │          │   │          │   │  Model   │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
│                                                     │        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────▼─────┐   │
│  │ Phase 7  │◀──│ Phase 6  │◀──│ Phase 5  │◀──│ Phase 4  │   │
│  │  Plan +  │   │  Arch.   │   │  UI/UX   │   │   API    │   │
│  │  Tasks   │   │          │   │          │   │ Contract │   │
│  └────┬─────┘   └──────────┘   └──────────┘   └──────────┘   │
│       │                                                      │
│  ┌────▼─────┐   ┌──────────┐                                 │
│  │ Phase 8  │──▶│ Phase 9  │                                 │
│  │  Verify  │   │  Build   │                                 │
│  │  Spec    │   │  (Code)  │                                 │
│  └──────────┘   └──────────┘                                 │
│                                                              │
│  ─── = sequential dependency                                 │
│  Each phase: YOU prompt → AI drafts → YOU review → iterate   │
└──────────────────────────────────────────────────────────────┘
```

### The Interaction Loop (Every Phase)

```
1. YOU provide context + intent via a structured prompt
2. AI generates the artifact draft
3. YOU review: approve, reject, or request changes
4. AI revises based on your feedback
5. YOU approve → artifact is frozen → move to next phase
```

**Critical rule:** Never skip the review step. AI-generated specs that go unreviewed will contain assumptions that don't match your intent.

---

## 3. Phase 0 — Context Loading

### Purpose
Give the AI everything it needs to understand the project before generating any specs.

### What to Provide

| Context Item | Example | Why It Matters |
|-------------|---------|----------------|
| **Challenge/brief** | "Build a payables product inspired by Ramp Bill Pay" | Defines scope boundaries |
| **Reference material** | Links, screenshots, competitor docs | Grounds the AI in the domain |
| **Tech constraints** | "Must use TypeScript, React, Express, PostgreSQL" | Prevents wrong tech recommendations |
| **Time constraints** | "This is a 2-day take-home challenge" | Calibrates scope ambition |
| **Audience** | "Reviewed by senior engineers at a fintech startup" | Sets quality bar |
| **Your preferences** | "I prefer vanilla CSS over Tailwind" | Avoids unwanted suggestions |

### Prompt Template

```markdown
I'm starting a new project and want to use Spec-Driven Development (SDD).
Before we write any code, we'll generate all specs first.

Here's my project context:

**Project:** [one-line description]
**Brief/Challenge:** [paste the requirements or challenge prompt]
**Reference Material:** [links, docs, screenshots]
**Tech Stack:** [languages, frameworks, databases]
**Constraints:** [time, scope, audience, deployment target]
**My Preferences:** [styling approach, state management, etc.]

Please acknowledge that you understand the context.
Do NOT generate any specs yet — just confirm your understanding
and ask me any clarifying questions.
```

### What to Expect
The AI should:
- Summarize its understanding back to you
- Identify ambiguities in the brief
- Ask 2-5 clarifying questions
- **Not** start generating specs yet

### 🔑 Key Principle: Front-load Context

The more context you give in Phase 0, the fewer corrections you'll make in Phases 1-8. Spend 10-15 minutes here to save hours later.

---

## 4. Phase 1 — Constitution

### Purpose
Establish the non-negotiable rules that govern all subsequent specs. This document is the **supreme authority** — every other artifact must comply with it.

### Prompt Template

```markdown
Generate the project Constitution (00-constitution.md).

This document must define:
1. **Mission statement** — what we're building and why
2. **Non-negotiable principles** — rules that can never be violated
3. **Technology constraints** — exact versions and choices with rationale
4. **Architectural rules** — data model patterns, API conventions, frontend patterns
5. **Design system rules** — brand, theme, typography, responsiveness
6. **Quality standards** — what "done" means
7. **Documentation requirements** — what the README must include
8. **Git hygiene** — commit conventions

Base this on the context I provided. Be specific, not generic.
Every rule should be actionable and verifiable.
```

### Review Checklist
- [ ] Every tech choice has a rationale
- [ ] Rules are specific enough to be testable (not "code should be clean")
- [ ] No contradictions between rules
- [ ] Matches your actual preferences (not AI assumptions)

---

## 5. Phase 2 — Product Requirements

### Purpose
Define **what** the product does from the user's perspective, with testable acceptance criteria.

### Prompt Template

```markdown
Generate the Product Requirements Document (01-product-requirements.md).

Based on our constitution and the reference material, define:
1. **Problem statement** — what pain point this solves
2. **Product vision** — one-paragraph north star
3. **Target user** — who uses this, what they need
4. **Core workflows** — ordered by priority (P1, P2, ..., Pn)
   - Each workflow must have:
     - A description of what it does
     - Acceptance criteria as a checkbox list ([ ])
     - Dependencies on other workflows (if any)
5. **Non-functional requirements** — performance, accessibility, error handling
6. **Out of scope** — what we're NOT building, and why
7. **Success metrics** — how we know the product is "done"

For the workflows, study the reference material and prioritize based on:
- What provides the most value for the least complexity
- What demonstrates engineering judgment
- What the evaluator would use first
```

### Review Checklist
- [ ] Workflows are in the right priority order
- [ ] Every acceptance criterion is testable (not vague)
- [ ] Out-of-scope items have justified reasoning
- [ ] No feature is mentioned without a workflow context

### 💡 Pro Tip: Challenge the AI's Priorities

Ask: *"Why did you rank workflow X above Y? What if we swapped them?"*

The AI's initial prioritization is based on patterns from training data. Your product judgment should override it.

---

## 6. Phase 3 — Data Model

### Purpose
Define the domain entities, their relationships, field types, business rules, and constraints.

### Prompt Template

```markdown
Generate the Data Model Specification (02-data-model-spec.md).

Based on the PRD workflows, define:
1. **ERD** (Entity Relationship Diagram) — use Mermaid erDiagram syntax
2. **Enumerations** — all enum types with values, descriptions, and entry conditions
3. **Entity details** — for each entity:
   - Field table (name, type, constraints, notes)
   - Business rules (who can create/edit/delete, state guards)
   - Table mapping (if ORM uses different names)
4. **Design decisions log** — table of "Decision | Rationale" explaining key choices
   - Why this type? Why this relation? Why this constraint?
5. **Indexes & performance notes** — which fields need indexes and why
6. **Seed data strategy** — what demo data looks like, how many records, what story it tells

Important constraints from our constitution:
- [paste relevant data model rules from constitution]
```

### Review Checklist
- [ ] ERD matches all workflows from the PRD
- [ ] Every field needed by the UI/API exists in the model
- [ ] Business rules are explicitly stated (not implied)
- [ ] No circular dependencies
- [ ] Seed data would tell a convincing demo story

### 🔑 Key Principle: The Data Model Drives Everything

If you get the data model wrong, the API and UI will be built on a flawed foundation. Spend extra time here. Ask the AI:

- *"What if a bill could have multiple payments? How would the model change?"*
- *"What happens if I delete a vendor that has bills?"*
- *"How would I query 'all bills approved this week' with this schema?"*

---

## 7. Phase 4 — API Contract

### Purpose
Define every HTTP endpoint, its request/response schema, status codes, and error cases. This is the **contract** between frontend and backend.

### Prompt Template

```markdown
Generate the API Contract Specification (03-api-contract.md).

Based on the data model and PRD workflows, define:
1. **Conventions** — request/response format, pagination envelope,
   error envelope, HTTP status codes used
2. **For each entity, define all endpoints:**
   - Method + path
   - Query parameters (for list endpoints) with types and defaults
   - Request body schema (JSON example)
   - Response body schema (JSON example)
   - Preconditions (state guards)
   - Error cases with specific status codes and messages
3. **Lifecycle/action endpoints** — one table showing all state transitions
   with their valid source states and side effects
4. **Bulk operations** — if any
5. **Aggregation endpoints** — dashboard, reports

For each endpoint, I need to know EXACTLY what the frontend should
send and what it will receive back. Include full JSON examples.
```

### Review Checklist
- [ ] Every PRD workflow maps to at least one API endpoint
- [ ] Every field in the data model appears in at least one response
- [ ] Error cases cover: not found, validation failure, state violation
- [ ] Pagination is standardized across all list endpoints
- [ ] Response shapes are consistent (same envelope everywhere)

### 💡 Pro Tip: Test the Contract Mentally

For each endpoint, mentally walk through: *"If I call this with X, I get Y. If I call it with bad data, I get Z."* If you can't answer that from the spec alone, the spec is incomplete.

---

## 8. Phase 5 — UI/UX Specification

### Purpose
Define the visual design system, component library, page layouts, responsive behavior, and interaction patterns.

### Prompt Template

```markdown
Generate the UI/UX Specification (04-ui-ux-spec.md).

1. **Design philosophy** — 3-5 principles guiding all UI decisions
2. **Design tokens** — CSS custom properties for:
   - Colors (backgrounds, brand, semantic, text)
   - Typography (font family, scale, weights)
   - Spacing (grid system)
   - Border radius scale
   - Shadows & effects
   - Transitions & animations
3. **Component specifications** — for each reusable component:
   - Visual description
   - Variants (e.g., button: primary, secondary, danger...)
   - States (default, hover, active, disabled, focus)
   - Accessibility notes
4. **Page specifications** — for each page:
   - ASCII wireframe showing layout structure
   - Which components are used where
   - Data bindings (what data is shown)
   - User interactions available
5. **Responsive behavior**
   - Breakpoint table
   - What changes at each breakpoint
   - Mobile transformation strategy (e.g., tables → cards)
6. **Interaction specifications**
   - Confirmation dialogs (which actions require confirmation)
   - Loading states
   - Empty states
   - Error states
   - Keyboard shortcuts

Use the brand identity from our constitution for colors and typography.
```

### Review Checklist
- [ ] Every page in the PRD has a wireframe
- [ ] Every interactive element has hover/focus/disabled states defined
- [ ] Loading, empty, and error states are specified for every data view
- [ ] Responsive breakpoints cover phone → desktop
- [ ] Destructive actions have confirmation dialogs

---

## 9. Phase 6 — Architecture

### Purpose
Define how all the pieces fit together: system architecture, file structure, dependencies, data flows, and deployment.

### Prompt Template

```markdown
Generate the Architecture Specification (05-architecture.md).

1. **System architecture diagram** — Mermaid graph showing:
   - Client, Server, Database layers
   - How they communicate
   - Development vs Production topology
2. **File structure** — complete tree with every file and a one-line description
3. **Dependency map** — table of every npm package with its purpose
4. **Data flow diagrams** — Mermaid sequence diagrams for:
   - The most common user action (e.g., creating an entity)
   - The most complex action (e.g., a state transition with side effects)
   - A read-heavy flow (e.g., dashboard aggregation)
5. **State machine diagram** — Mermaid stateDiagram-v2 showing all
   entity states and valid transitions
6. **Deployment architecture** — dev mode, production mode, Docker
   - How the build pipeline works
   - What the entrypoint script does
```

### Review Checklist
- [ ] File structure matches what you'll actually create (no phantom files)
- [ ] Every dependency has a clear purpose (no "it was in the template")
- [ ] Data flows match the API contract exactly
- [ ] State machine matches the lifecycle from the PRD
- [ ] Deployment diagram covers Docker and local dev

---

## 10. Phase 7 — Implementation Plan & Tasks

### Purpose
Break the architecture into **phases** and the phases into **atomic tasks**.

### Prompt Template

```markdown
Generate two documents:

### 06-implementation-plan.md
1. **Phases** — divide work into 4-6 sequential phases
   - Each phase should produce a deployable increment
   - Include a Mermaid Gantt chart with time estimates
2. **Phase details** — for each phase:
   - Goal (one sentence)
   - Step-by-step table (step, what, files created/modified)
   - Deliverable (what "done" looks like)
   - Verification checklist
3. **Risk mitigation** — table of "Risk | Mitigation"
4. **Quality gates** — what must pass before moving to next phase

### 07-task-breakdown.md
1. Break each phase into **atomic tasks** (T-001, T-002, ...)
2. Each task must be:
   - Completable in ≤30 minutes
   - Testable independently
   - Traceable to a spec (PRD acceptance criterion, API endpoint, etc.)
3. Use checkbox format: `- [ ] **T-001** description`
4. Include a **dependency graph** (Mermaid) showing phase-level dependencies
5. Note which phases can be parallelized
```

### Review Checklist
- [ ] Time estimates are realistic (not optimistic)
- [ ] Each phase has a clear deliverable
- [ ] Tasks are small enough to feel achievable (not overwhelming)
- [ ] No task requires reading another task to understand what to do
- [ ] Dependency graph identifies parallelization opportunities

---

## 11. Phase 8 — Verification Specification

### Purpose
Define exactly how to prove the implementation is correct.

### Prompt Template

```markdown
Generate the Verification Specification (08-verification-spec.md).

1. **Testing strategy** — explain the approach (unit, integration, E2E, manual)
2. **API verification matrix** — one table per API group:
   - Test case name
   - HTTP method + endpoint
   - Expected status code + response shape
   - Mark each as ✅ when passing
3. **UI verification matrix** — test cases for:
   - Navigation and layout
   - Each page's core functionality
   - Form submissions
   - Error states
4. **Responsive verification** — test at 4+ widths
5. **Deployment verification** — Docker build and run
6. **Full E2E walkthrough** — a numbered step-by-step scenario
   that exercises EVERY major feature in sequence
   (this is the "demo script" an evaluator would follow)

The E2E walkthrough should read like a script:
"Step 1: Open the app. Step 2: Click X. Step 3: Verify Y."
```

### Review Checklist
- [ ] Every API endpoint has at least one test case
- [ ] Every UI page has test cases for happy path + error path
- [ ] The E2E walkthrough covers all 7 workflows
- [ ] Responsive testing covers the smallest and largest breakpoints
- [ ] Docker verification is a standalone section

---

## 12. Phase 9 — Implementation with AI

### Purpose
Use the completed specs as the **blueprint** for AI-assisted code generation.

### The Implementation Prompt Strategy

Once all specs are approved, you switch from "spec generation" mode to "code generation" mode. The key is to **feed specs as context**:

```markdown
I have a complete SDD specification for my project.

Here are the relevant specs for the task I need to implement:

**Constitution rules that apply:**
[paste relevant sections]

**Data model for this entity:**
[paste from 02-data-model-spec.md]

**API endpoints to implement:**
[paste from 03-api-contract.md]

**Task from the breakdown:**
- [ ] T-016: GET /api/bills — list with filters, sort, pagination

Implement this task. Follow the spec exactly.
Do not add features not in the spec.
Do not skip error handling defined in the spec.
```

### Rules for AI-Assisted Implementation

| Rule | Why |
|------|-----|
| **One task per prompt** | Prevents scope creep and keeps changes reviewable |
| **Always include the relevant spec excerpt** | AI can't remember previous conversations reliably |
| **Review generated code against the spec** | Verify the code matches, don't trust blindly |
| **Update specs if you discover issues** | Specs are living documents — don't let them go stale |
| **Never let AI modify specs without your approval** | You own the specs; AI is the implementer |

### Handling Spec Deviations During Implementation

```
Discovery: "The API contract says X, but I realize Y would be better"
     ↓
DO NOT just change the code
     ↓
FIRST update the API contract spec
     ↓
THEN update any downstream specs affected (UI, verification)
     ↓
THEN implement the change
```

---

## 13. Prompt Templates

### Quick Reference: One-Line Prompts for Each Phase

| Phase | Quick Prompt |
|-------|-------------|
| 0 | *"Here's my project context: [paste]. Summarize your understanding and ask clarifying questions."* |
| 1 | *"Generate the project constitution with non-negotiable principles, tech constraints, and quality standards."* |
| 2 | *"Generate the PRD with prioritized workflows and acceptance criteria."* |
| 3 | *"Generate the data model spec with ERD, entity details, business rules, and seed strategy."* |
| 4 | *"Generate the API contract with all endpoints, schemas, status codes, and error cases."* |
| 5 | *"Generate the UI/UX spec with design tokens, component specs, page wireframes, and responsive rules."* |
| 6 | *"Generate the architecture spec with system diagram, file structure, data flows, and deployment."* |
| 7 | *"Generate the implementation plan with phases and atomic task breakdown."* |
| 8 | *"Generate the verification spec with test matrices and a full E2E walkthrough."* |
| 9 | *"Implement task T-XXX following this spec: [paste]"* |

### Revision Prompt Templates

When the AI's output needs changes:

```markdown
# Specific correction
"In the data model spec, change the `amount` field from Float to Decimal(12,2).
The rationale is: floating-point arithmetic causes rounding errors with currency."

# Structural change
"The API contract is missing pagination for the vendors endpoint.
Add it following the same envelope pattern used for bills."

# Scope change
"Remove workflow P7 (Vendor Management) from the PRD.
It's out of scope. Move it to the 'Out of Scope' table with the reason:
'Vendors can be managed via seed data for the MVP.'"

# Tone/clarity
"The constitution principles are too vague. Rewrite principle #3
so it's specific enough that I could write a test for it."
```

---

## 14. Anti-Patterns to Avoid

### ❌ Don't: "Generate all specs at once"

**Why it fails:** The AI loses context in a single massive output. Specs become internally inconsistent.

**Do instead:** Generate one artifact at a time. Review and approve before moving on.

---

### ❌ Don't: Skip the review step

**Why it fails:** AI makes plausible-sounding assumptions that don't match your intent. These propagate through all downstream specs.

**Do instead:** Read every generated spec. Challenge assumptions. Ask "why did you choose X over Y?"

---

### ❌ Don't: Use specs as read-only documentation

**Why it fails:** Code evolves during implementation. Stale specs are worse than no specs — they mislead.

**Do instead:** When implementation reveals a spec error, update the spec FIRST, then fix the code.

---

### ❌ Don't: Over-specify implementation details

**Why it fails:** Specs should define WHAT, not HOW. If the spec dictates variable names and loop structures, it's too rigid.

**Do instead:** Specify behavior, interfaces, and constraints. Let the implementation breathe.

```markdown
# ❌ Over-specified
"Create a for loop that iterates over the bills array and checks
if bill.status === 'DRAFT' using a strict equality check..."

# ✅ Well-specified
"The delete operation must validate that the bill is in DRAFT status.
If not, return 400 with error message 'Only draft bills can be deleted'."
```

---

### ❌ Don't: Generate specs for a project you don't understand

**Why it fails:** If you can't evaluate whether the AI's output is correct, the specs are garbage-in-garbage-out.

**Do instead:** Spend time understanding the domain first. Study reference products. Then use AI to structure your understanding into formal specs.

---

### ❌ Don't: Treat every line as sacred once written

**Why it fails:** Early specs WILL need revision as later specs reveal inconsistencies.

**Do instead:** Expect ~2-3 revision passes across all specs before they stabilize. Budget that time.

---

## 15. Artifact Traceability Matrix

Every artifact should trace back to its source and forward to its implementation:

```
Challenge Brief
  └──▶ 00-constitution.md (principles derived from brief)
        └──▶ 01-product-requirements.md (workflows scoped by constitution)
              └──▶ 02-data-model-spec.md (entities support all workflows)
              │     └──▶ server/prisma/schema.prisma
              │
              └──▶ 03-api-contract.md (endpoints serve all workflows)
              │     └──▶ server/src/routes/*.ts
              │
              └──▶ 04-ui-ux-spec.md (pages implement all workflows)
              │     └──▶ client/src/pages/*.tsx
              │     └──▶ client/src/index.css
              │
              └──▶ 05-architecture.md (structure holds all components)
                    └──▶ file tree, Docker files, configs

06-implementation-plan.md ←── derives from 01 through 05
07-task-breakdown.md ←── decomposes 06
08-verification-spec.md ←── validates 01 through 05
```

### Cross-Reference Convention

When writing specs, use explicit references:

```markdown
# In the API contract:
"See PRD §P1 (Bill Lifecycle) for the complete state machine."
"See Data Model §3.2 (Bill entity) for field definitions."

# In the task breakdown:
"T-021 implements API Contract §2.6 (Submit action)"
"T-048 implements UI/UX Spec §4.1 (Dashboard page)"

# In the verification spec:
"Test L1 validates PRD §P1 acceptance criterion #1"
```

---

## 16. Checklist: SDD Completeness

Use this checklist before starting implementation. Every item must be ✅:

### Constitution
- [ ] Mission statement is one clear sentence
- [ ] At least 5 non-negotiable principles, each testable
- [ ] Tech stack fully specified with versions
- [ ] Architectural rules cover data, API, and frontend patterns
- [ ] Design system rules specify brand colors and typography

### Product Requirements
- [ ] Problem statement explains the pain point
- [ ] At least 3 prioritized workflows
- [ ] Every workflow has ≥3 acceptance criteria
- [ ] Out-of-scope table with ≥5 items and justifications
- [ ] Non-functional requirements include performance and accessibility

### Data Model
- [ ] ERD diagram exists and is valid
- [ ] Every entity has a complete field table
- [ ] Business rules are explicit for create, edit, delete
- [ ] Enum values have descriptions and entry conditions
- [ ] Seed data strategy describes realistic demo scenario

### API Contract
- [ ] Every workflow maps to ≥1 endpoint
- [ ] Every endpoint has request + response schema
- [ ] Error cases are documented with status codes
- [ ] Pagination is standardized
- [ ] At least one full JSON example per endpoint

### UI/UX Specification
- [ ] Design tokens cover colors, typography, spacing, radii, shadows
- [ ] At least 4 component specs (buttons, forms, tables, modals)
- [ ] Every page has a wireframe
- [ ] Responsive breakpoints ≥3
- [ ] Loading, empty, and error states defined

### Architecture
- [ ] System architecture diagram exists
- [ ] Complete file tree with descriptions
- [ ] At least 2 data flow sequence diagrams
- [ ] State machine diagram for primary entity
- [ ] Deployment diagram for dev and production

### Implementation Plan
- [ ] Divided into ≥3 phases
- [ ] Each phase has a clear deliverable
- [ ] Time estimates are realistic
- [ ] Risk mitigation table exists
- [ ] Quality gates defined per phase

### Task Breakdown
- [ ] Total tasks ≥20 (for non-trivial projects)
- [ ] Each task completable in ≤30 minutes
- [ ] Each task is independently testable
- [ ] Dependency graph identifies parallelization

### Verification Specification
- [ ] Every API endpoint has ≥1 test case
- [ ] UI test cases cover happy path + error path
- [ ] Responsive testing covers min and max widths
- [ ] Full E2E walkthrough exists with ≥15 steps
- [ ] Docker verification is included

---

## Appendix A: Session Management

### Starting a New Session

AI assistants don't remember previous conversations. When resuming work:

```markdown
I'm continuing SDD work on [project name].

Here are the specs completed so far:
- Constitution: [paste or reference file]
- PRD: [paste or reference file]
- Data Model: [approved/in-progress]

We're currently working on: [current phase]

Here's where we left off: [specific context]
```

### Saving Progress

After each phase, save the approved artifact to your project directory. Recommended structure:

```
.sdd/
├── README.md              ← Index + reading order
├── 00-constitution.md
├── 01-product-requirements.md
├── 02-data-model-spec.md
├── 03-api-contract.md
├── 04-ui-ux-spec.md
├── 05-architecture.md
├── 06-implementation-plan.md
├── 07-task-breakdown.md
└── 08-verification-spec.md
```

---

## Appendix B: Scaling SDD to Larger Projects

For projects beyond a take-home challenge:

| Scale | Adaptation |
|-------|------------|
| **Multi-developer** | Add a RACI matrix per spec. Assign spec ownership. |
| **Multi-service** | One API contract per service. Shared constitution. |
| **Long-lived product** | Version specs (v1.0, v1.1). Maintain changelog. |
| **Automated testing** | Verification spec becomes the test plan. Generate test stubs from it. |
| **CI/CD** | API contract can generate OpenAPI spec → automated contract tests. |
| **Design system** | UI/UX spec becomes a Storybook source of truth. |

---

## Appendix C: Quick-Start Template

For those who want to jump in immediately, here's the single prompt that kicks off the entire SDD process:

```markdown
I want to build [product description] using [tech stack].

Here's the challenge/brief:
[paste]

Here's reference material:
[paste or link]

Let's use Spec-Driven Development. Generate the artifacts in this order:
1. Constitution (principles + constraints)
2. PRD (workflows + acceptance criteria)
3. Data Model (ERD + entities + business rules)
4. API Contract (all endpoints + schemas)
5. UI/UX Spec (design tokens + wireframes)
6. Architecture (diagrams + file structure)
7. Implementation Plan (phases + tasks)
8. Verification Spec (test matrices + E2E scenario)

Start with #1 (Constitution). After I approve each artifact,
move to the next. Do NOT skip ahead.
```

---

*This guide is itself an SDD artifact — a specification for how to create specifications.* 🔄
