from typing import Optional
from sqlalchemy.orm import Session
from backend.domain.models import AMLAlert, Customer
from backend.tools.schemas import AlertDetailsOutput


def get_alert_service(db: Session, alert_id: str, institution_id: str = "BANK-RIO-SUR") -> Optional[AlertDetailsOutput]:
    """Retrieve an alert with tenant isolation."""
    alert = (
        db.query(AMLAlert)
        .filter(AMLAlert.id == alert_id, AMLAlert.institution_id == institution_id)
        .first()
    )
    if not alert:
        return None

    customer_name = alert.customer.name if alert.customer else None

    return AlertDetailsOutput(
        id=alert.id,
        institution_id=alert.institution_id,
        customer_id=alert.customer_id,
        customer_name=customer_name,
        alert_type=alert.alert_type,
        trigger_reason=alert.trigger_reason,
        risk_score=alert.risk_score,
        status=alert.status,
        created_at=alert.created_at.isoformat() if alert.created_at else "",
    )
