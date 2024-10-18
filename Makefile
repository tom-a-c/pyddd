SHELL=/bin/bash

.PHONY: docs
docs:
	sphinx-build -M html docs docs/_build

.PHONY: install
install:
	poetry install
	poetry run pre-commit install

.PHONY: test
test:
	poetry run pytest
