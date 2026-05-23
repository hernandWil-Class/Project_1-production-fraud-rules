from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Decision(StrEnum):
    ACCEPT = "accept"
    REVIEW = "review"
    REJECT = "reject"


class ReasonCode(StrEnum):
    HIGH_ORDER_AMOUNT = "HIGH_ORDER_AMOUNT"
    HIGH_MERCHANT_RISK_SCORE = "HIGH_MERCHANT_RISK_SCORE"
    NEW_CUSTOMER_HIGH_AMOUNT = "NEW_CUSTOMER_HIGH_AMOUNT"
    MULTIPLE_PREVIOUS_FAILED_PAYMENTS = "MULTIPLE_PREVIOUS_FAILED_PAYMENTS"
    HIGH_DEVICE_RISK_SCORE = "HIGH_DEVICE_RISK_SCORE"
    RISKY_EMAIL_DOMAIN = "RISKY_EMAIL_DOMAIN"
    LARGE_BILLING_SHIPPING_DISTANCE = "LARGE_BILLING_SHIPPING_DISTANCE"
    SUSPICIOUS_TRANSACTION_TIME = "SUSPICIOUS_TRANSACTION_TIME"
    HIGH_RISK_MERCHANT_CATEGORY = "HIGH_RISK_MERCHANT_CATEGORY"
    HIGH_DEVICE_NEW_CUSTOMER_HIGH_AMOUNT = "HIGH_DEVICE_NEW_CUSTOMER_HIGH_AMOUNT"


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction_id: str
    customer_id: str
    merchant_id: str
    order_amount: float = Field(ge=0)
    merchant_category: str
    merchant_risk_score: float = Field(ge=0, le=1)
    customer_tenure_days: int = Field(ge=0)
    number_previous_orders: int = Field(ge=0)
    previous_failed_payments: int = Field(ge=0)
    device_id: str
    device_risk_score: float = Field(ge=0, le=1)
    email_domain: str
    email_domain_risk: float = Field(ge=0, le=1)
    billing_shipping_distance_km: float = Field(ge=0)
    payment_method: str
    country: str
    hour_of_day: int = Field(ge=0, le=23)


class RuleResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_name: str
    fired: bool
    score: int
    reason_code: ReasonCode
    explanation: str


class EngineResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction_id: str
    policy_version: str
    decision: Decision
    total_risk_score: int
    risk_flags: list[str]
    reason_codes: list[ReasonCode]
    rule_results: list[RuleResult]
