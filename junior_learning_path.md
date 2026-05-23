# Junior Learning Path: Fraud Rules Engine

## What This File Is For

In any production learning project, `junior_learning_path.md` is the beginner-friendly study guide.

It is not meant to sell the project like a README. It is meant to teach someone how to understand the project slowly, file by file, concept by concept.

For every project, this file should answer:

- Where should a beginner start?
- Which files should they read first?
- What does each file do?
- What concept should they learn from each file?
- What tiny exercise should they do before moving on?
- How do the files connect into one working system?
- What should they be able to explain at the end?

Think of it as a guided tour for a junior data scientist, junior ML engineer, or future version of yourself who opens the repo months later and needs a gentle path back into the system.

This document is a baby-steps guide for a junior data scientist who wants to understand this project slowly and correctly.

Do not try to understand everything at once. Follow the steps in order. After each step, pause and explain what you learned in your own words.

## Goal Of This Guide

By the end, you should understand:

- What problem this project solves.
- What each folder and file is responsible for.
- How one transaction becomes a fraud decision.
- How rules are configured, executed, tested, audited, and monitored.
- How Docker runs the project in a repeatable container environment.
- How pre-commit, Ruff, and pytest protect changes before they are pushed to GitHub.
- Where you can safely make your first changes.

## Mental Model First

This project answers one question:

> Given one BNPL transaction, should we accept it, send it to review, or reject it?

The system does this by:

1. Reading a transaction.
2. Validating the transaction fields.
3. Loading fraud rule settings from YAML.
4. Running each enabled rule.
5. Adding up the risk scores from fired rules.
6. Applying decision thresholds.
7. Returning a transparent decision with reason codes.
8. Writing audit and monitoring outputs.

## Step 0: Run The Project Before Reading Code

Before reading files, run the project.

```bash
make install
make test
make lint
make pre-commit
make generate-data
make run
```

If your local Python environment is messy, or you want to practice the container workflow,
you can also run the project with Docker:

```bash
make docker-build
make docker-run
```

This uses the same input data and writes the same report files, but the Python package runs
inside a container instead of directly on your machine.

What to observe:

- The tests should pass.
- Ruff and pre-commit should pass.
- The CLI should print transaction decisions.
- The project should create files under `reports/`.
- The Docker run should produce the same kind of decisions as the local run.

Mini task:

- Open `reports/batch_report.json`.
- Write down how many transactions were accepted, reviewed, and rejected.

## Step 1: Start With The README

Open:

```text
README.md
```

Understand:

- The business problem.
- Why a BNPL company might use fraud rules.
- What the visual overview image is trying to summarize.
- What the architecture diagram says.
- How to run the project.

Do not worry about the code yet.

Mini task:

- Explain the project in three sentences as if talking to a Product Manager.

## Step 2: Look At The Data

Open:

```text
data/sample_transactions.csv
```

Understand:

- Each row is one transaction.
- Each column is a feature used by fraud rules.
- Some columns describe the customer.
- Some columns describe the merchant.
- Some columns describe the device, email, payment, and timing.

Important columns:

- `order_amount`
- `merchant_risk_score`
- `customer_tenure_days`
- `previous_failed_payments`
- `device_risk_score`
- `email_domain_risk`
- `billing_shipping_distance_km`
- `hour_of_day`

Mini task:

- Pick one risky-looking transaction.
- Guess whether it should be accepted, reviewed, or rejected before running the engine.

## Step 3: Read The Rule Configuration

Open:

```text
config/rules.yaml
```

Understand:

- `policy_version` names the fraud policy being used.
- `review_threshold` is the minimum score for manual review.
- `reject_threshold` is the minimum score for rejection.
- Each rule has:
  - `enabled`
  - `weight`
  - `params`

Example:

```yaml
high_order_amount:
  enabled: true
  weight: 25
  params:
    amount_threshold: 500
```

This means:

> If the order amount is at least 500, add 25 risk points.

Mini task:

- Change the `high_order_amount` threshold from `500` to `300`.
- Run `make run`.
- Observe how the decisions change.
- Change it back afterward.

## Step 4: Understand The Data Models

Open:

```text
src/fraud_rules_engine/models.py
```

Understand these classes:

- `Decision`
- `Transaction`
- `RuleResult`
- `EngineResult`

Plain-English meaning:

- `Transaction` is the input.
- `RuleResult` is the output of one rule.
- `EngineResult` is the final output of the whole engine.
- `Decision` is one of `accept`, `review`, or `reject`.

Why this matters:

- Data models make the system predictable.
- Pydantic validates bad inputs early.
- `extra="forbid"` means unexpected fields fail instead of being ignored.

Mini task:

- Add a fake extra column to one CSV row.
- Run the CLI.
- Observe that validation protects the system.

## Step 5: Understand Config Loading

Open:

```text
src/fraud_rules_engine/config.py
```

Understand:

- YAML is loaded from disk.
- Pydantic validates the config.
- `reject_threshold` must be greater than `review_threshold`.

Why this matters:

- Fraud policy mistakes can cause real business harm.
- Bad config should fail before production scoring starts.

Mini task:

- Set `reject_threshold` lower than `review_threshold`.
- Run `make run`.
- Observe the validation error.
- Change it back afterward.

## Step 6: Understand One Simple Rule

Open:

```text
src/fraud_rules_engine/rules/amount_rules.py
```

Start with:

```text
HighOrderAmountRule
```

Understand:

- The rule reads a threshold from config.
- It checks whether the transaction amount is high.
- It returns a `RuleResult`.
- If the rule fires, it contributes its configured score.

Mini task:

- Find the explanation text returned by the rule.
- Run the CLI and find that explanation in the output.

## Step 7: Understand The Base Rule Pattern

Open:

```text
src/fraud_rules_engine/rules/base.py
```

Understand:

- Every fraud rule inherits from `FraudRule`.
- Every rule must implement `evaluate()`.
- The `result()` helper builds a consistent `RuleResult`.

Why this matters:

- All rules follow the same contract.
- This makes rules easier to test and easier to extend.

Mini task:

- Explain why it is useful that every rule returns the same shape of output.

## Step 8: Read The Other Rules

Open these files:

```text
src/fraud_rules_engine/rules/customer_rules.py
src/fraud_rules_engine/rules/device_rules.py
src/fraud_rules_engine/rules/merchant_rules.py
```

Understand:

- Customer rules look at customer history and email risk.
- Device rules look at device risk and combinations of risk signals.
- Merchant rules look at merchant risk and merchant category.

Mini task:

- Pick your favorite rule.
- Explain what business risk it is trying to detect.

## Step 9: Understand The Decision Policy

Open:

```text
src/fraud_rules_engine/decision.py
```

Understand:

- Scores below review threshold are accepted.
- Scores at or above review threshold go to review.
- Scores at or above reject threshold are rejected.

Mini task:

- What happens if a transaction has score `39`?
- What happens if it has score `40`?
- What happens if it has score `80`?

## Step 10: Understand The Engine

Open:

```text
src/fraud_rules_engine/engine.py
```

Understand the flow:

1. Build enabled rule objects from config.
2. Run every rule on the transaction.
3. Keep rules that fired.
4. Sum the risk score.
5. Apply the decision policy.
6. Return an `EngineResult`.

Important idea:

```text
RULE_REGISTRY
```

This maps rule names from YAML to Python rule classes.

Mini task:

- Disable one rule in `config/rules.yaml`.
- Run `make run`.
- Confirm the rule no longer appears in scoring.

## Step 11: Understand The CLI

Open:

```text
src/fraud_rules_engine/cli.py
```

Understand:

- It reads CSV rows.
- It converts numeric fields from strings into numbers.
- It creates `Transaction` objects.
- It loads config.
- It runs the engine.
- It prints results.
- It writes audit and monitoring outputs.

Mini task:

- Run:

```bash
python -m fraud_rules_engine.cli --limit 2
```

- Confirm only two transactions are scored.

## Step 12: Understand Audit Logging

Open:

```text
src/fraud_rules_engine/audit.py
```

Understand:

- Audit logs are compact records of decisions.
- They include policy version, transaction ID, customer ID, merchant ID, score, decision, flags, and reason codes.
- They are written as JSONL: one JSON object per line.

Why this matters:

- Fraud and credit decisions often need to be explained later.
- Audit records help with disputes, debugging, compliance, and monitoring.

Mini task:

- Run `make run`.
- Open `reports/audit_log.jsonl`.
- Pick one line and explain what happened.

## Step 13: Understand Batch Monitoring

Open:

```text
src/fraud_rules_engine/reporting.py
```

Understand:

- The report counts accept/review/reject decisions.
- It calculates average risk score.
- It shows the most common fired rules.

Why this matters:

- Risk teams need to know whether a policy is too strict or too weak.
- A sudden jump in reject rate could indicate a bad policy change or a real fraud attack.

Mini task:

- Run `make run`.
- Open `reports/batch_report.json`.
- Identify the most common fired rule.

## Step 14: Read The Tests

Open:

```text
tests/test_rules.py
tests/test_decision.py
tests/test_engine.py
tests/test_reporting.py
```

Understand:

- `test_rules.py` checks individual rules.
- `test_decision.py` checks decision thresholds.
- `test_engine.py` checks full engine behavior.
- `test_reporting.py` checks monitoring summaries.

Why this matters:

- Tests protect business logic.
- In fraud systems, small rule mistakes can affect many customers.

Mini task:

- Break one rule intentionally.
- Run `make test`.
- Observe which test fails.
- Undo your change.

## Step 15: Generate New Synthetic Data

Open:

```text
src/fraud_rules_engine/data_generation.py
```

Understand:

- The project generates fake but realistic transactions.
- Some transactions are normal.
- Some transactions follow risky patterns.
- A random seed makes the data reproducible.

Mini task:

```bash
make generate-data 50
make run 50
```

Observe:

- Did the decision distribution change?
- Which rules fired most often?

## Step 16: Clean Generated Files

As you run the project, it creates data, reports, caches, and local metadata.

Use:

```bash
make clean
```

Understand:

- This removes generated data and reports.
- This removes Python, test, and lint caches.
- This does not remove your virtual environment.

If you want to remove the virtual environment too, use:

```bash
make clean-all
```

Mini task:

- Run `make generate-data 10`.
- Run `make run 10`.
- Confirm `data/sample_transactions.csv` and files under `reports/` exist.
- Run `make clean`.
- Confirm those generated files were removed.

## Step 17: Understand Supporting Files And Tooling

Open:

```text
pyproject.toml
Makefile
Dockerfile
.gitignore
.pre-commit-config.yaml
requirements.txt
README_visual.png
```

Understand:

- `pyproject.toml` defines the Python package and tooling.
- `Makefile` gives common project commands.
- `Dockerfile` runs the project in a container.
- `.gitignore` avoids committing generated or local files.
- `.pre-commit-config.yaml` defines checks that run before commits.
- `requirements.txt` lists runtime and development dependencies for simple installation.
- `README_visual.png` is the visual overview shown in the README.

Focus especially on these Makefile targets:

```text
install
test
lint
format
pre-commit
docker-build
docker-run
```

Plain-English meaning:

- `make docker-build` creates a Docker image named `fraud-rules-engine`.
- `make docker-run` starts a temporary container from that image.
- `make docker-run 10` scores only 10 transactions, similar to `make run 10`.
- The Docker run mounts local `data/` into `/app/data` as read-only.
- The Docker run mounts local `reports/` into `/app/reports` so outputs remain visible
  after the container exits.
- `make pre-commit` runs all configured pre-commit hooks over all files.
- `make lint` runs Ruff lint checks.
- `make format` applies Ruff formatting and safe lint fixes.

Why this matters:

- Docker gives the project a repeatable runtime.
- A teammate can run the engine without manually creating a virtual environment.
- The container separates the application runtime from your laptop setup.
- Mounting `reports/` keeps generated audit and monitoring files outside the container.
- Pre-commit catches formatting, linting, YAML, merge-conflict, whitespace, and file-size
  issues before they are committed.
- The large-file hook allows the README visual image but still blocks files larger than
  3 MB by default.

Common Docker workflow:

```bash
make generate-data
make docker-build
make docker-run 10
```

Common local quality workflow:

```bash
make test
make lint
make pre-commit
```

Install the Git hook once:

```bash
PRE_COMMIT_HOME=.cache/pre-commit .venv/bin/python -m pre_commit install
```

After this, `git commit` automatically runs the hooks.

When to rebuild:

- Rebuild after changing Python source files.
- Rebuild after changing package metadata in `pyproject.toml`.
- You do not need to rebuild just because `reports/` changed.

Mini task:

- Run `make docker-build`.
- Run `make docker-run 5`.
- Open `reports/batch_report.json`.
- Explain why the report exists on your machine even though the engine ran in a container.

Mini task:

- Find the command behind `make test`.
- Find the command behind `make lint`.
- Find the command behind `make pre-commit`.
- Find the command behind `make run`.
- Find the command behind `make clean`.
- Find the command behind `make docker-run`.

## Your First Real Extension

Implement one new rule:

```text
ForeignCountryHighAmountRule
```

Business idea:

> If the transaction country is not DE and the order amount is high, add risk points.

Suggested config:

```yaml
foreign_country_high_amount:
  enabled: true
  weight: 20
  params:
    home_country: DE
    amount_threshold: 400
```

Files to edit:

1. Add the rule class in one of the files under `src/fraud_rules_engine/rules/`.
2. Export it from `src/fraud_rules_engine/rules/__init__.py`.
3. Register it in `RULE_REGISTRY` inside `src/fraud_rules_engine/engine.py`.
4. Add it to `config/rules.yaml`.
5. Add tests in `tests/test_rules.py`.
6. Run `make test`.

## Checklist For Understanding The Project

You are ready to move on when you can answer these:

- What is a transaction?
- What is a rule?
- What is a reason code?
- What is a policy version?
- What is the difference between a rule score and the final score?
- What is the difference between `review` and `reject`?
- Why do we use config instead of hard-coding thresholds?
- Why do we write audit logs?
- What does the batch monitoring report tell us?
- What does Docker add to this project?
- Why does `make docker-run` mount `data/` and `reports/`?
- What does pre-commit check before a commit?
- Why is `README_visual.png` allowed even though large files are usually risky?
- Where would you add a new rule?
- Where would you add a new test?
- How would this later become an API?

## Final Advice

Move slowly. The value of this project is not memorizing the files. The value is understanding how small, testable pieces combine into a system that a Risk team, Product Manager, Staff Engineer, and Data Scientist could all reason about.
