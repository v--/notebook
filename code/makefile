.PHONY: test lint

test:
	poetry run pytest

lint:
	poetry run ruff check src
	poetry run mypy --package src
