from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

from fraud_rules_engine.models import Transaction

MERCHANT_CATEGORIES = ["electronics", "fashion", "home", "groceries", "luxury", "gift_cards"]
PAYMENT_METHODS = ["card", "paypal", "direct_debit"]
COUNTRIES = ["DE", "NL", "FR", "AT", "ES", "IT"]
EMAIL_DOMAINS = {
    "gmail.com": 0.10,
    "outlook.com": 0.15,
    "icloud.com": 0.12,
    "proton.me": 0.52,
    "temp-mail.org": 0.91,
    "maildrop.cc": 0.95,
}


def generate_transactions(rows: int, seed: int = 42) -> list[Transaction]:
    rng = random.Random(seed)
    transactions: list[Transaction] = []

    for index in range(1, rows + 1):
        merchant_category = rng.choice(MERCHANT_CATEGORIES)
        email_domain, email_risk = rng.choice(list(EMAIL_DOMAINS.items()))
        risky_pattern = rng.random() < 0.18

        order_amount = rng.uniform(40, 280)
        customer_tenure_days = rng.randint(45, 900)
        device_risk_score = rng.uniform(0.02, 0.55)
        merchant_risk_score = rng.uniform(0.05, 0.65)
        previous_failed_payments = rng.choice([0, 0, 0, 1, 1, 2])
        distance = rng.uniform(1, 180)
        hour = rng.randint(7, 23)

        if risky_pattern:
            order_amount = rng.uniform(350, 1200)
            customer_tenure_days = rng.randint(0, 35)
            device_risk_score = rng.uniform(0.65, 0.99)
            merchant_risk_score = rng.uniform(0.60, 0.98)
            previous_failed_payments = rng.randint(1, 4)
            distance = rng.uniform(150, 750)
            hour = rng.choice([0, 1, 2, 3, 4, 5, 23])

        transactions.append(
            Transaction(
                transaction_id=f"txn_{index:05d}",
                customer_id=f"cust_{rng.randint(1000, 9999)}",
                merchant_id=f"merch_{rng.randint(100, 999)}",
                order_amount=round(order_amount, 2),
                merchant_category=merchant_category,
                merchant_risk_score=round(merchant_risk_score, 2),
                customer_tenure_days=customer_tenure_days,
                number_previous_orders=rng.randint(0, 40),
                previous_failed_payments=previous_failed_payments,
                device_id=f"dev_{rng.randint(10000, 99999)}",
                device_risk_score=round(device_risk_score, 2),
                email_domain=email_domain,
                email_domain_risk=email_risk,
                billing_shipping_distance_km=round(distance, 1),
                payment_method=rng.choice(PAYMENT_METHODS),
                country=rng.choice(COUNTRIES),
                hour_of_day=hour,
            )
        )

    return transactions


def write_transactions_csv(transactions: list[Transaction], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(Transaction.model_fields))
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction.model_dump())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic BNPL transaction data.")
    parser.add_argument("--output", type=Path, default=Path("data/sample_transactions.csv"))
    parser.add_argument("--rows", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    transactions = generate_transactions(rows=args.rows, seed=args.seed)
    write_transactions_csv(transactions, args.output)
    print(f"Wrote {len(transactions)} transactions to {args.output}")


if __name__ == "__main__":
    main()

