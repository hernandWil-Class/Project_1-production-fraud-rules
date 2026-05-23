from fraud_rules_engine.models import ReasonCode, RuleResult, Transaction
from fraud_rules_engine.rules.base import FraudRule


class HighDeviceRiskScoreRule(FraudRule):
    rule_name = "high_device_risk_score"
    reason_code = ReasonCode.HIGH_DEVICE_RISK_SCORE

    def evaluate(self, transaction: Transaction) -> RuleResult:
        threshold = float(self.param("risk_threshold", 0.80))
        fired = transaction.device_risk_score >= threshold
        return self.result(
            fired=fired,
            explanation=(
                f"Device risk score is {transaction.device_risk_score:.2f}; "
                f"threshold is {threshold:.2f}."
            ),
        )


class HighDeviceNewCustomerHighAmountRule(FraudRule):
    rule_name = "high_device_new_customer_high_amount"
    reason_code = ReasonCode.HIGH_DEVICE_NEW_CUSTOMER_HIGH_AMOUNT

    def evaluate(self, transaction: Transaction) -> RuleResult:
        device_threshold = float(self.param("device_risk_threshold", 0.75))
        max_tenure_days = int(self.param("max_tenure_days", 14))
        amount_threshold = float(self.param("amount_threshold", 400))
        fired = (
            transaction.device_risk_score >= device_threshold
            and transaction.customer_tenure_days <= max_tenure_days
            and transaction.order_amount >= amount_threshold
        )
        return self.result(
            fired=fired,
            explanation=(
                "Combination check: "
                f"device risk={transaction.device_risk_score:.2f}, "
                f"tenure={transaction.customer_tenure_days} days, "
                f"amount={transaction.order_amount:.2f}."
            ),
        )
