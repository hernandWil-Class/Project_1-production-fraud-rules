from fraud_rules_engine.models import ReasonCode, RuleResult, Transaction
from fraud_rules_engine.rules.base import FraudRule


class HighOrderAmountRule(FraudRule):
    rule_name = "high_order_amount"
    reason_code = ReasonCode.HIGH_ORDER_AMOUNT

    def evaluate(self, transaction: Transaction) -> RuleResult:
        threshold = float(self.param("amount_threshold", 500))
        fired = transaction.order_amount >= threshold
        return self.result(
            fired=fired,
            explanation=(
                f"Order amount {transaction.order_amount:.2f} is "
                f"{'above' if fired else 'below'} threshold {threshold:.2f}."
            ),
        )


class NewCustomerHighAmountRule(FraudRule):
    rule_name = "new_customer_high_amount"
    reason_code = ReasonCode.NEW_CUSTOMER_HIGH_AMOUNT

    def evaluate(self, transaction: Transaction) -> RuleResult:
        max_tenure_days = int(self.param("max_tenure_days", 30))
        amount_threshold = float(self.param("amount_threshold", 300))
        fired = (
            transaction.customer_tenure_days <= max_tenure_days
            and transaction.order_amount >= amount_threshold
        )
        return self.result(
            fired=fired,
            explanation=(
                f"Customer tenure is {transaction.customer_tenure_days} days and order "
                f"amount is {transaction.order_amount:.2f}; configured limits are "
                f"{max_tenure_days} days and {amount_threshold:.2f}."
            ),
        )


class LargeBillingShippingDistanceRule(FraudRule):
    rule_name = "large_billing_shipping_distance"
    reason_code = ReasonCode.LARGE_BILLING_SHIPPING_DISTANCE

    def evaluate(self, transaction: Transaction) -> RuleResult:
        threshold = float(self.param("distance_threshold_km", 250))
        fired = transaction.billing_shipping_distance_km >= threshold
        return self.result(
            fired=fired,
            explanation=(
                f"Billing-shipping distance is {transaction.billing_shipping_distance_km:.1f} km; "
                f"threshold is {threshold:.1f} km."
            ),
        )


class SuspiciousTransactionTimeRule(FraudRule):
    rule_name = "suspicious_transaction_time"
    reason_code = ReasonCode.SUSPICIOUS_TRANSACTION_TIME

    def evaluate(self, transaction: Transaction) -> RuleResult:
        start_hour = int(self.param("start_hour", 0))
        end_hour = int(self.param("end_hour", 5))
        fired = start_hour <= transaction.hour_of_day <= end_hour
        return self.result(
            fired=fired,
            explanation=(
                f"Transaction hour is {transaction.hour_of_day}; suspicious window is "
                f"{start_hour}:00-{end_hour}:59."
            ),
        )
