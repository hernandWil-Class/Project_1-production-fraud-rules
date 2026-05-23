from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from fraud_rules_engine.models import Decision, EngineResult


class BatchMonitoringReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_version: str
    transactions_scored: int = Field(ge=0)
    decision_counts: dict[Decision, int]
    average_risk_score: float
    top_fired_rules: dict[str, int]


def build_batch_monitoring_report(results: list[EngineResult]) -> BatchMonitoringReport:
    """Summarize decision distribution and rule fire rates for a scored batch."""

    if not results:
        return BatchMonitoringReport(
            policy_version="unknown",
            transactions_scored=0,
            decision_counts={decision: 0 for decision in Decision},
            average_risk_score=0.0,
            top_fired_rules={},
        )

    policy_versions = {result.policy_version for result in results}
    if len(policy_versions) != 1:
        raise ValueError("batch monitoring report expects one policy version per batch")

    decision_counts = Counter(result.decision for result in results)
    rule_counts = Counter(rule_name for result in results for rule_name in result.risk_flags)
    average_score = sum(result.total_risk_score for result in results) / len(results)

    return BatchMonitoringReport(
        policy_version=results[0].policy_version,
        transactions_scored=len(results),
        decision_counts={decision: decision_counts.get(decision, 0) for decision in Decision},
        average_risk_score=round(average_score, 2),
        top_fired_rules=dict(rule_counts.most_common(10)),
    )


def write_batch_monitoring_report(report: BatchMonitoringReport, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report.model_dump(mode="json"), file, indent=2)
