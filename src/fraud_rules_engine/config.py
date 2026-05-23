from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class DecisionThresholds(BaseModel):
    """Score thresholds used to map a total risk score to a business decision."""

    model_config = ConfigDict(extra="forbid")

    review_threshold: int = Field(ge=0)
    reject_threshold: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_ordering(self) -> DecisionThresholds:
        if self.reject_threshold <= self.review_threshold:
            raise ValueError("reject_threshold must be greater than review_threshold")
        return self


class RuleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    weight: int = Field(default=0, ge=0)
    params: dict[str, Any] = Field(default_factory=dict)


class EngineConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_version: str = Field(min_length=1)
    decision_thresholds: DecisionThresholds
    rules: dict[str, RuleConfig]


def load_config(path: str | Path) -> EngineConfig:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        raw_config = yaml.safe_load(file)
    return EngineConfig.model_validate(raw_config)
