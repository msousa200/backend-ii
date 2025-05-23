FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "data_pipeline.api:app", "--host", "0.0.0.0", "--port", "8000"]