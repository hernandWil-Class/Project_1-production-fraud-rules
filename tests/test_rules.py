from fraud_rules_engine.config import RuleConfig
from fraud_rules_engine.models import ReasonCode, Transaction
from fraud_rules_engine.rules.amount_rules import HighOrderAmountRule, NewCustomerHighAmountRule
from fraud_rules_engine.rules.device_rules import HighDeviceNewCustomerHighAmountRule


def base_transaction(**overrides: object) -> Transaction:
    data = {
        "transaction_id": "txn_test",
        "customer_id": "cust_test",
        "merchant_id": "merch_test",
        "order_amount": 100.0,
        "merchant_category": "fashion",
        "merchant_risk_score": 0.20,
        "customer_tenure_days": 180,
        "number_previous_orders": 6,
        "previous_failed_payments": 0,
        "device_id": "dev_test",
        "device_risk_score": 0.10,
        "email_domain": "gmail.com",
        "email_domain_risk": 0.10,
        "billing_shipping_distance_km": 8.0,
        "payment_method": "card",
        "country": "DE",
        "hour_of_day": 13,
    }
    data.update(overrides)
    return Transaction.model_validate(data)


def test_high_order_amount_rule_fires_above_threshold() -> None:
    rule = HighOrderAmountRule(
        RuleConfig(weight=25, params={"amount_threshold": 500}),
    )

    result = rule.evaluate(base_transaction(order_amount=750))

    assert result.fired is True
    assert result.score == 25
    assert result.reason_code == ReasonCode.HIGH_ORDER_AMOUNT


def test_new_customer_high_amount_requires_both_conditions() -> None:
    rule = NewCustomerHighAmountRule(
        RuleConfig(weight=30, params={"max_tenure_days": 30, "amount_threshold": 300}),
    )

    result = rule.evaluate(base_transaction(customer_tenure_days=10, order_amount=350))
    non_result = rule.evaluate(base_transaction(customer_tenure_days=10, order_amount=100))

    assert result.fired is True
    assert non_result.fired is False


def test_combination_rule_requires_all_conditions() -> None:
    rule = HighDeviceNewCustomerHighAmountRule(
        RuleConfig(
            weight=35,
            params={
                "device_risk_threshold": 0.75,
                "max_tenure_days": 14,
                "amount_threshold": 400,
            },
        )
    )

    result = rule.evaluate(
        base_transaction(device_risk_score=0.90, customer_tenure_days=5, order_amount=600)
    )
    partial_result = rule.evaluate(
        base_transaction(device_risk_score=0.90, customer_tenure_days=40, order_amount=600)
    )

    assert result.fired is True
    assert partial_result.fired is False
