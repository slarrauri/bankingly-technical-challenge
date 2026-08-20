import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.domain.models import (
    Base,
    Customer,
    CustomerKYC,
    Counterparty,
    Transaction,
    AMLAlert,
    AMLPolicy,
    AlertStatus,
)
from backend.data.seed import seed_database


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_seed_database_idempotency(in_memory_db):
    # First seed
    seed_database(in_memory_db)

    # Verify counts
    customers = in_memory_db.query(Customer).all()
    assert len(customers) == 12

    counterparties = in_memory_db.query(Counterparty).all()
    assert len(counterparties) == 18

    policies = in_memory_db.query(AMLPolicy).all()
    assert len(policies) == 4

    alerts = in_memory_db.query(AMLAlert).all()
    assert len(alerts) == 12

    transactions = in_memory_db.query(Transaction).all()
    assert len(transactions) == 400

    # Check key customer Martín Pereira (CUST-004)
    cust_004 = in_memory_db.query(Customer).filter_by(id="CUST-004").first()
    assert cust_004 is not None
    assert cust_004.name == "Martín Pereira"
    assert cust_004.kyc_profile.declared_monthly_income == Decimal("4500.00")

    # Second seed (idempotency check)
    seed_database(in_memory_db)
    assert in_memory_db.query(Customer).count() == 12
    assert in_memory_db.query(Transaction).count() == 400
