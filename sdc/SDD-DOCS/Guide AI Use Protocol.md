# AI Use Protocol

> **Version:** 1.0  
> **Last Updated:** 2026-04-23  
> **Status:** Active

---

## 1. Purpose

This document defines how AI tools and services are used within an organization or project.

**Objectives:**

* Prevent security, legal, and compliance risks
* Standardize AI usage across teams and contributors
* Increase execution speed without compromising control or accountability

**Scope:**

This protocol applies to all team members, contractors, and contributors who use AI tools in any capacity — including code generation, content creation, data analysis, and workflow automation.

**This protocol is mandatory and will evolve over time.**

---

## 2. Core Principle

* AI is a tool. Humans are responsible.
* AI does not make decisions
* AI does not control systems
* The user is fully accountable for all outputs

---

## 3. AI Usage Categories

### 3.1 Tier 1 — Automation (No Human Review Required)

**Definition:**
Low-risk tasks where AI transforms existing content without creating new meaning.

**Allowed Use Cases:**

* Translation between languages
* Text formatting / cleanup
* Summarization of existing content
* Data extraction from structured sources
* Rewriting (same meaning preserved)
* Classification / tagging

**Conditions:**

* No sensitive or confidential data is involved
* No legal, financial, or regulatory impact
* No decision-making outputs

---

### 3.2 Tier 2 — Assisted Generation (Human Validation Required)

**Definition:**
AI generates new content, logic, or ideas that will influence decisions, products, or communication.

**Allowed Use Cases:**

* Code generation
* Documentation and technical writing
* Product specifications
* User flows and workflows
* UI components
* Marketing and public-facing content
* Simulations and prototyping

**Mandatory Rule:**
All outputs must be reviewed and approved by a qualified human before use.

**Validator Responsibility:**

* Accuracy — Is the output factually correct?
* Compliance — Does it conform to applicable regulations?
* Alignment — Does it match product/project requirements?

**Validation Checklist:**

* Is the output correct and complete?
* Does it comply with applicable regulations and policies?
* Could it be misinterpreted as authoritative professional advice?
* Does it introduce operational, reputational, or legal risk?
* Has it been reviewed by someone with domain expertise?

If unclear → escalate to the appropriate stakeholder.

---

### 3.3 Tier 3 — Prohibited Use (Strictly Forbidden)

#### A. Domain-Critical Decisions

* Generating professional advice (legal, medical, financial, etc.) presented as authoritative
* Making autonomous decisions that require licensed expertise
* Communicating recommendations to end users without appropriate disclaimers

#### B. Autonomous System Actions

* Executing actions in production environments
* Triggering irreversible business operations (transactions, deployments, data mutations)
* Autonomous agents performing actions without human confirmation

#### C. Security Violations

* Sharing API keys, credentials, tokens, or secrets with AI services
* Exposing private repositories or proprietary source code
* Connecting AI tools directly to internal production systems

#### D. Sensitive Data Exposure

* Personally Identifiable Information (PII)
* Protected data subject to regulatory requirements (e.g., HIPAA, GDPR, PCI-DSS)
* Confidential business data, trade secrets, or proprietary algorithms
* Legal agreements, partner contracts, or NDA-covered materials

---

## 4. Input & Access Restrictions

**Never provide AI with:**

* Production system access
* Database credentials or connection strings
* API keys / secrets / tokens
* Personal or sensitive user data
* Confidential system architecture details
* Proprietary business agreements

**Allowed Inputs:**

* Mock / synthetic data
* Sanitized and anonymized data
* Public or non-sensitive documentation

---

## 5. AI Tools & Infrastructure

This section governs which AI tools can be used and under what conditions.

### 5.1 Approved Tool Types

* LLM interfaces (e.g., ChatGPT, Claude, Gemini)
* IDE copilots and code assistants
* Internal AI-powered workflows
* MCP Servers (Model Context Protocol)
* Automation tools with AI capabilities

> **Note:** Teams should maintain an internal registry of approved tools and versions.

---

### 5.2 MCP Servers & Advanced Integrations

**Definition:**
MCP servers or similar systems that allow AI models to access tools, retrieve data, or execute workflows.

**Rules for MCP / Tool Integrations**

**STRICT REQUIREMENTS:**

* **No Production Access**
  AI-connected tools must NOT interact with production environments

* **Sandbox Only**
  Only staging, development, or sandbox environments are permitted

* **No Secrets Exposure**
  API keys and credentials must never be passed through prompts
  Use secure environment variables or secret managers only

* **Scoped Permissions**
  Tools must operate with minimal required access (least privilege principle)

* **No Autonomous Execution**
  AI must not autonomously execute:

  * Irreversible business operations
  * Data mutations in shared environments
  * External service calls with real-world consequences

* **Auditability**
  All tool usage must be traceable and logged

---

### 5.3 Tool Approval Process

Before adopting a new AI tool or integration:

**Evaluate:**

* What data will it access?
* What are the security and privacy risks?
* What is the compliance impact?

**Required:**

* Approval from the responsible team lead or product owner
* Engineering validation (if the tool integrates with systems)
* Documented use case and scope of access

---

### 5.4 Forbidden Tool Usage

**Connecting AI directly to:**

* Production databases or live systems
* Domain-critical external APIs or third-party services
* Systems that process real user data

**Uploading to AI services:**

* Real user data in any form
* Confidential or proprietary business data
* Credentials, tokens, or access keys

---

## 6. Decision Framework (Quick Check)

Before using AI for any task, ask yourself:

| # | Question | If YES → |
|---|----------|----------|
| 1 | Does this involve real user data or PII? | **Stop** — use mock/sanitized data |
| 2 | Am I exposing credentials, keys, or system access? | **Stop** — use environment variables |
| 3 | Could this output create legal, regulatory, or compliance risk? | **Stop** — require expert review |
| 4 | Will this output go live or reach users without human review? | **Stop** — add a review step |
| 5 | Could this action trigger an irreversible operation? | **Stop** — require explicit confirmation |
| 6 | Am I unsure whether this use case is appropriate? | **Stop** — escalate to your team lead |

**Rule of thumb:** If any answer is **YES**, stop and require validation before proceeding.

---

## 7. Responsibility Model

The AI user is responsible for:

* **Inputs** — What data and context is provided to AI
* **Outputs** — What AI generates and how it is used
* **Consequences** — Any impact resulting from AI-assisted work

**No exceptions.**

---

## 8. Compliance Alignment

This protocol is designed to align with common compliance and regulatory frameworks. Teams should map their applicable requirements to this protocol's controls.

**Examples of applicable frameworks:**

| Framework | Relevance |
|-----------|-----------|
| GDPR | Personal data protection and privacy |
| SOC 2 | Security, availability, and confidentiality controls |
| HIPAA | Protected health information |
| PCI-DSS | Payment card data security |
| ISO 27001 | Information security management |
| Industry-specific regulations | As applicable to your domain |

**Non-compliance can result in:**

* Project delays or blocked releases
* Regulatory exposure and legal liability
* Loss of user or stakeholder trust

> **Action Item:** Each team should document which frameworks apply to their project and ensure this protocol's controls satisfy those requirements.

---

## 9. Evolution & Versioning

This is a living document.

It will evolve based on:

* Product and project needs
* Regulatory and compliance updates
* Team learnings and incident retrospectives
* Changes in AI tooling and capabilities

### Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-23 | Sebastián Larrauri | Initial version |


### Review Cadence

* **Quarterly:** Review for relevance and completeness
* **On incident:** Update if an AI-related incident reveals a gap
* **On tool adoption:** Review when new AI tools are introduced

---

## Appendix A: Domain Customization

This protocol is designed as a **universal base layer**. Teams operating in regulated or specialized domains should extend it with domain-specific overlays.

### How to Customize

1. **Keep the core protocol unchanged** — it provides universal governance
2. **Add a domain-specific addendum** that extends §3.3 (Prohibited Use), §4 (Input Restrictions), and §8 (Compliance)
3. **Reference the addendum** in your team's onboarding documentation

### Example Overlays by Industry

#### Fintech / Financial Services

* Prohibit AI from generating content that could be interpreted as financial advice
* Prohibit autonomous execution of transactions, payments, or investment routing
* Add KYC/AML data to the sensitive data list (§3.3-D)
* Add custody risk controls and financial API restrictions (Plaid, Stripe, etc.)
* Map to PCI-DSS, SOX, and applicable financial regulations

#### Healthcare

* Prohibit AI from generating medical diagnoses or treatment recommendations
* Add PHI (Protected Health Information) to the sensitive data list
* Require HIPAA-compliant data handling for all AI interactions
* Prohibit uploading patient records or clinical data to external AI services

#### E-commerce / Retail

* Prohibit AI from autonomously modifying product pricing or inventory
* Add customer purchase history and payment data to the sensitive data list
* Require review of AI-generated product descriptions for regulatory claims
* Map to PCI-DSS for payment data handling

#### SaaS / Platform

* Prohibit AI from modifying access control, permissions, or tenant data
* Add multi-tenant data isolation to security requirements
* Require review of AI-generated API documentation for accuracy
* Map to SOC 2 Type II controls

---

*This protocol is part of the [Spec-Driven Development Guides](SDD/README.md) — a methodology for structured, AI-assisted software engineering.*
