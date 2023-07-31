# Build Stage
FROM python:3.11-slim


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock

# RUN pip install poetry
# RUN poetry install
COPY . .

CMD ["ls", "/"]
