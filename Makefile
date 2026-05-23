.PHONY: install test lint format pre-commit generate-data run clean clean-all docker-build docker-run

PYTHON ?= python3
PRE_COMMIT_HOME ?= .cache/pre-commit

ARG ?= $(word 2,$(MAKECMDGOALS))

LIMIT ?= $(ARG)
ifeq ($(LIMIT),)
LIMIT := 100
endif

ROWS ?= $(ARG)
ifeq ($(ROWS),)
ROWS := 100
endif

ARG_TARGETS := run generate-data docker-run
ifneq ($(filter $(ARG_TARGETS),$(MAKECMDGOALS)),)
EXTRA_ARGS := $(filter-out $(ARG_TARGETS),$(MAKECMDGOALS))
ifneq ($(EXTRA_ARGS),)
$(eval $(EXTRA_ARGS):;@:)
endif
endif

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

pre-commit:
	PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) $(PYTHON) -m pre_commit run --all-files

generate-data:
	$(PYTHON) -m fraud_rules_engine.data_generation --output data/sample_transactions.csv --rows $(ROWS)

run:
	$(PYTHON) -m fraud_rules_engine.cli --config config/rules.yaml --input data/sample_transactions.csv --limit $(LIMIT)

clean:
	rm -f data/sample_transactions.csv
	rm -f reports/audit_log.jsonl reports/batch_report.json
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	rm -rf src/*.egg-info

clean-all: clean
	rm -rf .venv

docker-build:
	docker build -t fraud-rules-engine .

docker-run:
	mkdir -p data reports
	docker run --rm \
		-v "$(CURDIR)/data:/app/data:ro" \
		-v "$(CURDIR)/reports:/app/reports" \
		fraud-rules-engine \
		--config config/rules.yaml \
		--input data/sample_transactions.csv \
		--limit $(LIMIT)
