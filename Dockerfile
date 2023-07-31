# Build Stage
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH "${PYTHONPATH}:/app"

ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock

RUN pip install poetry
RUN poetry install
COPY . .

ENTRYPOINT ["ls"]
