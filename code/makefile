.PHONY: test lint

test:
	@poetry run pytest --capture=tee-sys

lint:
	@poetry run pycodestyle src
	@poetry run mypy src

format-figures:
	@poetry run python format_matrices.py ../figures/*.tex

# I have implemented a very useful build system for LaTeX with log processing and debouncing
watch:
	@poetry run python watcher.py all

watch-figures:
	@poetry run python watcher.py figures
