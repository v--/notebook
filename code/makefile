.PHONY: test lint

test:
	@poetry run pytest --capture=tee-sys

lint:
	@poetry run pycodestyle .
	@poetry run mypy .

format-figures:
	@poetry run python src/commands/format_matrices.py ../figures/*.tex

# I have implemented a very useful build system for LaTeX with log processing and debouncing
watch:
	@poetry run python src/commands/watcher.py all

watch-figures:
	@poetry run python src/commands/watcher.py figures
