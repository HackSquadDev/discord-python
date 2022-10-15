FROM python:3.10-slim-buster

WORKDIR /code
COPY pyproject.toml poetry.lock /code/

RUN pip install poetry

COPY . /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi