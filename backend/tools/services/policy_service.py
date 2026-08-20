from typing import Optional, List
from sqlalchemy.orm import Session
from backend.domain.models import AMLPolicy, AMLAlert
from backend.tools.schemas import (
    AMLPoliciesOutput,
    AMLPolicyItem,
    PreviousAlertsOutput,
    PreviousAlertItem,
)


def get_aml_policies_service(
    db: Session,
    category: Optional[str] = None,
    institution_id: str = "BANK-RIO-SUR",
) -> AMLPoliciesOutput:
    """Retrieve institutional AML policies, optionally filtered by category."""
    query = db.query(AMLPolicy).filter(AMLPolicy.institution_id == institution_id)
    if category:
        query = query.filter(AMLPolicy.category == category)

    policies = query.all()
    items = [
        AMLPolicyItem(
            policy_id=p.id,
            category=p.category,
            title=p.title,
            description=p.description,
            severity=p.severity,
        )
        for p in policies
    ]
    return AMLPoliciesOutput(policies=items)


def get_previous_alerts_service(
    db: Session,
    customer_id: str,
    exclude_alert_id: Optional[str] = None,
    institution_id: str = "BANK-RIO-SUR",
) -> PreviousAlertsOutput:
    """Retrieve historical alerts for a customer."""
    query = db.query(AMLAlert).filter(
        AMLAlert.customer_id == customer_id,
        AMLAlert.institution_id == institution_id,
    )
    if exclude_alert_id:
        query = query.filter(AMLAlert.id != exclude_alert_id)

    alerts = query.order_by(AMLAlert.created_at.desc()).all()
    items = [
        PreviousAlertItem(
            alert_id=a.id,
            alert_type=a.alert_type,
            risk_score=a.risk_score,
            status=a.status,
            trigger_reason=a.trigger_reason,
            created_at=a.created_at.isoformat() if a.created_at else "",
        )
        for a in alerts
    ]
    return PreviousAlertsOutput(
        customer_id=customer_id,
        total_previous_alerts=len(items),
        alerts=items,
    )
