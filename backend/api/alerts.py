from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Header, HTTPException
from sqlalchemy.orm import Session

from backend.data.database import get_db
from backend.domain.models import AMLAlert
from backend.tools.services.alert_service import get_alert_service

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
