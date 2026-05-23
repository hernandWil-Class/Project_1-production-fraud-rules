from fraud_rules_engine.models import ReasonCode, RuleResult, Transaction
from fraud_rules_engine.rules.base import FraudRule


class MultiplePreviousFailedPaymentsRule(FraudRule):
    rule_name = "multiple_previous_failed_payments"
    reason_code = ReasonCode.MULTIPLE_PREVIOUS_FAILED_PAYMENTS

    def evaluate(self, transaction: Transaction) -> RuleResult:
        threshold = int(self.param("failed_payments_threshold", 2))
        fired = transaction.previous_failed_payments >= threshold
        return self.result(
            fired=fired,
            explanation=(
                f"Previous failed payments is {transaction.previous_failed_payments}; "
                f"threshold is {threshold}."
            ),
        )


class RiskyEmailDomainRule(FraudRule):
    rule_name = "risky_email_domain"
    reason_code = ReasonCode.RISKY_EMAIL_DOMAIN

    def evaluate(self, transaction: Transaction) -> RuleResult:
        threshold = float(self.param("risk_threshold", 0.70))
        fired = transaction.email_domain_risk >= threshold
        return self.result(
            fired=fired,
            explanation=(
                f"Email domain {transaction.email_domain} has risk "
                f"{transaction.email_domain_risk:.2f}; threshold is {threshold:.2f}."
            ),
        )
