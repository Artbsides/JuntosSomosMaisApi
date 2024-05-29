FROM python:3.12.3-alpine AS debuggable

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-root

COPY /api ./api
COPY /tests ./tests

FROM python:3.12.3-alpine

WORKDIR /app

COPY --from=debuggable /app/pyproject.toml /app/poetry.lock ./
COPY --from=debuggable /app/api ./api

RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-root --no-dev

ENV APP_HOST=${APP_HOST:-0.0.0.0} \
    APP_HOST_PORT=${APP_HOST_PORT:-8000}

CMD gunicorn api.main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker --bind=${APP_HOST}:${APP_HOST_PORT}
