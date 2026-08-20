from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Header, HTTPException
from sqlalchemy.orm import Session

from backend.data.database import get_db
from backend.domain.models import AMLAlert
from backend.tools.services.alert_service import get_alert_service
from backend.tools.services.customer_service import get_customer_profile_service
from backend.tools.services.summary_service import get_transaction_summary_service

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("")
def list_alerts(
    status: Optional[str] = Query(None, description="Filter by status"),
    min_risk: Optional[int] = Query(None, description="Filter by minimum risk score"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    x_institution_id: str = Header("BANK-RIO-SUR", alias="X-Institution-Id"),
    db: Session = Depends(get_db),
):
    """List AML alerts with pagination and optional filters."""
    query = db.query(AMLAlert).filter(AMLAlert.institution_id == x_institution_id)

    if status:
        query = query.filter(AMLAlert.status == status)
    if min_risk:
        query = query.filter(AMLAlert.risk_score >= min_risk)

    total = query.count()
    alerts = query.order_by(AMLAlert.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    data = [
        {
            "id": a.id,
            "customer_id": a.customer_id,
            "customer_name": a.customer.name if a.customer else "Unknown",
            "alert_type": a.alert_type,
            "trigger_reason": a.trigger_reason,
            "risk_score": a.risk_score,
            "status": a.status,
            "created_at": a.created_at.isoformat() if a.created_at else "",
        }
        for a in alerts
    ]

    return {
        "data": data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": max(1, (total + limit - 1) // limit),
        },
    }


@router.get("/{alert_id}")
def get_alert_details(
    alert_id: str,
    x_institution_id: str = Header("BANK-RIO-SUR", alias="X-Institution-Id"),
    db: Session = Depends(get_db),
):
    """Retrieve details for a single AML alert."""
    alert = get_alert_service(db, alert_id, x_institution_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")
    return {"data": alert.model_dump()}


@router.get("/{alert_id}/context")
def get_alert_context(
    alert_id: str,
    x_institution_id: str = Header("BANK-RIO-SUR", alias="X-Institution-Id"),
    db: Session = Depends(get_db),
):
    """Retrieve combined alert context including customer KYC, calculated transaction metrics, and any existing investigation from SQLite."""
    alert = get_alert_service(db, alert_id, x_institution_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")

    customer = get_customer_profile_service(db, alert.customer_id, x_institution_id)
    summary = get_transaction_summary_service(db, alert.customer_id, 30, x_institution_id)

    db_alert = (
        db.query(AMLAlert)
        .filter(AMLAlert.id == alert_id, AMLAlert.institution_id == x_institution_id)
        .first()
    )

    inv_data = None
    if db_alert and db_alert.investigation:
        inv = db_alert.investigation
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
        inv_data = {
            "investigation_id": inv.id,
            "alert_id": inv.alert_id,
            "status": inv.status,
            "summary": inv.summary,
            "risk_assessment": inv.risk_assessment,
            "confidence_score": float(inv.confidence_score or 0.0),
            "recommendation": rec_data,
            "created_at": inv.created_at.isoformat() if inv.created_at else "",
            "completed_at": inv.completed_at.isoformat() if inv.completed_at else None,
        }

    return {
        "data": {
            "alert": alert.model_dump(),
            "customer": customer.model_dump() if customer else None,
            "transaction_summary": summary.model_dump() if summary else None,
            "investigation": inv_data,
        }
    }


