import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.domain.models import AuditEvent


def log_audit_event(
    db: Session,
    actor_type: str,  # AGENT, ANALYST, SYSTEM_HARNESS
    actor_id: str,
    event_type: str,
    payload: Dict[str, Any],
    investigation_id: Optional[str] = None,
    institution_id: str = "BANK-RIO-SUR",
) -> AuditEvent:
    """Records an immutable audit event for regulatory compliance."""
    event = AuditEvent(
        id=f"AUD-{uuid.uuid4().hex[:10].upper()}",
        institution_id=institution_id,
        investigation_id=investigation_id,
        actor_type=actor_type,
        actor_id=actor_id,
        event_type=event_type,
        payload=payload,
        created_at=datetime.utcnow(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
