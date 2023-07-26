# Build Stage
FROM cr-preview.pentium.network/python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ADD Dockerfile Dockerfile

RUN pip install poetry
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final Stage
FROM cr-preview.pentium.network/python:3.11-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install -U pip && pip install --no-cache /wheels/*

COPY . .

ENTRYPOINT ["python", "/src/main.py"]
