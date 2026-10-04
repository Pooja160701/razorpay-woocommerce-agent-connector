FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY docs ./docs
COPY tests ./tests

RUN pip install --no-cache-dir .

ENV WOOCOMMERCE_MODE=mock

CMD ["woocommerce-mcp"]