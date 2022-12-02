FROM python:3.10

ENV POETRY_VERSION=1.2.0

RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . .
RUN poetry run python -m wulkabot
