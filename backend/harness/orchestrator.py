from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.domain.models import (
    AMLAlert,
    Investigation,
    Recommendation,
    InvestigationStatus,
    AlertStatus,
)
from backend.harness.tool_registry import AUTHORIZED_READ_TOOLS
from backend.harness.validator import validate_investigation_output
from backend.harness.state_machine import validate_investigation_transition
from backend.harness.audit_service import log_audit_event
from backend.agent.prompt_engine import SYSTEM_PROMPT, build_investigation_prompt
from backend.agent.llm_client import get_llm_client


class InvestigationOrchestrator:
    def __init__(self, db: Session, institution_id: str = "BANK-RIO-SUR"):
        self.db = db
        self.institution_id = institution_id
        self.llm = get_llm_client()

    def run_investigation(
        self,
        alert_id: str,
        analyst_id: str = "ANA-0091",
    ) -> Dict[str, Any]:
        """
        Orchestrates an automated AML alert investigation:
        1. Initializes Investigation record (Status: INVESTIGATING).
        2. Calls authorized read-only data tools to collect evidence.
        3. Invokes LLM with strict bounded context prompt.
        4. Validates schema using Pydantic (max 2 retries).
        5. Saves Recommendation and transitions to AWAITING_APPROVAL.
        """
        # Step 1: Fetch alert
        alert = (
            self.db.query(AMLAlert)
            .filter(AMLAlert.id == alert_id, AMLAlert.institution_id == self.institution_id)
            .first()
        )
        if not alert:
            raise ValueError(f"Alert '{alert_id}' not found for institution '{self.institution_id}'.")

        # Step 2: Initialize or fetch existing investigation
        investigation = (
            self.db.query(Investigation)
            .filter(Investigation.alert_id == alert_id)
            .first()
        )
        if not investigation:
            investigation = Investigation(
                id=f"INV-{alert_id}",
                institution_id=self.institution_id,
                alert_id=alert.id,
                analyst_id=analyst_id,
                status=InvestigationStatus.INVESTIGATING.value,
                created_at=datetime.utcnow(),
            )
            self.db.add(investigation)
            self.db.commit()
            self.db.refresh(investigation)
        else:
            investigation.status = InvestigationStatus.INVESTIGATING.value
            self.db.commit()

        log_audit_event(
            self.db,
            actor_type="SYSTEM_HARNESS",
            actor_id=analyst_id,
            event_type="INVESTIGATION_STARTED",
            payload={"alert_id": alert.id, "customer_id": alert.customer_id},
            investigation_id=investigation.id,
            institution_id=self.institution_id,
        )

        # Step 3: Tool Execution Phase (Gather evidence deterministically)
        tool_alert = AUTHORIZED_READ_TOOLS["get_alert"]["function"](
            self.db, alert.id, self.institution_id
        )
        tool_customer = AUTHORIZED_READ_TOOLS["get_customer_profile"]["function"](
            self.db, alert.customer_id, self.institution_id
        )
        tool_summary = AUTHORIZED_READ_TOOLS["get_transaction_summary"]["function"](
            self.db, alert.customer_id, 30, self.institution_id
        )
        tool_transactions = AUTHORIZED_READ_TOOLS["get_transactions"]["function"](
            self.db, alert.customer_id, None, None, 20, self.institution_id
        )
        tool_prev_alerts = AUTHORIZED_READ_TOOLS["get_previous_alerts"]["function"](
            self.db, alert.customer_id, alert.id, self.institution_id
        )
        tool_policies = AUTHORIZED_READ_TOOLS["get_aml_policies"]["function"](
            self.db, None, self.institution_id
        )

        context_data = {
            "alert": tool_alert.model_dump() if tool_alert else {},
            "customer": tool_customer.model_dump() if tool_customer else {},
            "summary": tool_summary.model_dump() if tool_summary else {},
            "transactions": tool_transactions.model_dump().get("transactions", []) if tool_transactions else [],
            "previous_alerts": tool_prev_alerts.model_dump().get("alerts", []) if tool_prev_alerts else [],
            "policies": tool_policies.model_dump().get("policies", []) if tool_policies else [],
        }

        # Step 4: Prompt generation & LLM reasoning
        user_prompt = build_investigation_prompt(
            context_data["alert"],
            context_data["customer"],
            context_data["summary"],
            context_data["transactions"],
            context_data["previous_alerts"],
            context_data["policies"],
        )

        # Step 5: Validation loop (with max 2 retries)
        max_retries = 2
        validated_result = None
        for attempt in range(max_retries + 1):
            raw_output = self.llm.generate_investigation(SYSTEM_PROMPT, user_prompt, context_data)
            is_valid, parsed_model, error_msg = validate_investigation_output(raw_output)
            if is_valid and parsed_model:
                validated_result = parsed_model
                break

        if not validated_result:
            investigation.status = InvestigationStatus.INVESTIGATION_FAILED.value
            self.db.commit()
            raise ValueError(f"Investigation failed schema validation after {max_retries} retries: {error_msg}")

        # Step 6: Persist structured result & advance state to AWAITING_APPROVAL
        investigation.summary = validated_result.investigation_summary
        investigation.risk_assessment = validated_result.risk_assessment.value
        investigation.confidence_score = validated_result.confidence
        investigation.status = InvestigationStatus.AWAITING_APPROVAL.value

        # Persist recommendation
        rec_data = [f.model_dump() for f in validated_result.findings]
        existing_rec = self.db.query(Recommendation).filter(Recommendation.investigation_id == investigation.id).first()
        if existing_rec:
            existing_rec.action = validated_result.recommendation.value
            existing_rec.rationale = validated_result.rationale
            existing_rec.findings = rec_data
            existing_rec.missing_information = validated_result.missing_information
            existing_rec.applicable_policies = validated_result.applicable_policies
            existing_rec.limitations = validated_result.limitations
            recommendation = existing_rec
        else:
            recommendation = Recommendation(
                id=f"REC-{investigation.id}",
                investigation_id=investigation.id,
                action=validated_result.recommendation.value,
                rationale=validated_result.rationale,
                findings=rec_data,
                missing_information=validated_result.missing_information,
                applicable_policies=validated_result.applicable_policies,
                limitations=validated_result.limitations,
                created_at=datetime.utcnow(),
            )
            self.db.add(recommendation)

        self.db.commit()

        log_audit_event(
            self.db,
            actor_type="AGENT",
            actor_id="COPILOT_AGENT",
            event_type="RECOMMENDATION_PRODUCED",
            payload={
                "action": validated_result.recommendation.value,
                "confidence": validated_result.confidence,
                "risk_assessment": validated_result.risk_assessment.value,
            },
            investigation_id=investigation.id,
            institution_id=self.institution_id,
        )

        return {
            "investigation_id": investigation.id,
            "alert_id": alert.id,
            "status": investigation.status,
            "summary": investigation.summary,
            "risk_assessment": investigation.risk_assessment,
            "confidence_score": float(investigation.confidence_score or 0.0),
            "recommendation": {
                "id": recommendation.id,
                "action": recommendation.action,
                "rationale": recommendation.rationale,
                "findings": recommendation.findings,
                "missing_information": recommendation.missing_information,
                "applicable_policies": recommendation.applicable_policies,
                "limitations": recommendation.limitations,
            },
        }
