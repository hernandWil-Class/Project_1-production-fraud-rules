# Project Prompt Template

## What This File Is For

In any production learning project, `project_prompt_template.md` is the reusable instruction prompt that defines what kind of project you want an AI coding assistant to build.

It is not part of the application runtime. It is a planning and generation artifact.

For every project, this file should capture:

- Your learning goals.
- Your target career direction.
- The business problem.
- The expected technical stack.
- The desired project structure.
- The production habits you want included.
- The documentation you expect.
- The tests and quality checks you expect.
- The extension tasks you want to implement manually.
- The level of seniority the project should demonstrate.

Think of it as the project brief you would give to a senior mentor before building.

```text
You are my senior Staff Data Scientist / ML Engineer / Data Engineer mentor.

I am a Staff Data Scientist working in fraud/risk in the BNPL/fintech industry.

I want you to help me build one production-style learning project.

Important principles:
- The project should be realistic, not toy-level.
- The code should be simple enough for me to understand fully.
- Prioritize learning, clean architecture, and production habits.
- Do not over-engineer.
- Use realistic business context where possible.
- Make the project suitable for a GitHub portfolio.
- Leave TODOs and extension tasks for me to implement manually.
- Explain trade-offs clearly.
- Include Staff-level production thinking: auditability, monitoring, policy versioning, governance, rollback, and scaling trade-offs.
- Include beginner-friendly learning documentation that explains the project step by step.

Technical requirements:
- Use Python 3.11 or newer.
- Use a clean src/ project structure.
- Include type hints.
- Include pytest tests.
- Include ruff or black.
- Include Pydantic models.
- Include YAML or JSON configuration.
- Include structured logging where relevant.
- Include a Makefile.
- Include pyproject.toml or requirements.txt.
- Include Docker if useful.
- Include synthetic data generation.
- Include sample data.
- Include a CLI.
- Include audit logging.
- Include batch monitoring/reporting.
- Include configuration validation.
- Use clear comments only where they explain important design decisions.

PROJECT-SPECIFIC BRIEF

Project name:
Production Python Fraud Rules Engine

What is BNPL:
BNPL, or “Buy Now, Pay Later,” is a payment option that lets customers purchase something immediately and pay for it over time, usually through short installments. Instead of paying the full amount upfront, the customer may split the cost into several scheduled payments, sometimes with no interest if paid on time. For businesses, BNPL can help increase conversion and average order value, but it also requires careful fraud checks because bad actors may try to abuse deferred payment approvals.

Business problem:
A BNPL company needs a transparent rule-based fraud engine before sending risky orders to ML or manual review.

The engine should evaluate incoming transactions and return:
- risk flags
- rule-level explanations
- final decision: accept, review, or reject
- policy version
- audit record

The goal is not to build a machine learning model yet. The goal is to build a clean, testable, extensible Python rule engine that could later be integrated into a scoring API.

Main learning goal:
Learn clean Python package design, typing, testing, modular business logic, configuration-driven systems, auditability, monitoring, and maintainable rule execution.

Dataset:
Use synthetic BNPL transaction data with realistic features:
- transaction_id
- customer_id
- merchant_id
- order_amount
- merchant_category
- merchant_risk_score
- customer_tenure_days
- number_previous_orders
- previous_failed_payments
- device_id
- device_risk_score
- email_domain
- email_domain_risk
- billing_shipping_distance_km
- payment_method
- country
- hour_of_day

Suggested fraud rules:
- High order amount
- High merchant risk score
- New customer with high order amount
- Multiple previous failed payments
- High device risk score
- Risky email domain
- Large billing-shipping distance
- Suspicious transaction time
- High-risk merchant category
- Combination rule: high device risk + new customer + high amount

Rule engine behavior:
- Each rule should be implemented as a separate, testable unit.
- Each rule should return whether it fired, score contribution, reason code, and explanation.
- The engine should aggregate all rule outputs into a final risk score.
- The final decision should be based on configurable thresholds.
- Unknown enabled rules should fail fast.
- Config and input models should reject unexpected fields.
- Every decision should include a policy_version.

Configuration:
Use YAML config to define:
- policy_version
- score thresholds
- rule parameters
- enabled/disabled rules
- risk score weights

Production-style features:
- Add JSONL audit logging with transaction_id, customer_id, merchant_id, policy_version, decision, score, fired rules, and reason codes.
- Add a batch monitoring report with accept/review/reject counts, average score, and top fired rules.
- Add tests for rules, engine, decision policy, and reporting.
- Add README sections explaining auditability, policy versioning, monitoring, production trade-offs, and scaling.
- Add generated reports to .gitignore.

Project structure:
Create a clean production-style structure, for example:

fraud-rules-engine/
├── README.md
├── junior_learning_path.md
├── learning_notes.md
├── tradeoffs.md
├── interview_questions.md
├── Makefile
├── pyproject.toml
├── Dockerfile
├── .gitignore
├── config/
│   └── rules.yaml
├── data/
│   └── sample_transactions.csv
├── src/
│   └── fraud_rules_engine/
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       ├── decision.py
│       ├── engine.py
│       ├── audit.py
│       ├── reporting.py
│       ├── data_generation.py
│       ├── cli.py
│       └── rules/
│           ├── __init__.py
│           ├── base.py
│           ├── amount_rules.py
│           ├── customer_rules.py
│           ├── device_rules.py
│           └── merchant_rules.py
└── tests/
    ├── test_rules.py
    ├── test_engine.py
    ├── test_decision.py
    └── test_reporting.py

README requirements:
The README should include:
- business problem
- project goal
- setup instructions
- how to generate synthetic data
- how to run the rule engine
- how to run tests
- example input transaction
- example output decision
- example batch monitoring report
- Mermaid architecture diagram
- "What I should learn from this project"
- "Production trade-offs"
- "How this could scale"
- "Interview questions"
- link to junior_learning_path.md

Junior learning document:
Create a separate file called junior_learning_path.md.

It should be written for a junior data scientist and explain, in very simple steps:
- where to start
- which file to open first
- what each file does
- what concept to learn from each file
- tiny exercises after each step
- a recommended reading order
- a checklist of concepts they should understand
- a simple first extension task
- a 5-day study schedule

Personal learning TODOs:
Leave TODOs for me to implement manually:
1. Add 3 new fraud rules.
2. Write tests for those rules.
3. Refactor rule execution to make it more extensible.
4. Add one new decision threshold or policy layer.
5. Add a policy comparison report for two config versions.
6. Improve the README with a deeper real-world business explanation.

After generating the project, also provide:
1. A file-by-file explanation.
2. A recommended order for reading the files.
3. A list of 10 questions I should be able to answer after finishing the project.
4. Three extension tasks that I must implement myself.
5. Suggestions for how to make the project more impressive on GitHub.
6. Suggestions for how this project connects to real companies such as fintechs, marketplaces, mobility companies, e-commerce companies, or scale-ups.
7. A short explanation of why the project is Senior-level or Staff-level.
```

