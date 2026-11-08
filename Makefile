MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.SUFFIXES:

.DEFAULT_GOAL := run

.PHONY: run
run:
	uv run python -m scripts.main

.PHONY: install
install:
	uv sync --frozen --extra dev

.PHONY: lint
lint:
	uv run ruff check --fix
	uv run mypy scripts tests

.PHONY: format
format:
	uv run black --color .

.PHONY: pre-commit
pre-commit:
	uv run pre-commit run --verbose --all-files

.PHONY: unit-tests
unit-tests:
	uv run pytest
