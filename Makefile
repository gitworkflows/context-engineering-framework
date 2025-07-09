.PHONY: install test lint format clean

# Variables
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
MYPY = mypy
ISORT = isort
FLAKE8 = flake8

# Default target
all: install

# Install the package in development mode
install:
	$(PIP) install -e .[dev]

# Run tests
test:
	$(PYTEST) tests/ -v --cov=src --cov-report=term-missing --cov-report=xml

# Run linters
lint:
	$(FLAKE8) src/
	$(MYPY) src/
	$(ISORT) --check-only src/

# Format code
format:
	$(BLACK) src/ tests/ examples/
	$(ISORT) src/ tests/ examples/

# Clean up build artifacts
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/ .coverage htmlcov/
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

# Run all checks (test, lint, format)
check: test lint

# Show help
help:
	@echo "Available targets:"
	@echo "  install   - Install the package in development mode"
	@echo "  test      - Run tests with coverage"
	@echo "  lint      - Run all linters"
	@echo "  format    - Format code"
	@echo "  clean     - Remove build artifacts"
	@echo "  check     - Run all checks (test, lint)"
