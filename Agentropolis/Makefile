.PHONY: help install test lint format clean

help:
	@echo "Agentropolis Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  install    - Install Python dependencies"
	@echo "  test       - Run test suite"
	@echo "  lint       - Run linters"
	@echo "  format     - Auto-format code"

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	black --check agentropolis tests
	flake8 agentropolis tests

format:
	black agentropolis tests
	isort agentropolis tests
