# Interview Questions Based On The Junior Learning Path

Use these questions after completing `junior_learning_path.md`. They follow the same learning order and are meant to help you explain the project out loud.

## Configuration

1. What is stored in `config/rules.yaml`?
2. Why are rule thresholds stored in config instead of hard-coded inside Python files?
3. What does `enabled: true` or `enabled: false` do for a rule?
4. What is the difference between a rule parameter and a rule weight?
5. Why should `reject_threshold` be greater than `review_threshold`?

## Data Models

6. What is the purpose of the `Transaction` model?
7. What does `Field(ge=0)` mean?
8. What does `Field(ge=0, le=1)` mean?
9. Why does the project use `ConfigDict(extra="forbid")`?
10. What is the difference between `Decision` and `ReasonCode`?
11. Why is `ReasonCode` stricter than using a plain string?
12. What is the difference between `RuleResult` and `EngineResult`?

## Rules

13. What does one rule class do?
14. What input does a rule receive?
15. What output does a rule return?
16. Where does a rule get its threshold values from?
17. Where does a rule get its score from?
18. Why does `HighOrderAmountRule` not hard-code its score?
19. What does the base `FraudRule.result()` helper do?
20. What does it mean when a rule has `fired=True`?

## Decision Logic

21. What is the difference between a rule score and the final risk score?
22. How does the `decide()` function choose between `accept`, `review`, and `reject`?

## Engine

23. What is `RULE_REGISTRY` used for?
24. What happens if a rule is enabled in config but missing from `RULE_REGISTRY`?

## Audit And Reporting

25. Why does the project write an audit log?
26. What is the difference between `reports/audit_log.jsonl` and `reports/batch_report.json`?
27. What is the difference between JSON and JSONL?
28. Why should every decision include a policy version?

## Docker And Makefile

29. What problem does Docker solve for this project?
30. What does `make docker-build` do?
31. What does `make docker-run` do?
32. Why does `make docker-run` mount the local `data/` directory into the container?
33. Why does `make docker-run` mount the local `reports/` directory into the container?
34. When should you rebuild the Docker image?
35. What is the difference between running `make run 10` and `make docker-run 10`?

## Tests

36. What kinds of behavior are tested in `tests/test_rules.py`?
37. What kinds of behavior are tested in `tests/test_engine.py`?
38. Why is it useful to have a `base_transaction(**overrides)` helper in tests?
39. How would you test that a rule does not fire?
40. How would you test that an invalid reason code is rejected?
