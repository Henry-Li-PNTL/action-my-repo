# Build Stage
FROM python:3.11-slim as builder


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock

# RUN pip install poetry
# RUN poetry install
COPY . .

ENTRYPOINT ["pwd"]
