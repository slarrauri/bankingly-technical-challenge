import csv
import os
from datetime import datetime
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session

from backend.data.database import engine, get_db_session, init_db
from backend.domain.models import (
    Customer,
    CustomerKYC,
    Counterparty,
    Transaction,
    AMLAlert,
    AMLPolicy,
    AlertStatus,
    CustomerType,
    RiskLevel,
    KYCStatus,
)

INSTITUTION_ID = "BANK-RIO-SUR"

# 18 Counterparties
COUNTERPARTIES = [
    {"id": "CP-001", "name": "TechNova Uruguay S.A.", "country": "Uruguay", "industry": "Software / Technology", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-002", "name": "Estudio Contable Rivera", "country": "Uruguay", "industry": "Accounting Services", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-003", "name": "Constructora del Plata", "country": "Uruguay", "industry": "Construction", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-004", "name": "Clínica Central", "country": "Uruguay", "industry": "Healthcare", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-005", "name": "Mercado Sur S.A.", "country": "Uruguay", "industry": "Food Distribution", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-006", "name": "Legal Partners Uruguay", "country": "Uruguay", "industry": "Legal Services", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-007", "name": "Arquitectura Norte", "country": "Uruguay", "industry": "Architecture", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-008", "name": "GlobalDev Inc.", "country": "United States", "industry": "Software", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-009", "name": "Andes Trading Ltd.", "country": "Uruguay", "industry": "Import / Export", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-010", "name": "Río Plata Imports S.R.L.", "country": "Uruguay", "industry": "Consumer Goods Import", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-011", "name": "Pacific Digital Services Ltd.", "country": "United States", "industry": "Digital Services", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-012", "name": "Nova Consulting Group", "country": "Argentina", "industry": "Consulting", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-013", "name": "Servicios Gastronómicos del Sur", "country": "Uruguay", "industry": "Food Services", "risk_level": RiskLevel.LOW.value},
    {"id": "CP-014", "name": "Capital Bridge LLC", "country": "United States", "industry": "Financial Consulting", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-015", "name": "Inversiones del Sur S.A.", "country": "Uruguay", "industry": "Investments", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-016", "name": "Comercial Horizonte S.A.", "country": "Uruguay", "industry": "Retail", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-017", "name": "Servicios Creativos Varela", "country": "Uruguay", "industry": "Marketing / Design", "risk_level": RiskLevel.MEDIUM.value},
    {"id": "CP-018", "name": "Plataformas Globales S.A.", "country": "Uruguay", "industry": "Digital Payments", "risk_level": RiskLevel.MEDIUM.value},
]

# 12 Customers & KYC Profiles
CUSTOMERS = [
    {
        "id": "CUST-001", "name": "Ana Rodríguez", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2021-03-15",
        "kyc": {"occupation": "Accountant", "income": Decimal("3800.00"), "source": "Professional services", "risk": RiskLevel.LOW.value, "status": KYCStatus.VERIFIED.value, "notes": "Stable professional baseline."}
    },
    {
        "id": "CUST-002", "name": "Diego Fernández", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2020-09-10",
        "kyc": {"occupation": "Civil Engineer", "income": Decimal("5200.00"), "source": "Employment income", "risk": RiskLevel.LOW.value, "status": KYCStatus.VERIFIED.value, "notes": "Predictable salary and household mortgage activity."}
    },
    {
        "id": "CUST-003", "name": "Lucía Martínez", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2022-01-20",
        "kyc": {"occupation": "Physician", "income": Decimal("6500.00"), "source": "Employment + private medical practice", "risk": RiskLevel.LOW.value, "status": KYCStatus.VERIFIED.value, "notes": "Multiple legitimate professional income streams."}
    },
    {
        "id": "CUST-004", "name": "Martín Pereira", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2022-04-18",
        "kyc": {"occupation": "Software Consultant", "income": Decimal("4500.00"), "source": "Professional consulting services", "risk": RiskLevel.MEDIUM.value, "status": KYCStatus.VERIFIED.value, "notes": "Customer indicated that occasional international consulting projects may generate additional income."}
    },
    {
        "id": "CUST-005", "name": "Sofía González", "type": CustomerType.BUSINESS.value, "country": "Uruguay", "created_at": "2019-06-11",
        "kyc": {"occupation": "Import Business Owner", "income": Decimal("8000.00"), "source": "Business income (Consumer goods import)", "risk": RiskLevel.MEDIUM.value, "status": KYCStatus.VERIFIED.value, "notes": "Expected frequent high-value supplier payments to foreign counterparties."}
    },
    {
        "id": "CUST-006", "name": "Carlos Silva", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2023-02-05",
        "kyc": {"occupation": "Architect", "income": Decimal("4000.00"), "source": "Professional services", "risk": RiskLevel.LOW.value, "status": KYCStatus.VERIFIED.value, "notes": "Stable local architectural design client fees."}
    },
    {
        "id": "CUST-007", "name": "Valentina Torres", "type": CustomerType.BUSINESS.value, "country": "Uruguay", "created_at": "2020-11-23",
        "kyc": {"occupation": "Restaurant Owner", "income": Decimal("7500.00"), "source": "Business income (Restaurant and catering)", "risk": RiskLevel.MEDIUM.value, "status": KYCStatus.VERIFIED.value, "notes": "Pronounced seasonal volume peaks during summer and mid-year tourism months."}
    },
    {
        "id": "CUST-008", "name": "Nicolás Cabrera", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2024-01-12",
        "kyc": {"occupation": "Freelance Software Developer", "income": Decimal("3500.00"), "source": "Software development services", "risk": RiskLevel.MEDIUM.value, "status": KYCStatus.VERIFIED.value, "notes": "Variable monthly income received from US-based tech clients."}
    },
    {
        "id": "CUST-009", "name": "Paula Suárez", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2021-08-30",
        "kyc": {"occupation": "Lawyer", "income": Decimal("5800.00"), "source": "Legal services", "risk": RiskLevel.MEDIUM.value, "status": KYCStatus.VERIFIED.value, "notes": "Client retainer payments across multiple regional professional networks."}
    },
    {
        "id": "CUST-010", "name": "Andrés Molina", "type": CustomerType.BUSINESS.value, "country": "Uruguay", "created_at": "2018-05-19",
        "kyc": {"occupation": "Retail Business Owner", "income": Decimal("6000.00"), "source": "Retail business income", "risk": RiskLevel.HIGH.value, "status": KYCStatus.VERIFIED.value, "notes": "High cash-deposit frequency inherent to local retail merchant operations."}
    },
    {
        "id": "CUST-011", "name": "Camila Varela", "type": CustomerType.INDIVIDUAL.value, "country": "Uruguay", "created_at": "2025-06-02",
        "kyc": {"occupation": "Graphic Designer", "income": Decimal("2800.00"), "source": "Professional services", "risk": RiskLevel.MEDIUM.value, "status": KYCStatus.INCOMPLETE.value, "notes": "Pending documentation: Secondary commercial activities and international receipts not verified."}
    },
    {
        "id": "CUST-012", "name": "Rodrigo Sosa", "type": CustomerType.BUSINESS.value, "country": "Uruguay", "created_at": "2017-10-14",
        "kyc": {"occupation": "Business Owner", "income": Decimal("12000.00"), "source": "Business income + investments", "risk": RiskLevel.HIGH.value, "status": KYCStatus.VERIFIED.value, "notes": "Complex corporate holdings and high-value investment transfers."}
    },
]

# 4 AML Institutional Policies
AML_POLICIES = [
    {
        "id": "P-001",
        "category": "VELOCITY",
        "title": "Material Transaction Volume Surge",
        "description": "If transaction volume in a 30-day window exceeds historical monthly baseline by >200%, the analyst must review the underlying source of funds and business justification before closing.",
        "severity": RiskLevel.HIGH.value,
    },
    {
        "id": "P-002",
        "category": "RAPID_MOVEMENT",
        "title": "Rapid Fund Turnover & Structuring",
        "description": "Rapid movement of newly received high-value funds (>USD 10,000) to third-party counterparties within a 5-day window requires enhanced due diligence and escalation review.",
        "severity": RiskLevel.HIGH.value,
    },
    {
        "id": "P-003",
        "category": "KYC_MISMATCH",
        "title": "Economic Profile & Activity Inconsistency",
        "description": "An unexplained mismatch between declared customer KYC income/occupation and observed high-value activity requires formal escalation unless backed by commercial contracts.",
        "severity": RiskLevel.CRITICAL.value,
    },
    {
        "id": "P-004",
        "category": "GOVERNANCE",
        "title": "Mandatory Human Sign-Off for Alert Closure",
        "description": "No AML alert may be closed or escalated automatically without explicit verification and approval by an authorized compliance analyst.",
        "severity": RiskLevel.CRITICAL.value,
    },
]

# 12 Initial AML Alerts
AML_ALERTS = [
    {
        "id": "AML-001", "customer_id": "CUST-004", "alert_type": "UNUSUAL_TRANSACTION_PATTERN",
        "trigger_reason": "Sudden 342% surge in transactional volume; high-value inflows from new counterparty Andes Trading Ltd.",
        "risk_score": 78, "status": AlertStatus.OPEN.value, "created_at": "2026-07-14T09:30:00"
    },
    {
        "id": "AML-002", "customer_id": "CUST-004", "alert_type": "MULTIPLE_INTERNATIONAL_INFLOWS",
        "trigger_reason": "Multiple international transfers received from newly established counterparty Pacific Digital Services.",
        "risk_score": 72, "status": AlertStatus.OPEN.value, "created_at": "2026-07-15T11:00:00"
    },
    {
        "id": "AML-003", "customer_id": "CUST-005", "alert_type": "HIGH_VALUE_INTERNATIONAL_ACTIVITY",
        "trigger_reason": "High-volume international payments to foreign supplier Río Plata Imports S.R.L.",
        "risk_score": 58, "status": AlertStatus.OPEN.value, "created_at": "2026-07-16T14:20:00"
    },
    {
        "id": "AML-004", "customer_id": "CUST-007", "alert_type": "VOLUME_SPIKE_SEASONAL",
        "trigger_reason": "Material increase in card processor receipts during June tourism peak.",
        "risk_score": 52, "status": AlertStatus.OPEN.value, "created_at": "2026-07-16T16:45:00"
    },
    {
        "id": "AML-005", "customer_id": "CUST-008", "alert_type": "VARIABLE_INTERNATIONAL_INCOME",
        "trigger_reason": "Fluctuating cross-border wire transfers from GlobalDev Inc.",
        "risk_score": 45, "status": AlertStatus.OPEN.value, "created_at": "2026-07-17T10:15:00"
    },
    {
        "id": "AML-006", "customer_id": "CUST-010", "alert_type": "HIGH_RISK_CASH_CONCENTRATION",
        "trigger_reason": "High-frequency cash deposits on retail account.",
        "risk_score": 68, "status": AlertStatus.OPEN.value, "created_at": "2026-07-18T08:30:00"
    },
    {
        "id": "AML-007", "customer_id": "CUST-011", "alert_type": "INCOMPLETE_KYC_SURGE",
        "trigger_reason": "Transaction receipts exceeding declared threshold with incomplete KYC documentation on file.",
        "risk_score": 75, "status": AlertStatus.OPEN.value, "created_at": "2026-07-18T13:10:00"
    },
    {
        "id": "AML-008", "customer_id": "CUST-012", "alert_type": "LARGE_INVESTMENT_TRANSFER",
        "trigger_reason": "High-value fund transfer to Inversiones del Sur S.A.",
        "risk_score": 60, "status": AlertStatus.OPEN.value, "created_at": "2026-07-19T09:00:00"
    },
    {
        "id": "AML-009", "customer_id": "CUST-004", "alert_type": "UNVERIFIED_NEW_COUNTERPARTY",
        "trigger_reason": "First-time transfer from Andes Trading Ltd with no commercial documentation on file.",
        "risk_score": 80, "status": AlertStatus.OPEN.value, "created_at": "2026-07-19T15:20:00"
    },
    {
        "id": "AML-010", "customer_id": "CUST-009", "alert_type": "MULTIPLE_CLIENT_RECEIPTS",
        "trigger_reason": "Concentration of payments from multiple regional corporate clients.",
        "risk_score": 42, "status": AlertStatus.OPEN.value, "created_at": "2026-07-20T11:40:00"
    },
    {
        "id": "AML-011", "customer_id": "CUST-012", "alert_type": "UNDOCUMENTED_CONSULTING_RECEIPT",
        "trigger_reason": "Significant funds received from Capital Bridge LLC without documented business relationship.",
        "risk_score": 70, "status": AlertStatus.OPEN.value, "created_at": "2026-07-20T16:00:00"
    },
    {
        "id": "AML-012", "customer_id": "CUST-004", "alert_type": "RAPID_FUNDS_DISPERSAL",
        "trigger_reason": "Immediate outflow of USD 21,000 received from CP-009 to external accounts within 48 hours.",
        "risk_score": 85, "status": AlertStatus.OPEN.value, "created_at": "2026-07-21T10:00:00"
    },
]


def seed_database(db: Session) -> None:
    """Idempotently seed the database with Banco Río Sur dataset."""
    print("[INFO] Initializing database schema...")
    init_db()

    print("[INFO] Cleaning existing data for idempotency...")
    db.query(Transaction).delete()
    db.query(AMLAlert).delete()
    db.query(AMLPolicy).delete()
    db.query(CustomerKYC).delete()
    db.query(Customer).delete()
    db.query(Counterparty).delete()
    db.commit()

    print("[INFO] Seeding 18 Counterparties...")
    for cp_data in COUNTERPARTIES:
        cp = Counterparty(
            id=cp_data["id"],
            institution_id=INSTITUTION_ID,
            name=cp_data["name"],
            country=cp_data["country"],
            industry=cp_data["industry"],
            risk_level=cp_data["risk_level"],
        )
        db.add(cp)
    db.commit()

    print("[INFO] Seeding 12 Customers and KYC Profiles...")
    for c_data in CUSTOMERS:
        created_dt = datetime.strptime(c_data["created_at"], "%Y-%m-%d")
        cust = Customer(
            id=c_data["id"],
            institution_id=INSTITUTION_ID,
            name=c_data["name"],
            customer_type=c_data["type"],
            country=c_data["country"],
            created_at=created_dt,
        )
        db.add(cust)
        db.flush()

        kyc_data = c_data["kyc"]
        kyc = CustomerKYC(
            id=f"KYC-{c_data['id']}",
            customer_id=c_data["id"],
            institution_id=INSTITUTION_ID,
            occupation=kyc_data["occupation"],
            declared_monthly_income=kyc_data["income"],
            declared_source_of_funds=kyc_data["source"],
            risk_level=kyc_data["risk"],
            kyc_status=kyc_data["status"],
            notes=kyc_data["notes"],
            verified_at=created_dt,
        )
        db.add(kyc)
    db.commit()

    print("[INFO] Seeding 4 AML Institutional Policies...")
    for p_data in AML_POLICIES:
        pol = AMLPolicy(
            id=p_data["id"],
            institution_id=INSTITUTION_ID,
            category=p_data["category"],
            title=p_data["title"],
            description=p_data["description"],
            severity=p_data["severity"],
        )
        db.add(pol)
    db.commit()

    print("[INFO] Seeding 12 AML Alerts...")
    for a_data in AML_ALERTS:
        created_dt = datetime.fromisoformat(a_data["created_at"])
        alert = AMLAlert(
            id=a_data["id"],
            institution_id=INSTITUTION_ID,
            customer_id=a_data["customer_id"],
            alert_type=a_data["alert_type"],
            trigger_reason=a_data["trigger_reason"],
            risk_score=a_data["risk_score"],
            status=a_data["status"],
            created_at=created_dt,
        )
        db.add(alert)
    db.commit()

    # Load Transactions from CSV
    csv_candidates = [
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "seed", "aml_simulated_transactions_400.csv"),
        os.path.join(os.path.dirname(__file__), "..", "..", ".sdc", "docs", "PoC", "7. Datos", "outputs", "aml_simulated_transactions_400.csv"),
    ]
    csv_path = None
    for cand in csv_candidates:
        if os.path.exists(cand):
            csv_path = cand
            break

    if csv_path:
        print(f"[INFO] Ingesting simulated transactions from {csv_path}...")
        tx_count = 0
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                tx = Transaction(
                    id=row["transaction_id"],
                    institution_id=row.get("institution_id", INSTITUTION_ID),
                    customer_id=row["customer_id"],
                    counterparty_id=row["counterparty_id"],
                    direction=row["direction"],
                    amount=Decimal(row["amount"]),
                    currency=row.get("currency", "USD"),
                    channel=row.get("channel", "BANK_TRANSFER"),
                    tx_type="WIRE_TRANSFER",
                    timestamp=ts,
                    description=row["description"],
                    pattern=row.get("pattern", "baseline"),
                )
                db.add(tx)
                tx_count += 1
        db.commit()
        print(f"[INFO] Successfully seeded {tx_count} transactions.")
    else:
        print("[WARN] Warning: transactions CSV not found. Skipping transaction bulk load.")

    print("[SUCCESS] Database seeding completed successfully for Banco Rio Sur.")


if __name__ == "__main__":
    with get_db_session() as session:
        seed_database(session)
