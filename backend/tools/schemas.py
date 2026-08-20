from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# 1. get_alert
class GetAlertInput(BaseModel):
    alert_id: str = Field(..., description="The ID of the AML alert, e.g. AML-00127")


class AlertDetailsOutput(BaseModel):
    id: str
    institution_id: str
    customer_id: str
    customer_name: Optional[str] = None
    alert_type: str
    trigger_reason: str
    risk_score: int
    status: str
    created_at: str


# 2. get_customer_profile
class GetCustomerProfileInput(BaseModel):
    customer_id: str = Field(..., description="The ID of the customer, e.g. CUST-0042")


class CustomerProfileOutput(BaseModel):
    customer_id: str
    institution_id: str
    name: str
    customer_type: str
    country: str
    created_at: str
    occupation: str
    declared_monthly_income: float
    declared_source_of_funds: str
    risk_level: str
    kyc_status: str
    kyc_notes: Optional[str] = None
    kyc_verified_at: str


# 3. get_transactions
class GetTransactionsInput(BaseModel):
    customer_id: str = Field(..., description="Target customer ID")
    date_from: Optional[str] = Field(None, description="Start date YYYY-MM-DD")
    date_to: Optional[str] = Field(None, description="End date YYYY-MM-DD")
    limit: Optional[int] = Field(50, le=500, description="Max transactions to return (max 500)")


class TransactionItem(BaseModel):
    transaction_id: str
    customer_id: str
    counterparty_id: Optional[str] = None
    counterparty_name: Optional[str] = None
    timestamp: str
    direction: str
    amount: float
    currency: str
    channel: str
    description: str
    pattern: Optional[str] = None


class TransactionsOutput(BaseModel):
    customer_id: str
    total_count: int
    transactions: List[TransactionItem]


# 4. get_transaction_summary (Deterministic calculations)
class GetTransactionSummaryInput(BaseModel):
    customer_id: str = Field(..., description="Target customer ID")
    period_days: Optional[int] = Field(30, description="Days to analyze, default 30")


class TransactionSummaryOutput(BaseModel):
    customer_id: str
    institution_id: str
    period_days: int
    current_period_inflow: float
    current_period_outflow: float
    current_period_tx_count: int
    historical_avg_monthly_inflow: float
    historical_avg_monthly_outflow: float
    volume_change_percentage: float  # e.g. 342.0 for +342%
    inflow_to_declared_income_ratio: float  # e.g. 4.67 (4.67x declared income)
    new_counterparties_detected: List[str]
    rapid_movement_detected: bool
    summary_text: str


# 5. get_previous_alerts
class GetPreviousAlertsInput(BaseModel):
    customer_id: str = Field(..., description="Target customer ID")


class PreviousAlertItem(BaseModel):
    alert_id: str
    alert_type: str
    risk_score: int
    status: str
    trigger_reason: str
    created_at: str


class PreviousAlertsOutput(BaseModel):
    customer_id: str
    total_previous_alerts: int
    alerts: List[PreviousAlertItem]


# 6. get_aml_policies
class GetAMLPoliciesInput(BaseModel):
    category: Optional[str] = Field(None, description="Policy category filter: VELOCITY, RAPID_MOVEMENT, KYC_MISMATCH, GOVERNANCE")


class AMLPolicyItem(BaseModel):
    policy_id: str
    category: str
    title: str
    description: str
    severity: str


class AMLPoliciesOutput(BaseModel):
    policies: List[AMLPolicyItem]
