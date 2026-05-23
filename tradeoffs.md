# Production Trade-Offs

## Simplicity Versus Extensibility

The engine uses explicit Python classes and a small registry. This is easy to read and test. The trade-off is that adding a new rule requires adding a class and updating the registry.

## Configuration Versus Code

Thresholds and weights live in YAML so policy changes do not require code changes. In a real company, this config would need validation, review, versioning, rollback, and experiment tracking.

## Auditability Versus Storage Cost

The CLI writes compact JSONL audit records so decisions can be inspected later. Production systems need this for disputes, compliance, incident response, and model training labels. The trade-off is that audit data can become large, sensitive, and subject to retention requirements.

## Monitoring Versus Alerting

The batch monitoring report summarizes decision counts and top fired rules. This is enough for a learning project. A real platform would convert these summaries into time-series metrics and alerts when reject rates, review rates, or rule fire rates move unexpectedly.

## Rule Scores Versus Probabilities

The final score is a weighted sum, not a probability of fraud. This is useful for policy ranking but should not be communicated as calibrated model risk.

## Online Versus Batch

The current code is transaction-oriented, which maps well to an API. Batch scoring would need vectorized execution, better IO, and partition-aware monitoring.
