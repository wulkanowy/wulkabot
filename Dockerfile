FROM python:3.10-alpine

ENV POETRY_VERSION=1.2.0
ENV PYTHONUNBUFFERED=1

RUN apk add gcc libressl-dev libffi-dev python3-dev musl-dev
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . .
CMD [ "poetry", "run", "python", "-m", "wulkabot" ]
