FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libffi-dev libssl-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
WORKDIR /app

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8002
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
