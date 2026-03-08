PYTHON ?= python

.PHONY: help run test lint

help:
	@echo "Available targets: run test lint"
	@echo "  run  - launch the game"
	@echo "  test - execute the game logic unit tests"
	@echo "  lint - sanity-check Python syntax via py_compile"

run:
	@$(PYTHON) -m snake_game

test:
	@$(PYTHON) -m unittest snake_game.tests.test_logic

lint:
	@$(PYTHON) -m py_compile snake_game/*.py snake_game/tests/*.py
