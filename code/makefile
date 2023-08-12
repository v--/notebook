.PHONY: test lint

test:
	poetry run pytest --capture=tee-sys

lint:
	poetry run ruff check src
	poetry run mypy --package src
