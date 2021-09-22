FROM python:3.9-slim

RUN apt update \
  && apt upgrade -y \
  && apt install -y build-essential

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir --upgrade pip \
  && pip install poetry

RUN  poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .

# CMD ["uvicorn", "holowhoslive.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD uvicorn holowhoslive.main:app --host 0.0.0.0 --port $PORT
