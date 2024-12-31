FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

COPY . /app/

ENV PYTHONPATH=/app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
