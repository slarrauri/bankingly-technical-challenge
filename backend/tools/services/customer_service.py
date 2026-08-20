from typing import Optional
from sqlalchemy.orm import Session
from backend.domain.models import Customer, CustomerKYC
from backend.tools.schemas import CustomerProfileOutput


def get_customer_profile_service(
    db: Session, customer_id: str, institution_id: str = "BANK-RIO-SUR"
) -> Optional[CustomerProfileOutput]:
    """Retrieve full customer profile and KYC record with tenant isolation."""
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id, Customer.institution_id == institution_id)
        .first()
    )
    if not customer:
        return None

    kyc = customer.kyc_profile

    return CustomerProfileOutput(
        customer_id=customer.id,
        institution_id=customer.institution_id,
        name=customer.name,
        customer_type=customer.customer_type,
        country=customer.country,
        created_at=customer.created_at.strftime("%Y-%m-%d") if customer.created_at else "",
        occupation=kyc.occupation if kyc else "Unknown",
        declared_monthly_income=float(kyc.declared_monthly_income) if kyc else 0.0,
        declared_source_of_funds=kyc.declared_source_of_funds if kyc else "Unknown",
        risk_level=kyc.risk_level if kyc else "MEDIUM",
        kyc_status=kyc.kyc_status if kyc else "INCOMPLETE",
        kyc_notes=kyc.notes if kyc else None,
        kyc_verified_at=kyc.verified_at.strftime("%Y-%m-%d") if kyc and kyc.verified_at else "",
    )
