from fraud_rules_engine.models import Decision, EngineResult, ReasonCode, RuleResult
from fraud_rules_engine.reporting import build_batch_monitoring_report


def engine_result(
    transaction_id: str,
    decision: Decision,
    total_risk_score: int,
    risk_flags: list[str],
) -> EngineResult:
    return EngineResult(
        transaction_id=transaction_id,
        policy_version="test-policy-v1",
        decision=decision,
        total_risk_score=total_risk_score,
        risk_flags=risk_flags,
        reason_codes=[ReasonCode(flag.upper()) for flag in risk_flags],
        rule_results=[
            RuleResult(
                rule_name=flag,
                fired=True,
                score=10,
                reason_code=ReasonCode(flag.upper()),
                explanation="test",
            )
            for flag in risk_flags
        ],
    )


def test_batch_monitoring_report_summarizes_decisions_and_rules() -> None:
    report = build_batch_monitoring_report(
        [
            engine_result("txn_1", Decision.ACCEPT, 10, []),
            engine_result("txn_2", Decision.REVIEW, 45, ["high_order_amount"]),
            engine_result(
                "txn_3",
                Decision.REJECT,
                95,
                ["high_order_amount", "high_device_risk_score"],
            ),
        ]
    )

    assert report.policy_version == "test-policy-v1"
    assert report.transactions_scored == 3
    assert report.decision_counts[Decision.ACCEPT] == 1
    assert report.decision_counts[Decision.REVIEW] == 1
    assert report.decision_counts[Decision.REJECT] == 1
    assert report.average_risk_score == 50.0
    assert report.top_fired_rules == {
        "high_order_amount": 2,
        "high_device_risk_score": 1,
    }
