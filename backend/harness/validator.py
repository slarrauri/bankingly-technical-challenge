import json
from typing import Tuple, Optional
from pydantic import ValidationError
from backend.agent.schemas import InvestigationResult


class SchemaValidationError(Exception):
    pass


def validate_investigation_output(raw_output: str) -> Tuple[bool, Optional[InvestigationResult], Optional[str]]:
    """
    Validates that the LLM output conforms strictly to the InvestigationResult Pydantic schema (INV-009).
    Returns (is_valid, parsed_model, error_message).
    """
    try:
        data = json.loads(raw_output)
        validated = InvestigationResult.model_validate(data)
        return True, validated, None
    except (json.JSONDecodeError, ValidationError) as err:
        return False, None, str(err)
