.PHONY: install dev test format lint clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies with Poetry"
	@echo "  dev         Run development server"
	@echo "  test        Run tests"
	@echo "  format      Format code with black and isort"
	@echo "  lint        Run linting and type checking"
	@echo "  clean       Remove cache and build files"
	@echo "  shell       Activate Poetry shell"

# Install dependencies
install:
	poetry install

# Run development server
dev:
	poetry run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	poetry run pytest api/tests/ -v

# Format code
format:
	poetry run black api/
	poetry run isort api/

# Lint and type check
lint:
	poetry run black --check api/
	poetry run isort --check-only api/
	poetry run mypy api/

# Clean cache and build files
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf dist/
	rm -rf build/

# Activate Poetry shell
shell:
	poetry shell

# Update dependencies
update:
	poetry update

# Show dependency tree
deps:
	poetry show --tree

# Export requirements.txt (for compatibility)
export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
