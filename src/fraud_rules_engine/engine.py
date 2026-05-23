from __future__ import annotations

import logging

from fraud_rules_engine.config import EngineConfig
from fraud_rules_engine.decision import decide
from fraud_rules_engine.models import EngineResult, Transaction
from fraud_rules_engine.rules import (
    FraudRule,
    HighDeviceNewCustomerHighAmountRule,
    HighDeviceRiskScoreRule,
    HighMerchantRiskScoreRule,
    HighOrderAmountRule,
    HighRiskMerchantCategoryRule,
    LargeBillingShippingDistanceRule,
    MultiplePreviousFailedPaymentsRule,
    NewCustomerHighAmountRule,
    RiskyEmailDomainRule,
    SuspiciousTransactionTimeRule,
)

logger = logging.getLogger(__name__)


RULE_REGISTRY: dict[str, type[FraudRule]] = {
    HighOrderAmountRule.rule_name: HighOrderAmountRule,
    HighMerchantRiskScoreRule.rule_name: HighMerchantRiskScoreRule,
    NewCustomerHighAmountRule.rule_name: NewCustomerHighAmountRule,
    MultiplePreviousFailedPaymentsRule.rule_name: MultiplePreviousFailedPaymentsRule,
    HighDeviceRiskScoreRule.rule_name: HighDeviceRiskScoreRule,
    RiskyEmailDomainRule.rule_name: RiskyEmailDomainRule,
    LargeBillingShippingDistanceRule.rule_name: LargeBillingShippingDistanceRule,
    SuspiciousTransactionTimeRule.rule_name: SuspiciousTransactionTimeRule,
    HighRiskMerchantCategoryRule.rule_name: HighRiskMerchantCategoryRule,
    HighDeviceNewCustomerHighAmountRule.rule_name: HighDeviceNewCustomerHighAmountRule,
}


class UnknownRuleError(ValueError):
    """Raised when config enables a rule that has no implementation."""


class FraudRulesEngine:
    """Runs enabled rules and aggregates transparent risk outputs."""

    def __init__(self, config: EngineConfig) -> None:
        self.config = config
        self.rules = self._build_rules(config)

    def _build_rules(self, config: EngineConfig) -> list[FraudRule]:
        rules: list[FraudRule] = []
        for rule_name, rule_config in config.rules.items():
            if not rule_config.enabled:
                logger.info("Skipping disabled rule", extra={"rule_name": rule_name})
                continue

            rule_class = RULE_REGISTRY.get(rule_name)
            if rule_class is None:
                raise UnknownRuleError(
                    f"Enabled rule '{rule_name}' is not registered. "
                    "Either implement it in RULE_REGISTRY or disable it in config."
                )

            rules.append(rule_class(rule_config))
        return rules

    def evaluate(self, transaction: Transaction) -> EngineResult:
        rule_results = [rule.evaluate(transaction) for rule in self.rules]
        fired_results = [result for result in rule_results if result.fired]
        total_score = sum(result.score for result in fired_results)
        final_decision = decide(total_score, self.config.decision_thresholds)

        logger.info(
            "Evaluated transaction",
            extra={
                "transaction_id": transaction.transaction_id,
                "total_risk_score": total_score,
                "decision": final_decision.value,
                "fired_rules": [result.rule_name for result in fired_results],
            },
        )

        return EngineResult(
            transaction_id=transaction.transaction_id,
            policy_version=self.config.policy_version,
            decision=final_decision,
            total_risk_score=total_score,
            risk_flags=[result.rule_name for result in fired_results],
            reason_codes=[result.reason_code for result in fired_results],
            rule_results=rule_results,
        )
