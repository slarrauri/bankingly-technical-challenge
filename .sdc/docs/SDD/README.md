# 📐 SDD Guides — Spec-Driven Development for AI-Assisted Engineering

> **A comprehensive methodology for structuring AI-assisted software development around formal specifications, agent configuration, and enterprise-grade artifact management.**

---

## Overview

This repository contains four in-depth guides that form a complete framework for **Spec-Driven Development (SDD)** — a methodology where formal specifications are authored *before* any code is written, and AI coding assistants are configured to follow those specifications precisely.

The guides address four interconnected concerns:

| # | Guide | Focus | Key Question |
|---|-------|-------|--------------|
| 1 | [Interacting with AI to Generate SDD Artifacts](#-guide-1-interacting-with-ai-to-generate-sdd-artifacts) | Workflow | *How do I create specs with AI?* |
| 2 | [Enterprise SDD — Extended Artifact Catalog](#-guide-2-enterprise-sdd--extended-artifact-catalog) | Artifacts | *What artifacts does my project need?* |
| 3 | [Configuring AI Coding Agents for Your Project](#-guide-3-configuring-ai-coding-agents-for-your-project) | AI Configuration | *How do I make AI follow my conventions?* |
| 4 | [AI Use Protocol](#-guide-4-ai-use-protocol) | Governance | *What are the rules for using AI responsibly?* |

---

## Who Is This For?

- **Developers** using AI coding assistants (Gemini, Copilot, Cursor, Claude, Antigravity,etc.) who want consistent, spec-compliant output
- **Tech leads** establishing AI-assisted development standards for their teams
- **Solo developers** building portfolio or production projects with structured AI workflows
- **Engineering teams** scaling AI tooling across multiple contributors

---

## The SDD Philosophy

```
Traditional Development          Spec-Driven Development
─────────────────────           ───────────────────────
  Idea → Code → Docs              Idea → Specs → Code
  (docs are afterthought)         (specs drive everything)
  AI guesses conventions          AI follows conventions
  Inconsistent output             Consistent, traceable output
```

### Core Principles

1. **Specs before code** — Define *what* and *why* before *how*
2. **AI as technical writer** — You provide intent; AI structures it into formal specifications
3. **Agent configuration as onboarding** — Configure AI the same way you'd onboard a new developer
4. **Traceability** — Every line of code traces back to a specification artifact

---

## 📖 Guide 1: Interacting with AI to Generate SDD Artifacts

**File:** `Guide Interacting with AI to Generate SDD Artifacts.md`

### What It Covers

A 9-phase sequential workflow for generating a complete specification suite using AI, from initial context loading through implementation:

```
Phase 0: Context Loading      →  Give AI your project context
Phase 1: Constitution         →  Non-negotiable rules & principles
Phase 2: Product Requirements →  Workflows & acceptance criteria
Phase 3: Data Model           →  ERD, entities, business rules
Phase 4: API Contract         →  Endpoints, schemas, error cases
Phase 5: UI/UX Specification  →  Design tokens, wireframes, responsive rules
Phase 6: Architecture         →  System diagrams, file structure, deployment
Phase 7: Implementation Plan  →  Phases, tasks, time estimates
Phase 8: Verification Spec    →  Test matrices, E2E walkthrough
Phase 9: Implementation       →  AI-assisted code generation from specs
```

### Key Sections

- **Prompt templates** for each phase with structured context injection
- **Review checklists** to validate AI-generated specs before approval
- **Anti-patterns** — common mistakes when using AI for spec generation
- **Artifact traceability matrix** showing how specs reference each other
- **SDD completeness checklist** — the gate before starting implementation
- **Session management** — how to resume work across AI conversations

---

## 🏢 Guide 2: Enterprise SDD — Extended Artifact Catalog

**File:** `Guide Enterprise SDD - Extended Artifact Catalog.md`

### What It Covers

Maps the complete artifact landscape needed for production software, organized into 6 layers:

| Layer | Artifacts | Scope |
|-------|-----------|-------|
| **1. Product** | Constitution, PRD, Data Model, API Contract, UI/UX, Architecture, Plan, Tasks, Verification | Core SDD specs |
| **2. Engineering Process** | Git Strategy, CI/CD Pipeline, Environment Strategy, Release Management, Code Review Standards | Team workflows |
| **3. Security & Compliance** | Security Spec (Auth, RBAC, OWASP), Data Governance (PII, GDPR) | Trust & compliance |
| **4. Operations** | Observability, Incident Response, Performance Spec (SLOs) | Production readiness |
| **5. AI Agent Config** | AGENTS.md, rules.md, skills.md, tool-specific configs | AI alignment |
| **6. Knowledge** | Onboarding Guide, ADRs, Dependency Policy, Glossary | Team scaling |

### Key Sections

- **Adoption matrix** — which artifacts to create based on project scale (Solo → Small Team → Enterprise)
- **Full templates** for each artifact with ready-to-use markdown structures
- **Complete enterprise file tree** showing where every artifact lives
- **Phased creation order** — what to create before code, before first sprint, before production, and ongoing

---

## 🤖 Guide 3: Configuring AI Coding Agents for Your Project

**File:** `Guide Configuring AI Coding Agents for Your Project.md`

### What It Covers

A deep-dive into creating configuration files that make AI coding assistants behave consistently within your specific codebase.

#### The Three Configuration Files

| File | Purpose | Analogy |
|------|---------|---------|
| **AGENTS.md** | *Who* does what — scope, permissions, coordination | Org chart |
| **rules.md** | *How* code should be written — conventions & constraints | Style guide |
| **skills.md** | *What* to do — parameterized task templates | Playbook |

### Key Sections

- **rules.md anatomy** — 7-section structure (Identity → Universal → Backend → Frontend → Styling → Testing → Forbidden)
- **skills.md design** — parameterized recipe templates with 5-part structure
- **Tool-specific configs** for Gemini, Copilot, Cursor, Claude, Windsurf, and Aider
- **Writing effective rules** — the quality spectrum from vague to precise
- **Cross-tool compatibility matrix** — feature support across 6 AI tools
- **Anti-patterns** — 6 common mistakes with concrete alternatives
- **Maintenance cadence** — weekly, monthly, quarterly review cycles
- **Quick-start template** — a 15-line rules.md to get started in 15 minutes

---

## 🛡️ Guide 4: AI Use Protocol

**File:** `Guide AI Use Protocol.md`

### What It Covers

A governance framework defining how AI tools and services should be used across any organization or project — regardless of industry, team size, or regulatory environment.

#### Risk-Tiered Usage Model

| Tier | Category | Human Review | Example |
|------|----------|--------------|---------|
| **1** | Automation | Not required | Translation, formatting, summarization |
| **2** | Assisted Generation | Required | Code generation, documentation, UI components |
| **3** | Prohibited Use | Blocked | Autonomous system actions, sensitive data exposure |

### Key Sections

- **Usage categories** — risk-tiered classification of AI tasks (Automation → Assisted Generation → Prohibited)
- **Input & access restrictions** — what data can and cannot be shared with AI
- **Tool governance** — approval process, MCP server rules, and forbidden integrations
- **Decision framework** — 6-question quick-check matrix before using AI
- **Compliance alignment** — maps to common frameworks (GDPR, SOC 2, HIPAA, PCI-DSS, ISO 27001)
- **Domain customization appendix** — overlay templates for Fintech, Healthcare, E-commerce, and SaaS

> **Note:** This protocol is designed as a universal base layer. Teams in regulated industries extend it with domain-specific addendums (see Appendix A in the document).

---

## Quick Start

### Option 1: 15-Minute Setup

Start with the minimum viable agent configuration from Guide 3, Appendix A:

1. Create `.gemini/rules.md` (or your tool's config file)
2. Add your project identity, 5–10 key conventions, and 5 forbidden patterns
3. Start coding with AI — add one new rule every time AI gets something wrong

### Option 2: Full SDD Workflow

Follow the phased approach from Guide 1:

1. Load context into AI (Phase 0)
2. Generate each spec artifact sequentially (Phases 1–8)
3. Review and approve each artifact before moving on
4. Use approved specs as blueprints for AI-assisted implementation (Phase 9)

### Option 3: Enterprise Adoption

Use Guide 2's layered artifact map:

1. **Before any code:** Layers 1 + 5 (Product specs + AI agent config)
2. **Before first sprint:** Layer 2 (Engineering process) + AI Use Protocol (Guide 4)
3. **Before production:** Layers 3 + 4 (Security + Operations)
4. **Ongoing:** Layer 6 (Knowledge & onboarding)

---

## Artifact Dependency Graph

```
Challenge Brief / Product Idea
  │
  └──▶ 00-constitution.md
        └──▶ 01-product-requirements.md
              ├──▶ 02-data-model-spec.md ──▶ schema.prisma
              ├──▶ 03-api-contract.md ──▶ routes/*.ts
              ├──▶ 04-ui-ux-spec.md ──▶ pages/*.tsx + index.css
              └──▶ 05-architecture.md ──▶ file tree + Docker

06-implementation-plan.md ◀── derives from 01–05
07-task-breakdown.md      ◀── decomposes 06
08-verification-spec.md   ◀── validates 01–05

AGENTS.md + rules.md + skills.md ◀── inform ALL of the above
AI Use Protocol ◀── governs HOW AI is used across all of the above
```

---

## Key Takeaways

> **Agent configs are your project's onboarding document for AI.**
> Just as you'd give a new developer a style guide, coding standards, and architecture overview — agent configs give the same context to your AI. The difference: humans can infer; AI needs explicit instruction.

```
Time to write agent configs:     ~1–2 hours
Time saved per AI interaction:   ~5–15 minutes
Break-even after:                ~10–20 interactions
Lifetime savings across team:    Hundreds of hours
```

---

## License 
`CC0 1.0 Universal`

These guides are provided for educational and professional development purposes.

---

<p align="center"><em>Spec-Driven Development: Because the best code starts with the best specifications.</em></p>
