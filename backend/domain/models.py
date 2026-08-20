import enum
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Column,
    String,
    Text,
    Numeric,
    Integer,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AlertStatus(str, enum.Enum):
    OPEN = "OPEN"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    CLOSED_FALSE_POSITIVE = "CLOSED_FALSE_POSITIVE"
    ESCALATED_SAR = "ESCALATED_SAR"
    INFO_REQUESTED = "INFO_REQUESTED"


class InvestigationStatus(str, enum.Enum):
    CREATED = "CREATED"
    INVESTIGATING = "INVESTIGATING"
    RECOMMENDATION_READY = "RECOMMENDATION_READY"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    INVESTIGATION_FAILED = "INVESTIGATION_FAILED"


class RecommendedAction(str, enum.Enum):
    CLOSE_ALERT = "CLOSE_ALERT"
    ESCALATE_ALERT = "ESCALATE_ALERT"
    REQUEST_INFORMATION = "REQUEST_INFORMATION"


class ApprovalDecision(str, enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    OVERRIDDEN = "OVERRIDDEN"


class CustomerType(str, enum.Enum):
    INDIVIDUAL = "INDIVIDUAL"
    BUSINESS = "BUSINESS"


class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class KYCStatus(str, enum.Enum):
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"
    PENDING = "PENDING"
    INCOMPLETE = "INCOMPLETE"


class TransactionDirection(str, enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    INCOMING = "INCOMING"
    OUTGOING = "OUTGOING"


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(64), primary_key=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    name = Column(String(255), nullable=False)
    customer_type = Column(String(32), nullable=False, default=CustomerType.INDIVIDUAL.value)
    country = Column(String(64), nullable=False, default="Uruguay")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    kyc_profile = relationship("CustomerKYC", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete-orphan")
    alerts = relationship("AMLAlert", back_populates="customer", cascade="all, delete-orphan")


class CustomerKYC(Base):
    __tablename__ = "customer_kyc"

    id = Column(String(64), primary_key=True)
    customer_id = Column(String(64), ForeignKey("customers.id"), nullable=False, unique=True, index=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    occupation = Column(String(255), nullable=False)
    declared_monthly_income = Column(Numeric(14, 2), nullable=False, default=Decimal("0.00"))
    declared_source_of_funds = Column(String(255), nullable=False)
    risk_level = Column(String(32), nullable=False, default=RiskLevel.MEDIUM.value)
    kyc_status = Column(String(32), nullable=False, default=KYCStatus.VERIFIED.value)
    notes = Column(Text, nullable=True)
    verified_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="kyc_profile")


class Counterparty(Base):
    __tablename__ = "counterparties"

    id = Column(String(64), primary_key=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    name = Column(String(255), nullable=False)
    country = Column(String(64), nullable=False)
    industry = Column(String(128), nullable=True)
    risk_level = Column(String(32), nullable=False, default=RiskLevel.LOW.value)

    # Relationships
    transactions = relationship("Transaction", back_populates="counterparty")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(64), primary_key=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    customer_id = Column(String(64), ForeignKey("customers.id"), nullable=False, index=True)
    counterparty_id = Column(String(64), ForeignKey("counterparties.id"), nullable=True, index=True)
    direction = Column(String(16), nullable=False)  # CREDIT / DEBIT / INCOMING / OUTGOING
    amount = Column(Numeric(14, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    channel = Column(String(64), nullable=False, default="BANK_TRANSFER")
    tx_type = Column(String(64), nullable=False, default="WIRE_TRANSFER")
    timestamp = Column(DateTime, nullable=False, index=True)
    description = Column(Text, nullable=False)  # Inert data
    pattern = Column(String(64), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="transactions")
    counterparty = relationship("Counterparty", back_populates="transactions")


class AMLAlert(Base):
    __tablename__ = "aml_alerts"

    id = Column(String(64), primary_key=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    customer_id = Column(String(64), ForeignKey("customers.id"), nullable=False, index=True)
    alert_type = Column(String(128), nullable=False)
    trigger_reason = Column(Text, nullable=False)
    risk_score = Column(Integer, nullable=False, default=50)
    status = Column(String(32), nullable=False, default=AlertStatus.OPEN.value)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="alerts")
    investigation = relationship("Investigation", back_populates="alert", uselist=False, cascade="all, delete-orphan")


class AMLPolicy(Base):
    __tablename__ = "aml_policies"

    id = Column(String(64), primary_key=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    category = Column(String(64), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False, default=RiskLevel.MEDIUM.value)


class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(String(64), primary_key=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    alert_id = Column(String(64), ForeignKey("aml_alerts.id"), nullable=False, unique=True, index=True)
    analyst_id = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default=InvestigationStatus.CREATED.value)
    summary = Column(Text, nullable=True)
    risk_assessment = Column(String(32), nullable=True)
    confidence_score = Column(Numeric(3, 2), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    alert = relationship("AMLAlert", back_populates="investigation")
    recommendation = relationship("Recommendation", back_populates="investigation", uselist=False, cascade="all, delete-orphan")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(64), primary_key=True)
    investigation_id = Column(String(64), ForeignKey("investigations.id"), nullable=False, unique=True, index=True)
    action = Column(String(32), nullable=False)  # RecommendedAction
    rationale = Column(Text, nullable=False)
    findings = Column(JSON, nullable=False, default=list)
    missing_information = Column(JSON, nullable=False, default=list)
    applicable_policies = Column(JSON, nullable=False, default=list)
    limitations = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    investigation = relationship("Investigation", back_populates="recommendation")
    approval = relationship("Approval", back_populates="recommendation", uselist=False, cascade="all, delete-orphan")


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(String(64), primary_key=True)
    recommendation_id = Column(String(64), ForeignKey("recommendations.id"), nullable=False, unique=True, index=True)
    analyst_id = Column(String(64), nullable=False)
    decision = Column(String(32), nullable=False)  # ApprovalDecision
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    recommendation = relationship("Recommendation", back_populates="approval")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(64), primary_key=True)
    institution_id = Column(String(64), nullable=False, index=True, default="BANK-RIO-SUR")
    investigation_id = Column(String(64), nullable=True, index=True)
    actor_type = Column(String(32), nullable=False)  # AGENT, ANALYST, SYSTEM_HARNESS
    actor_id = Column(String(64), nullable=False)
    event_type = Column(String(64), nullable=False)
    payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
