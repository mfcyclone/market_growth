FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Poetry
ENV POETRY_VERSION=1.8.3 POETRY_VIRTUALENVS_CREATE=false
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .
RUN poetry install --no-interaction --no-ansi

ENV PORT=8080
CMD ["poetry", "run", "serve"]
