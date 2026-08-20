from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from backend.data.database import get_db
from backend.harness.approval_gate import (
    register_analyst_decision,
    execute_approved_action,
    UnapprovedExecutionError,
    UnauthorizedAnalystError,
    DuplicateExecutionError,
    ApprovalGateError,
)
from backend.harness.audit_service import log_audit_event

router = APIRouter(prefix="/investigations", tags=["Decisions & Execution"])


class SubmitDecisionRequest(BaseModel):
    decision: str = Field(..., description="APPROVED, REJECTED, or OVERRIDDEN")
    notes: Optional[str] = Field(None, description="Compliance justification notes")


@router.post("/{investigation_id}/decide")
def decide_recommendation(
    investigation_id: str,
    req: SubmitDecisionRequest,
    x_institution_id: str = Header("BANK-RIO-SUR", alias="X-Institution-Id"),
    x_analyst_id: str = Header("ANA-0091", alias="X-Analyst-Id"),
    db: Session = Depends(get_db),
):
    """Record a compliance analyst's decision on an investigation recommendation."""
    try:
        approval = register_analyst_decision(
            db=db,
            investigation_id=investigation_id,
            analyst_id=x_analyst_id,
            decision=req.decision,
            notes=req.notes,
            institution_id=x_institution_id,
        )

        log_audit_event(
            db,
            actor_type="ANALYST",
            actor_id=x_analyst_id,
            event_type="APPROVAL_GRANTED" if req.decision == "APPROVED" else "APPROVAL_REJECTED",
            payload={"decision": req.decision, "notes": req.notes},
            investigation_id=investigation_id,
            institution_id=x_institution_id,
        )

        return {
            "data": {
                "investigation_id": investigation_id,
                "status": approval.decision,
                "approval": {
                    "id": approval.id,
                    "analyst_id": approval.analyst_id,
                    "decision": approval.decision,
                    "notes": approval.notes,
                    "created_at": approval.created_at.isoformat(),
                },
            }
        }
    except UnauthorizedAnalystError as err:
        raise HTTPException(status_code=403, detail=str(err))
    except ApprovalGateError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.post("/{investigation_id}/execute")
def execute_decision(
    investigation_id: str,
    x_institution_id: str = Header("BANK-RIO-SUR", alias="X-Institution-Id"),
    x_analyst_id: str = Header("ANA-0091", alias="X-Analyst-Id"),
    db: Session = Depends(get_db),
):
    """
    Execute the approved action on the AML alert.
    CRITICAL (INV-002): Strictly rejects if no prior human Approval record exists.
    CRITICAL (INV-004): Rejects if already executed.
    """
    try:
        result = execute_approved_action(
            db=db,
            investigation_id=investigation_id,
            institution_id=x_institution_id,
        )

        log_audit_event(
            db,
            actor_type="SYSTEM_HARNESS",
            actor_id=x_analyst_id,
            event_type="ACTION_EXECUTED",
            payload=result,
            investigation_id=investigation_id,
            institution_id=x_institution_id,
        )

        return {"data": result}
    except UnapprovedExecutionError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except DuplicateExecutionError as err:
        raise HTTPException(status_code=409, detail=str(err))
    except ApprovalGateError as err:
        raise HTTPException(status_code=400, detail=str(err))
