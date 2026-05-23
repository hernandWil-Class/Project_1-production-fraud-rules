import pytest

from fraud_rules_engine.config import DecisionThresholds, EngineConfig, RuleConfig
from fraud_rules_engine.engine import FraudRulesEngine, UnknownRuleError
from fraud_rules_engine.models import Decision, ReasonCode, Transaction


def risky_transaction() -> Transaction:
    return Transaction(
        transaction_id="txn_risky",
        customer_id="cust_new",
        merchant_id="merch_risky",
        order_amount=900,
        merchant_category="electronics",
        merchant_risk_score=0.90,
        customer_tenure_days=5,
        number_previous_orders=0,
        previous_failed_payments=3,
        device_id="dev_risky",
        device_risk_score=0.95,
        email_domain="temp-mail.org",
        email_domain_risk=0.91,
        billing_shipping_distance_km=500,
        payment_method="card",
        country="DE",
        hour_of_day=2,
    )


def test_engine_aggregates_rule_results_and_decides_reject() -> None:
    config = EngineConfig(
        policy_version="test-policy-v1",
        decision_thresholds=DecisionThresholds(review_threshold=40, reject_threshold=80),
        rules={
            "high_order_amount": RuleConfig(weight=25, params={"amount_threshold": 500}),
            "high_device_risk_score": RuleConfig(weight=25, params={"risk_threshold": 0.80}),
            "new_customer_high_amount": RuleConfig(
                weight=30,
                params={"max_tenure_days": 30, "amount_threshold": 300},
            ),
        },
    )
    engine = FraudRulesEngine(config)

    result = engine.evaluate(risky_transaction())

    assert result.total_risk_score == 80
    assert result.policy_version == "test-policy-v1"
    assert result.decision == Decision.REJECT
    assert result.risk_flags == [
        "high_order_amount",
        "high_device_risk_score",
        "new_customer_high_amount",
    ]
    assert result.reason_codes == [
        ReasonCode.HIGH_ORDER_AMOUNT,
        ReasonCode.HIGH_DEVICE_RISK_SCORE,
        ReasonCode.NEW_CUSTOMER_HIGH_AMOUNT,
    ]


def test_disabled_rules_are_not_evaluated() -> None:
    config = EngineConfig(
        policy_version="test-policy-v1",
        decision_thresholds=DecisionThresholds(review_threshold=40, reject_threshold=80),
        rules={
            "high_order_amount": RuleConfig(
                enabled=False,
                weight=25,
                params={"amount_threshold": 500},
            ),
        },
    )
    engine = FraudRulesEngine(config)

    result = engine.evaluate(risky_transaction())

    assert result.total_risk_score == 0
    assert result.decision == Decision.ACCEPT
    assert result.rule_results == []


def test_unknown_enabled_rule_fails_fast() -> None:
    config = EngineConfig(
        policy_version="test-policy-v1",
        decision_thresholds=DecisionThresholds(review_threshold=40, reject_threshold=80),
        rules={
            "rule_that_does_not_exist": RuleConfig(enabled=True, weight=10),
        },
    )

    with pytest.raises(UnknownRuleError):
        FraudRulesEngine(config)
