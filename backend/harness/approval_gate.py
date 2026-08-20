from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from backend.domain.models import (
    Investigation,
    Recommendation,
    Approval,
    AMLAlert,
    InvestigationStatus,
    AlertStatus,
    RecommendedAction,
    ApprovalDecision,
)
from backend.harness.state_machine import validate_investigation_transition


class ApprovalGateError(Exception):
    pass


class UnapprovedExecutionError(ApprovalGateError):
    """Raised when an attempt is made to execute an action without a valid Approval record (INV-002)."""
    pass


class UnauthorizedAnalystError(ApprovalGateError):
    """Raised when an analyst attempts to approve an alert outside their scope/institution (INV-003)."""
    pass


class DuplicateExecutionError(ApprovalGateError):
    """Raised when an already executed recommendation is re-executed (INV-004)."""
    pass


def register_analyst_decision(
    db: Session,
    investigation_id: str,
    analyst_id: str,
    decision: str,  # APPROVED / REJECTED / OVERRIDDEN
    notes: Optional[str] = None,
    institution_id: str = "BANK-RIO-SUR",
) -> Approval:
    """
    Records a human compliance analyst's decision on a recommendation.
    Advances investigation status to APPROVED or REJECTED.
    """
    investigation = (
        db.query(Investigation)
        .filter(Investigation.id == investigation_id, Investigation.institution_id == institution_id)
        .first()
    )
    if not investigation:
        raise ApprovalGateError(f"Investigation '{investigation_id}' not found.")

    if not analyst_id or not analyst_id.startswith("ANA-"):
        raise UnauthorizedAnalystError(f"Analyst '{analyst_id}' is not authorized to approve compliance alerts (INV-003).")

    recommendation = investigation.recommendation
    if not recommendation:
        raise ApprovalGateError(f"No recommendation found for investigation '{investigation_id}'.")

    # Target state
    target_status = (
        InvestigationStatus.APPROVED.value
        if decision == ApprovalDecision.APPROVED.value
        else InvestigationStatus.REJECTED.value
    )
    validate_investigation_transition(investigation.status, target_status)

    # Check if approval already exists
    existing_approval = db.query(Approval).filter(Approval.recommendation_id == recommendation.id).first()
    if existing_approval:
        existing_approval.decision = decision
        existing_approval.notes = notes
        existing_approval.analyst_id = analyst_id
        approval = existing_approval
    else:
        approval = Approval(
            id=f"APP-{investigation.id}",
            recommendation_id=recommendation.id,
            analyst_id=analyst_id,
            decision=decision,
            notes=notes,
            created_at=datetime.utcnow(),
        )
        db.add(approval)

    investigation.status = target_status
    db.commit()
    db.refresh(approval)
    return approval


def execute_approved_action(
    db: Session,
    investigation_id: str,
    institution_id: str = "BANK-RIO-SUR",
) -> dict:
    """
    Executes the approved action on the alert.
    CRITICAL (INV-002): Must verify a valid Approval record exists.
    CRITICAL (INV-004): Must verify it hasn't already been executed.
    """
    investigation = (
        db.query(Investigation)
        .filter(Investigation.id == investigation_id, Investigation.institution_id == institution_id)
        .first()
    )
    if not investigation:
        raise ApprovalGateError(f"Investigation '{investigation_id}' not found.")

    # Invariant 4: Check if already executed
    if investigation.status == InvestigationStatus.EXECUTED.value:
        raise DuplicateExecutionError(
            f"Investigation '{investigation_id}' has already been executed. Duplicate execution is prohibited (INV-004)."
        )

    # Invariant 2: Check for valid human approval
    recommendation = investigation.recommendation
    if not recommendation:
        raise UnapprovedExecutionError("No recommendation exists to execute (INV-002).")

    approval = recommendation.approval
    if not approval or investigation.status not in [InvestigationStatus.APPROVED.value, InvestigationStatus.REJECTED.value]:
        raise UnapprovedExecutionError(
            f"Execution denied: No valid human approval found for investigation '{investigation_id}'. "
            f"Status is '{investigation.status}' (INV-002)."
        )

    # Validate state transition to EXECUTED
    validate_investigation_transition(investigation.status, InvestigationStatus.EXECUTED.value)

    # Mutate alert status based on approved recommendation
    alert = investigation.alert
    action = recommendation.action

    if approval.decision == ApprovalDecision.APPROVED.value:
        if action == RecommendedAction.CLOSE_ALERT.value:
            alert.status = AlertStatus.CLOSED_FALSE_POSITIVE.value
        elif action == RecommendedAction.ESCALATE_ALERT.value:
            alert.status = AlertStatus.ESCALATED_SAR.value
        elif action == RecommendedAction.REQUEST_INFORMATION.value:
            alert.status = AlertStatus.INFO_REQUESTED.value
    else:
        # If rejected, maintain under review or info requested
        alert.status = AlertStatus.UNDER_INVESTIGATION.value

    investigation.status = InvestigationStatus.EXECUTED.value
    investigation.completed_at = datetime.utcnow()
    db.commit()

    return {
        "investigation_id": investigation.id,
        "alert_id": alert.id,
        "status": investigation.status,
        "resulting_alert_status": alert.status,
        "executed_action": action,
        "executed_at": investigation.completed_at.isoformat(),
    }
