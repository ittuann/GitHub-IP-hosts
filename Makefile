MAKEFLAGS = --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: run install lint format pre-commit unit-tests

.DEFAULT_GOAL := run

run:
	poetry run python -m scripts.main

install:
	poetry install --extras dev

lint:
	poetry run ruff check --fix
	poetry run mypy scripts tests

format:
	poetry run black --color .

pre-commit:
	poetry run pre-commit run --verbose --all-files

unit-tests:
	poetry run pytest
