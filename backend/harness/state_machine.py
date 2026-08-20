from typing import Set
from backend.domain.models import InvestigationStatus, AlertStatus


class InvalidStateTransitionError(Exception):
    pass


# Valid state transitions for an Investigation
VALID_INVESTIGATION_TRANSITIONS = {
    InvestigationStatus.CREATED: {InvestigationStatus.INVESTIGATING, InvestigationStatus.INVESTIGATION_FAILED},
    InvestigationStatus.INVESTIGATING: {InvestigationStatus.RECOMMENDATION_READY, InvestigationStatus.INVESTIGATION_FAILED},
    InvestigationStatus.RECOMMENDATION_READY: {InvestigationStatus.AWAITING_APPROVAL},
    InvestigationStatus.AWAITING_APPROVAL: {InvestigationStatus.APPROVED, InvestigationStatus.REJECTED},
    InvestigationStatus.APPROVED: {InvestigationStatus.EXECUTED},
    InvestigationStatus.REJECTED: {InvestigationStatus.EXECUTED},
    InvestigationStatus.EXECUTED: set(),  # Terminal state
    InvestigationStatus.INVESTIGATION_FAILED: set(),  # Terminal state
}


def can_transition_investigation(current_status: str, target_status: str) -> bool:
    """
    Validates if transition is legal.
    CRITICAL: RECOMMENDATION_READY -> EXECUTED is strictly ILLEGAL.
    """
    try:
        curr = InvestigationStatus(current_status)
        target = InvestigationStatus(target_status)
    except ValueError:
        return False

    return target in VALID_INVESTIGATION_TRANSITIONS.get(curr, set())


def validate_investigation_transition(current_status: str, target_status: str) -> None:
    """Raises InvalidStateTransitionError if transition is forbidden."""
    if not can_transition_investigation(current_status, target_status):
        raise InvalidStateTransitionError(
            f"Illegal state transition from '{current_status}' to '{target_status}'. "
            f"Direct execution without passing through AWAITING_APPROVAL and APPROVED is strictly prohibited."
        )
