from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.domain.models import Transaction, Counterparty
from backend.tools.schemas import TransactionsOutput, TransactionItem


def get_transactions_service(
    db: Session,
    customer_id: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 50,
    institution_id: str = "BANK-RIO-SUR",
) -> TransactionsOutput:
    """Retrieve customer transactions with optional date range and strict limit."""
    query = db.query(Transaction).filter(
        Transaction.customer_id == customer_id,
        Transaction.institution_id == institution_id,
    )

    if date_from:
        try:
            dt_from = datetime.fromisoformat(date_from)
            query = query.filter(Transaction.timestamp >= dt_from)
        except ValueError:
            pass

    if date_to:
        try:
            dt_to = datetime.fromisoformat(date_to)
            query = query.filter(Transaction.timestamp <= dt_to)
        except ValueError:
            pass

    safe_limit = min(max(1, limit), 500)
    txs = query.order_by(desc(Transaction.timestamp)).limit(safe_limit).all()

    items = []
    for tx in txs:
        cp_name = tx.counterparty.name if tx.counterparty else None
        items.append(
            TransactionItem(
                transaction_id=tx.id,
                customer_id=tx.customer_id,
                counterparty_id=tx.counterparty_id,
                counterparty_name=cp_name,
                timestamp=tx.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                direction=tx.direction,
                amount=float(tx.amount),
                currency=tx.currency,
                channel=tx.channel,
                description=tx.description,
                pattern=tx.pattern,
            )
        )

    return TransactionsOutput(
        customer_id=customer_id,
        total_count=len(items),
        transactions=items,
    )
