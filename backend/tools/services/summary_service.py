from datetime import datetime, timedelta
from typing import List, Set
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.domain.models import Transaction, Customer, CustomerKYC
from backend.tools.schemas import TransactionSummaryOutput


def get_transaction_summary_service(
    db: Session,
    customer_id: str,
    period_days: int = 30,
    institution_id: str = "BANK-RIO-SUR",
) -> TransactionSummaryOutput:
    """
    Deterministically computes transactional metrics:
    - Volume inflow/outflow in the target window.
    - Historical baseline averages.
    - Percentage volume change (e.g. +342%).
    - Inflow to declared monthly income multiplier.
    - Identification of new or concentrated counterparties.
    """
    # Fetch customer and KYC
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id, Customer.institution_id == institution_id)
        .first()
    )
    declared_income = (
        float(customer.kyc_profile.declared_monthly_income)
        if customer and customer.kyc_profile
        else 4500.0
    )

    # Fetch all transactions for customer
    all_txs = (
        db.query(Transaction)
        .filter(
            Transaction.customer_id == customer_id,
            Transaction.institution_id == institution_id,
        )
        .order_by(Transaction.timestamp.asc())
        .all()
    )

    if not all_txs:
        return TransactionSummaryOutput(
            customer_id=customer_id,
            institution_id=institution_id,
            period_days=period_days,
            current_period_inflow=0.0,
            current_period_outflow=0.0,
            current_period_tx_count=0,
            historical_avg_monthly_inflow=0.0,
            historical_avg_monthly_outflow=0.0,
            volume_change_percentage=0.0,
            inflow_to_declared_income_ratio=0.0,
            new_counterparties_detected=[],
            rapid_movement_detected=False,
            summary_text="No transaction history available for customer.",
        )

    max_date = all_txs[-1].timestamp
    cutoff_date = max_date - timedelta(days=period_days)

    recent_txs = [t for t in all_txs if t.timestamp >= cutoff_date]
    historical_txs = [t for t in all_txs if t.timestamp < cutoff_date]

    # Current period metrics
    current_inflow = sum(
        float(t.amount) for t in recent_txs if t.direction in ["CREDIT", "INCOMING"]
    )
    current_outflow = sum(
        float(t.amount) for t in recent_txs if t.direction in ["DEBIT", "OUTGOING"]
    )

    # Historical metrics
    hist_inflow = sum(
        float(t.amount) for t in historical_txs if t.direction in ["CREDIT", "INCOMING"]
    )
    hist_outflow = sum(
        float(t.amount) for t in historical_txs if t.direction in ["DEBIT", "OUTGOING"]
    )

    # Calculate months spanned by historical data
    if historical_txs:
        min_hist_date = historical_txs[0].timestamp
        hist_days = max(1, (cutoff_date - min_hist_date).days)
        hist_months = max(1.0, hist_days / 30.0)
        avg_monthly_hist_inflow = hist_inflow / hist_months
        avg_monthly_hist_outflow = hist_outflow / hist_months
    else:
        avg_monthly_hist_inflow = declared_income
        avg_monthly_hist_outflow = declared_income * 0.8

    # Percentage change
    if avg_monthly_hist_inflow > 0:
        volume_change = (
            (current_inflow - avg_monthly_hist_inflow) / avg_monthly_hist_inflow
        ) * 100.0
    else:
        volume_change = 0.0

    inflow_ratio = (
        current_inflow / declared_income if declared_income > 0 else 0.0
    )

    # New counterparties in recent period
    hist_cps = set(t.counterparty_id for t in historical_txs if t.counterparty_id)
    recent_cps = set(t.counterparty_id for t in recent_txs if t.counterparty_id)
    new_cps = list(recent_cps - hist_cps)

    # Rapid movement heuristic (>70% of high incoming funds dispersed within short window)
    rapid_movement = False
    if current_inflow > 10000 and current_outflow > (current_inflow * 0.7):
        rapid_movement = True

    summary_text = (
        f"In the last {period_days} days, customer received USD {current_inflow:,.2f} "
        f"and transferred USD {current_outflow:,.2f}. Volume changed by {volume_change:+.1f}% "
        f"vs historical baseline ({inflow_ratio:.2f}x declared monthly income of USD {declared_income:,.2f}). "
        f"New counterparties: {', '.join(new_cps) if new_cps else 'None'}."
    )

    return TransactionSummaryOutput(
        customer_id=customer_id,
        institution_id=institution_id,
        period_days=period_days,
        current_period_inflow=round(current_inflow, 2),
        current_period_outflow=round(current_outflow, 2),
        current_period_tx_count=len(recent_txs),
        historical_avg_monthly_inflow=round(avg_monthly_hist_inflow, 2),
        historical_avg_monthly_outflow=round(avg_monthly_hist_outflow, 2),
        volume_change_percentage=round(volume_change, 1),
        inflow_to_declared_income_ratio=round(inflow_ratio, 2),
        new_counterparties_detected=new_cps,
        rapid_movement_detected=rapid_movement,
        summary_text=summary_text,
    )
