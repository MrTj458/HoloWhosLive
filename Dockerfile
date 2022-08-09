FROM node:16-alpine as build-client

WORKDIR /app
COPY ./client/package*.json ./
RUN npm install
COPY ./client/ .
RUN npm run build

FROM python:3.9-slim as build-server

RUN apt update \
  && apt upgrade -y \
  && apt install -y build-essential

WORKDIR /app

COPY ./server/pyproject.toml ./server/poetry.lock /app/

RUN pip install --no-cache-dir --upgrade pip \
  && pip install poetry

RUN  poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY ./server .

COPY --from=build-client /app/dist/ ./app/

CMD uvicorn holowhoslive.main:app --host 0.0.0.0 --port $PORT
