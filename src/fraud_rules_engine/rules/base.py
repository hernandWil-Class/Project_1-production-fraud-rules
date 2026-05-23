from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from fraud_rules_engine.config import RuleConfig
from fraud_rules_engine.models import ReasonCode, RuleResult, Transaction


class FraudRule(ABC):
    """Base class for isolated, testable fraud rules."""

    rule_name: str
    reason_code: ReasonCode

    def __init__(self, config: RuleConfig) -> None:
        self.config = config

    @property
    def weight(self) -> int:
        return self.config.weight

    def param(self, name: str, default: Any | None = None) -> Any:
        return self.config.params.get(name, default)

    @abstractmethod
    def evaluate(self, transaction: Transaction) -> RuleResult:
        """Evaluate one transaction and return a complete rule-level explanation."""

    def result(self, fired: bool, explanation: str) -> RuleResult:
        return RuleResult(
            rule_name=self.rule_name,
            fired=fired,
            score=self.weight if fired else 0,
            reason_code=self.reason_code,
            explanation=explanation,
        )
