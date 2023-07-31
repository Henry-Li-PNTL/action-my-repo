# Build Stage
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ADD pyproject.toml pyproject.toml

RUN pip install poetry
# RUN poetry export --without-hashes --without dev --format=requirements.txt > requirements.txt && \
#     pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final Stage
FROM python:3.11-slim

WORKDIR /app

# COPY --from=builder /app/wheels /wheels
# COPY --from=builder /app/requirements.txt .

COPY . .
# RUN pip install -U pip && pip install --no-cache /wheels/*
RUN pip install -U pip && pip install poetry
RUN poetry install 


ENTRYPOINT ["python", "src/main.py"]
