MAKEFLAGS = --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: run install lint

.DEFAULT_GOAL := run

run:
	poetry run python ./Scripts/main.py

install:
	poetry install --no-root

lint:
	poetry run black --color ./Scripts
	poetry run ruff check --fix ./Scripts
	poetry run mypy ./Scripts
	poetry run autoflake --remove-all-unused-imports --remove-unused-variables --recursive ./Scripts
