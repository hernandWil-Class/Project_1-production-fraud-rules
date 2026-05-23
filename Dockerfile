FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY config ./config
COPY data ./data
COPY src ./src

RUN pip install --no-cache-dir .

CMD ["fraud-rules-engine", "--config", "config/rules.yaml", "--input", "data/sample_transactions.csv"]

