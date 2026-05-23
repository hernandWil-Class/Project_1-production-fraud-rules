from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from fraud_rules_engine.models import EngineResult, Transaction


def build_audit_record(transaction: Transaction, result: EngineResult) -> dict[str, object]:
    """Create a compact audit record suitable for JSONL storage."""

    return {
        "scored_at": datetime.now(UTC).isoformat(),
        "transaction_id": result.transaction_id,
        "customer_id": transaction.customer_id,
        "merchant_id": transaction.merchant_id,
        "policy_version": result.policy_version,
        "decision": result.decision.value,
        "total_risk_score": result.total_risk_score,
        "risk_flags": result.risk_flags,
        "reason_codes": result.reason_codes,
    }


def write_audit_log(
    transactions: list[Transaction],
    results: list[EngineResult],
    output_path: Path,
) -> None:
    """Write one decision audit record per scored transaction."""

    if len(transactions) != len(results):
        raise ValueError("transactions and results must have the same length")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for transaction, result in zip(transactions, results, strict=True):
            file.write(json.dumps(build_audit_record(transaction, result)) + "\n")

