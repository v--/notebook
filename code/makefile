.PHONY: test lint

test:
	poetry run pytest

lint:
	poetry run ruff check
	poetry run mypy --package notebook
