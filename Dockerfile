# Build Stage
FROM python:3.11-slim


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock

COPY . /
RUN pip install poetry
RUN cd / && poetry install

CMD ["python", "/src/main.py", "--help"]
