.PHONY: format
format:
	python -m pyright ./src
	python -m ruff check . --fix
	python -m black .