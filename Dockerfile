# Build Stage
FROM python:3.11-slim


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock

COPY . .
RUN pip install poetry
RUN poetry export --without-hashes --without dev --format=requirements.txt > requirements.txt && \
    pip install -r requirements.txt

ENTRYPOINT ["python", "/src/main.py"]
