from fraud_rules_engine.config import DecisionThresholds
from fraud_rules_engine.models import Decision


def decide(total_risk_score: int, thresholds: DecisionThresholds) -> Decision:
    if total_risk_score >= thresholds.reject_threshold:
        return Decision.REJECT
    if total_risk_score >= thresholds.review_threshold:
        return Decision.REVIEW
    return Decision.ACCEPT

