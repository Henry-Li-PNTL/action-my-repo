TEST_ENV=./tests/test.env
LINT_DIR=./src
TEST_CASE_FOLDER=./tests
TEST_ARGUMENT=
ARGS=--help

.PHONY: install lint format check-coding-style check-static-type check tests

install:
	poetry install

lint:  ## Run linting
	poetry run isort $(LINT_DIR) $(TEST_CASE_FOLDER)
	poetry run black $(LINT_DIR) $(TEST_CASE_FOLDER)
	poetry run flake8 --config=.flake8 $(LINT_DIR) --tee --format=pylint --output-file=./.report/flake8.xml

format:
	poetry run isort --settings-path pyproject.toml $(LINT_DIR)
	poetry run black --config pyproject.toml $(LINT_DIR)

check-coding-style:
	poetry run flake8 --config .flake8 $(LINT_DIR)

check-static-type:
	poetry run mypy --config pyproject.toml --install-types --non-interactive $(LINT_DIR)

check:
	make format
	make check-coding-style
	make check-static-type
	make tests

tests:  ## Run tests
	GITHUB_ACCESS_TOKEN="test" poetry run pytest -v  $(TEST_CASE_FOLDER)/unit --capture no

cli-test-command:  ## Run tests
	GITHUB_ACCESS_TOKEN="test" poetry run python src/main.py $(ARGS)

cli-local-test-command:  ## Run tests
	GITHUB_ACCESS_TOKEN=${GITHUB_ACCESS_TOKEN_LOCALDEV} poetry run python src/main.py $(ARGS)
