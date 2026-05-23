from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Any

from fraud_rules_engine.audit import write_audit_log
from fraud_rules_engine.config import load_config
from fraud_rules_engine.engine import FraudRulesEngine
from fraud_rules_engine.models import Transaction
from fraud_rules_engine.reporting import (
    build_batch_monitoring_report,
    write_batch_monitoring_report,
)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def coerce_csv_row(row: dict[str, str]) -> dict[str, Any]:
    numeric_fields = {
        "order_amount": float,
        "merchant_risk_score": float,
        "customer_tenure_days": int,
        "number_previous_orders": int,
        "previous_failed_payments": int,
        "device_risk_score": float,
        "email_domain_risk": float,
        "billing_shipping_distance_km": float,
        "hour_of_day": int,
    }
    coerced: dict[str, Any] = dict(row)
    for field_name, field_type in numeric_fields.items():
        coerced[field_name] = field_type(row[field_name])
    return coerced


def read_transactions(input_path: Path) -> list[Transaction]:
    with input_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [Transaction.model_validate(coerce_csv_row(row)) for row in reader]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the BNPL fraud rules engine.")
    parser.add_argument("--config", type=Path, default=Path("config/rules.yaml"))
    parser.add_argument("--input", type=Path, default=Path("data/sample_transactions.csv"))
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--audit-output", type=Path, default=Path("reports/audit_log.jsonl"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/batch_report.json"))
    args = parser.parse_args()

    configure_logging()
    config = load_config(args.config)
    engine = FraudRulesEngine(config)

    transactions = read_transactions(args.input)[: args.limit]
    results = [engine.evaluate(transaction) for transaction in transactions]
    monitoring_report = build_batch_monitoring_report(results)

    write_audit_log(transactions, results, args.audit_output)
    write_batch_monitoring_report(monitoring_report, args.report_output)

    print(json.dumps([result.model_dump(mode="json") for result in results], indent=2))
    print(f"Wrote audit log to {args.audit_output}")
    print(f"Wrote batch monitoring report to {args.report_output}")


if __name__ == "__main__":
    main()
