SHELL=/bin/bash

.PHONY: install
install:
	poetry install
	poetry run pre-commit install

.PHONY: test
test:
	poetry run pytest
