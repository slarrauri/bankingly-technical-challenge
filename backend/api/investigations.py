from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from backend.data.database import get_db
from backend.domain.models import Investigation
from backend.harness.orchestrator import InvestigationOrchestrator

router = APIRouter(prefix="/investigations", tags=["Investigations"])


class StartInvestigationRequest(BaseModel):
    alert_id: str


@router.post("/start")
def start_investigation(
    req: StartInvestigationRequest,
    x_institution_id: str = Header("BANK-RIO-SUR", alias="X-Institution-Id"),
    x_analyst_id: str = Header("ANA-0091", alias="X-Analyst-Id"),
    db: Session = Depends(get_db),
):
    """Trigger an autonomous, bounded Copilot investigation on an AML alert."""
    orchestrator = InvestigationOrchestrator(db, institution_id=x_institution_id)
    try:
        result = orchestrator.run_investigation(alert_id=req.alert_id, analyst_id=x_analyst_id)
        return {"data": result}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/{investigation_id}")
def get_investigation_details(
    investigation_id: str,
    x_institution_id: str = Header("BANK-RIO-SUR", alias="X-Institution-Id"),
    db: Session = Depends(get_db),
):
    """Retrieve full status, findings, and recommendation of an investigation."""
    inv = (
        db.query(Investigation)
        .filter(Investigation.id == investigation_id, Investigation.institution_id == x_institution_id)
        .first()
    )
    if not inv:
        raise HTTPException(status_code=404, detail=f"Investigation '{investigation_id}' not found.")

    rec = inv.recommendation
    rec_data = None
    if rec:
        rec_data = {
            "id": rec.id,
            "action": rec.action,
            "rationale": rec.rationale,
            "findings": rec.findings,
            "missing_information": rec.missing_information,
            "applicable_policies": rec.applicable_policies,
            "limitations": rec.limitations,
        }

    return {
        "data": {
            "id": inv.id,
            "alert_id": inv.alert_id,
            "status": inv.status,
            "summary": inv.summary,
            "risk_assessment": inv.risk_assessment,
            "confidence_score": float(inv.confidence_score or 0.0),
            "recommendation": rec_data,
            "created_at": inv.created_at.isoformat() if inv.created_at else "",
            "completed_at": inv.completed_at.isoformat() if inv.completed_at else None,
        }
    }
