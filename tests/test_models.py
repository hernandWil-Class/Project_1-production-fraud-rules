import pytest
from pydantic import ValidationError

from fraud_rules_engine.models import RuleResult


def test_rule_result_rejects_unknown_reason_code() -> None:
    with pytest.raises(ValidationError):
        RuleResult(
            rule_name="high_order_amount",
            fired=True,
            score=25,
            reason_code="NOT_A_REAL_REASON_CODE",
            explanation="test",
        )
