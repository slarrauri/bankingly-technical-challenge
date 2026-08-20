# Skills — Reusable Task Templates for AML Copilot

> Use these parameterized recipes to perform recurring tasks with consistent quality.
> Always replace `{parameters}` with actual values.

---

## Skill: Add New AML Tool to Harness

### Description
Adds a new read-only data tool for the AI agent to consult during investigations, with full typing, service layer isolation, and harness registration.

### Parameters
- `{tool_name}`: snake_case name (e.g. `get_sanctions_check`)
- `{description}`: Clear explanation of what data the tool returns
- `{input_schema}`: Pydantic input model
- `{output_schema}`: Pydantic output model
- `{service_method}`: Corresponding method in `backend/tools/services/`

### Steps
1. **Define Schema:** Add `{input_schema}` and `{output_schema}` in `backend/tools/schemas.py`.
2. **Implement Service:** Add data retrieval and deterministic processing in `backend/tools/services/{domain}.py`. Ensure `institution_id` filter is applied.
3. **Register Tool in Harness:** In `backend/harness/tool_registry.py`:
   - Add tool definition to `AUTHORIZED_INVESTIGATION_TOOLS`.
   - Wire execution handler to service method.
4. **Update Specs:** Document tool input/output in `.sdd/03-api-contract.md` and `.sdd/05-architecture.md`.
5. **Add Unit Test:** In `tests/unit/test_tools.py`, verify happy path, invalid inputs, and tenant isolation.

---

## Skill: Add Evaluation Scenario to Benchmark

### Description
Adds a new test case to the 25-case evaluation benchmark with ground truth and category classification.

### Parameters
- `{case_id}`: E.g., `EVAL-026`
- `{category}`: One of `[CLEAR, LEGITIMATE_UNUSUAL, AMBIGUOUS, CONTRADICTORY, MISSING_DATA, ADVERSARIAL, SECURITY_GATE]`
- `{customer_id}`: Target customer ID
- `{alert_id}`: Target alert ID
- `{expected_recommendation}`: One of `[CLOSE_ALERT, ESCALATE_ALERT, REQUEST_INFORMATION]`
- `{expected_findings}`: List of expected key findings
- `{expected_missing_info}`: List of expected missing items (if applicable)

### Steps
1. **Update Evaluation Dataset:** Append row in `data/evaluation/aml_evaluation_ground_truth.csv` (or `.json`).
2. **Verify Simulated Data Exists:** Ensure corresponding alert, customer KYC, and transactions exist in `data/seed/`.
3. **Run Grader:** Execute `pytest tests/evaluation/test_eval_runner.py -k {case_id}`.
4. **Check Metrics:** Verify that the test correctly evaluates Recommendation Accuracy and Evidence Grounding.
5. **Update Verification Spec:** Add the scenario to `.sdd/08-verification-spec.md`.

---

## Skill: Add New AML Institution Policy

### Description
Adds a new configurable AML policy to the institution's policy registry.

### Parameters
- `{policy_id}`: E.g., `P-005`
- `{title}`: Policy title
- `{category}`: E.g., `TRANSACTION_VELOCITY`, `KYC_INCONSISTENCY`, `HIGH_RISK_JURISDICTION`
- `{description}`: Policy text and condition
- `{severity}`: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

### Steps
1. **Database Seed:** Add policy entry to `data/seed/aml_policies.json` or SQL seed.
2. **Policy Service:** Ensure `get_aml_policies` can filter and retrieve the new category in `backend/tools/services/policy_service.py`.
3. **Prompt Definition:** If policy indexing metadata is updated, reflect in `.sdd/02-data-model-spec.md`.
4. **Verification:** Test query via `get_aml_policies(policy_category="{category}")`.

---

## Skill: Verify System Safety Invariants

### Description
Executes the full suite of security and invariant tests to prove architectural compliance with `INVARIANTS.md`.

### Steps
1. Run security test suite:
   ```bash
   pytest tests/security/ -v
   ```
2. Verify all 10 invariants:
   - `INV-001`: Agent cannot execute actions (Denied).
   - `INV-002`: Unapproved execution blocked (Denied).
   - `INV-003`: Unauthorized analyst approval rejected.
   - `INV-004`: Idempotent action execution (no duplicate runs).
   - `INV-005`: Cross-tenant data query returns Forbidden.
   - `INV-006`: Prompt injection in transaction text treated as inert string.
   - `INV-007`: Unsupported claims rejected by grader.
   - `INV-008`: Missing evidence yields `REQUEST_INFORMATION` or explicit missing info list.
   - `INV-009`: Invalid LLM output JSON fails safely without mutating state.
   - `INV-010`: Tool database failure recorded as missing data, never fabricated.
3. Generate invariant verification report in `evals/invariants_report.json`.
