MAKEFLAGS = --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: run install lint pre-commi

.DEFAULT_GOAL := run

run:
	poetry run python -m scripts.main

install:
	poetry install --no-root

lint:
	poetry run black --color ./scripts
	poetry run autoflake --remove-all-unused-imports --remove-unused-variables --recursive ./scripts
	poetry run ruff check --fix ./scripts
	poetry run mypy -p scripts
	poetry run pyupgrade --py311-plus ./scripts/main.py

pre-commit:
	poetry run pre-commit run --verbose --all-files
