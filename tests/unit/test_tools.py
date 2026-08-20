import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.domain.models import Base
from backend.data.seed import seed_database
from backend.tools.services.alert_service import get_alert_service
from backend.tools.services.customer_service import get_customer_profile_service
from backend.tools.services.transaction_service import get_transactions_service
from backend.tools.services.summary_service import get_transaction_summary_service
from backend.tools.services.policy_service import (
    get_aml_policies_service,
    get_previous_alerts_service,
)


@pytest.fixture
def seeded_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    seed_database(session)
    yield session
    session.close()


def test_get_alert_service(seeded_db):
    alert = get_alert_service(seeded_db, "AML-001")
    assert alert is not None
    assert alert.id == "AML-001"
    assert alert.customer_id == "CUST-004"
    assert alert.customer_name == "Martín Pereira"
    assert alert.risk_score == 78

    # Tenant isolation check
    alien_alert = get_alert_service(seeded_db, "AML-001", institution_id="BANK-OTHER")
    assert alien_alert is None


def test_get_customer_profile_service(seeded_db):
    profile = get_customer_profile_service(seeded_db, "CUST-004")
    assert profile is not None
    assert profile.name == "Martín Pereira"
    assert profile.occupation == "Software Consultant"
    assert profile.declared_monthly_income == 4500.0
    assert profile.kyc_status == "VERIFIED"


def test_get_transaction_summary_deterministic_math(seeded_db):
    # Test Martín Pereira (CUST-004) across 90 days window
    summary = get_transaction_summary_service(seeded_db, "CUST-004", period_days=90)
    assert summary is not None
    assert summary.customer_id == "CUST-004"
    assert summary.current_period_tx_count > 0
    assert summary.historical_avg_monthly_inflow > 0
    assert summary.summary_text is not None


def test_get_transactions_limit_guard(seeded_db):
    # Test strict limit bounding
    txs = get_transactions_service(seeded_db, "CUST-004", limit=10)
    assert txs.total_count == 10
    assert len(txs.transactions) == 10


def test_get_aml_policies(seeded_db):
    policies = get_aml_policies_service(seeded_db)
    assert len(policies.policies) == 4
    policy_ids = [p.policy_id for p in policies.policies]
    assert "P-001" in policy_ids
    assert "P-004" in policy_ids
