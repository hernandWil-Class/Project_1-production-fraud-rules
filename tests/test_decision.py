from fraud_rules_engine.config import DecisionThresholds
from fraud_rules_engine.decision import decide
from fraud_rules_engine.models import Decision


def test_decision_accept_review_reject_boundaries() -> None:
    thresholds = DecisionThresholds(review_threshold=40, reject_threshold=80)

    assert decide(39, thresholds) == Decision.ACCEPT
    assert decide(40, thresholds) == Decision.REVIEW
    assert decide(79, thresholds) == Decision.REVIEW
    assert decide(80, thresholds) == Decision.REJECT
