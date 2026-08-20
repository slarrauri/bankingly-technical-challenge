from typing import Callable, Dict, Any, List
from sqlalchemy.orm import Session

from backend.tools.services.alert_service import get_alert_service
from backend.tools.services.customer_service import get_customer_profile_service
from backend.tools.services.transaction_service import get_transactions_service
from backend.tools.services.summary_service import get_transaction_summary_service
from backend.tools.services.policy_service import (
    get_aml_policies_service,
    get_previous_alerts_service,
)

# Registry of AUTHORIZED read-only tools exposed to the agent.
# CRITICAL (INV-001): There is NO execute_action, close_alert, or fund_freeze tool in this registry.
AUTHORIZED_READ_TOOLS: Dict[str, Dict[str, Any]] = {
    "get_alert": {
        "description": "Fetch details of the target AML alert.",
        "function": get_alert_service,
    },
    "get_customer_profile": {
        "description": "Retrieve customer demographic and KYC profile.",
        "function": get_customer_profile_service,
    },
    "get_transactions": {
        "description": "Fetch customer transaction history with optional date range and bounds.",
        "function": get_transactions_service,
    },
    "get_transaction_summary": {
        "description": "Deterministically calculate volume surge %, historical averages, and counterparty metrics.",
        "function": get_transaction_summary_service,
    },
    "get_previous_alerts": {
        "description": "Fetch historical AML alerts and resolutions for the customer.",
        "function": get_previous_alerts_service,
    },
    "get_aml_policies": {
        "description": "Retrieve institutional AML policies and rules.",
        "function": get_aml_policies_service,
    },
}


def is_tool_authorized(tool_name: str) -> bool:
    """Verifies whether a requested tool is in the authorized read-only registry."""
    return tool_name in AUTHORIZED_READ_TOOLS
