from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from backend.domain.models import RecommendedAction, RiskLevel


class EvidenceReference(BaseModel):
    source_type: str = Field(..., description="E.g. transaction_summary, customer_kyc, transactions, aml_policies")
    source_id: Optional[str] = Field(None, description="Identifier of the specific record, e.g. TX-0025 or CUST-0042")
    field: Optional[str] = Field(None, description="Specific field cited, e.g. volume_change_percentage")
    value: Optional[str] = Field(None, description="Verifiable value or observation")


class Finding(BaseModel):
    finding: str = Field(..., description="Concise statement of an observed fact or risk indicator")
    evidence: List[EvidenceReference] = Field(default_factory=list, description="Direct citations supporting this finding")


class InvestigationResult(BaseModel):
    investigation_summary: str = Field(..., description="Executive summary of the investigation")
    risk_assessment: RiskLevel = Field(..., description="Assessed risk level: LOW, MEDIUM, HIGH, CRITICAL")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score between 0.0 and 1.0")
    findings: List[Finding] = Field(default_factory=list, description="Structured findings backed by evidence")
    missing_information: List[str] = Field(default_factory=list, description="Gaps, missing documents, or unverified facts")
    applicable_policies: List[str] = Field(default_factory=list, description="Policy IDs triggered, e.g. ['P-001', 'P-003']")
    recommendation: RecommendedAction = Field(..., description="One of: CLOSE_ALERT, ESCALATE_ALERT, REQUEST_INFORMATION")
    rationale: str = Field(..., description="Clear justification for the recommended action")
    limitations: List[str] = Field(default_factory=list, description="Analytical limitations or assumptions made")
