.PHONY: test lint

test:
	poetry run pytest notebook

lint:
	poetry run ruff check
	poetry run mypy --package notebook
