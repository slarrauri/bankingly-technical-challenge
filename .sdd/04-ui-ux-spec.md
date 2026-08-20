# 🎨 04 — UI/UX Specification

> **Project:** AML Alert Investigation Copilot  
> **Target Device:** Desktop Compliance Workstation (1280px+ optimized, responsive down to 768px)  
> **Theme:** Modern Fintech Slate / Dark & Light Mode Support

---

## 1. Design Principles

1. **Information Density & Clarity:** Compliance analysts handle complex data; layout must maximize scannability without clutter.
2. **Provenance at a Glance:** Every finding must display clickable evidence badges that trace directly to raw transactions or KYC notes.
3. **Friction at the Decision Gate:** Approvals and actions must be explicit, intentional, and require secondary confirmation.

---

## 2. Wireframes & Layout Structure

### 2.1 Investigation Workspace Wireframe (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏛️ BANCO RÍO SUR  |  AML Investigation Console             👤 Andrea Silva │
├─────────────────────────────────────────────────────────────────────────────┤
│ ◀ Back to Alerts    Alert: AML-00127  |  Martín Pereira (CUST-0042)        │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 📊 ALERT & CUSTOMER CONTEXT          │ 🤖 COPILOT INVESTIGATION REPORT       │
│                                      │                                      │
│ Risk Score: [ 78 / 100 ] HIGH        │ Status: [ AWAITING APPROVAL ]        │
│ Trigger: Unusual Transaction Pattern │ Confidence: [ 84% ]                  │
│ Customer Since: Apr 2022             │                                      │
│ Declared Income: USD 4,500 / mo      │ Summary:                             │
│ KYC Status: [ VERIFIED ]             │ Transaction volume spiked +342% vs   │
│                                      │ baseline. Rapid outflow to Andes     │
│ ──────────────────────────────────── │ Trading Ltd without contract file.   │
│ 💳 RECENT TRANSACTIONS               │                                      │
│ • 2026-07-12: +$18,500 (Andes Trad)  │ 🔍 FINDINGS & EVIDENCE:              │
│ • 2026-07-13: +$21,000 (Andes Trad)  │ 1. Volume spike +342% [Evidence #1]  │
│ • 2026-07-13: -$20,500 (Wire Out)    │ 2. New unverified CP [Evidence #2]   │
│ • 2026-07-14: -$17,900 (Wire Out)    │                                      │
│                                      │ ⚠️ MISSING INFORMATION:              │
│ 📜 APPLICABLE POLICIES               │ • Commercial contract for consulting │
│ • P-001: Material Volume Increase    │                                      │
│ • P-002: Rapid Fund Movement         │ ⚖️ RECOMMENDATION:                   │
│ • P-003: Profile Mismatch Escalation │ [ 🔴 ESCALATE ALERT (SAR Filing) ]   │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ 🛡️ DECISION BAR: [ ✅ Approve Recommendation ]  [ ❌ Reject ]  [ ❓ Request Info ] │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Specifications

### 3.1 `RiskScoreBadge`
- `0–39`: Green background, `LOW RISK`.
- `40–69`: Yellow/Amber background, `MEDIUM RISK`.
- `70–100`: Crimson/Red background, `HIGH / CRITICAL RISK`.

### 3.2 `EvidenceCitationTag`
- Renders as interactive pill badge: `[ 🔍 Summary: +342% ]` or `[ 📄 KYC: USD 4,500 ]`.
- Clicking highlights corresponding row in transaction table or KYC card.

### 3.3 `ApprovalModal` (Decision Gate)
- Dialog opens upon clicking **Approve** or **Reject**.
- Summary of action to be executed: `Transition alert AML-00127 to ESCALATED_SAR`.
- Mandatory or optional justification notes input.
- Explicit buttons: `Cancel` and `Confirm Execution`.

---

## 4. State Handling

- **Loading State:** Skeleton loader on findings card with pulsing indicator: *"Agent gathering evidence from customer and transaction tools..."*.
- **Empty State:** When no open alerts exist, display clean banner: *"All AML alerts are currently investigated and resolved."*.
- **Error State:** If investigation fails schema or timeout, show amber warning box with technical details and a *"Retry Investigation"* button.
