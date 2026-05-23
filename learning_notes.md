# Learning Notes

Use this file as your own lab notebook while studying the project.

## Concepts To Trace

- A raw CSV row becomes a validated `Transaction`.
- YAML config becomes typed `EngineConfig`.
- Each enabled rule becomes a `FraudRule` instance.
- Each rule returns a `RuleResult`.
- The engine aggregates rule scores and calls the decision policy.
- Each scored transaction carries a `policy_version`.
- The CLI writes audit and monitoring outputs that help explain production behavior.

## TODOs For You

- TODO: Add 3 new fraud rules.
- TODO: Write tests for those rules.
- TODO: Refactor the rule execution logic to make it more extensible.
- TODO: Add one new decision threshold or policy layer.
- TODO: Improve the README with a real business explanation.
- TODO: Compare two policy versions on the same batch and summarize changed decisions.

## Reflection Prompts

- Which rules are customer behavior signals?
- Which rules are merchant risk signals?
- Which rules could unfairly penalize legitimate customers?
- Which features would you want to monitor daily?
- Which outputs would a manual review agent need to see?
- What should happen if a new policy version increases the reject rate by 30 percent?
