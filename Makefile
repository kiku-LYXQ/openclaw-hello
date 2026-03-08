PYTHON ?= python

.PHONY: help run test lint

help:
	@echo "Available targets: run test lint"
	@echo "  run  - launch the game (runs inside hello-app)"
	@echo "  test - execute the game logic unit tests"
	@echo "  lint - sanity-check Python syntax via py_compile"

run:
	@cd hello-app && $(PYTHON) -m snake_game

test:
	@cd hello-app && $(PYTHON) -m unittest snake_game.tests.test_logic

lint:
	@cd hello-app && $(PYTHON) -m py_compile snake_game/*.py snake_game/tests/*.py
