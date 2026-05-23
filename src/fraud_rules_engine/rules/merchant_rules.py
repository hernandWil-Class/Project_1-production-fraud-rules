from fraud_rules_engine.models import ReasonCode, RuleResult, Transaction
from fraud_rules_engine.rules.base import FraudRule


class HighMerchantRiskScoreRule(FraudRule):
    rule_name = "high_merchant_risk_score"
    reason_code = ReasonCode.HIGH_MERCHANT_RISK_SCORE

    def evaluate(self, transaction: Transaction) -> RuleResult:
        threshold = float(self.param("risk_threshold", 0.75))
        fired = transaction.merchant_risk_score >= threshold
        return self.result(
            fired=fired,
            explanation=(
                f"Merchant risk score is {transaction.merchant_risk_score:.2f}; "
                f"threshold is {threshold:.2f}."
            ),
        )


class HighRiskMerchantCategoryRule(FraudRule):
    rule_name = "high_risk_merchant_category"
    reason_code = ReasonCode.HIGH_RISK_MERCHANT_CATEGORY

    def evaluate(self, transaction: Transaction) -> RuleResult:
        categories = set(self.param("categories", []))
        fired = transaction.merchant_category in categories
        return self.result(
            fired=fired,
            explanation=(
                f"Merchant category is {transaction.merchant_category}; "
                f"configured high-risk categories are {sorted(categories)}."
            ),
        )
