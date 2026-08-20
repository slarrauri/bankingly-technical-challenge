import csv
import os
from typing import List, Optional
from pydantic import BaseModel


class EvaluationCase(BaseModel):
    evaluation_id: str
    alert_id: str
    category: str
    scenario: str
    expected_recommendation: str
    severity: str
    key_signals: str
    expected_behavior: str


def load_evaluation_dataset() -> List[EvaluationCase]:
    """Load the 25 stratified benchmark cases from CSV."""
    csv_candidates = [
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "evaluation", "aml_evaluation_ground_truth_25.csv"),
        os.path.join(os.path.dirname(__file__), "..", "..", ".sdc", "docs", "PoC", "7. Datos", "outputs", "aml_evaluation_ground_truth_25.csv"),
    ]
    csv_path = None
    for cand in csv_candidates:
        if os.path.exists(cand):
            csv_path = cand
            break

    if not csv_path:
        raise FileNotFoundError("Evaluation ground truth CSV file not found.")

    cases = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append(
                EvaluationCase(
                    evaluation_id=row["evaluation_id"],
                    alert_id=row["alert_id"],
                    category=row["category"],
                    scenario=row["scenario"],
                    expected_recommendation=row["expected_recommendation"],
                    severity=row["severity"],
                    key_signals=row["key_signals"],
                    expected_behavior=row["expected_behavior"],
                )
            )
    return cases
