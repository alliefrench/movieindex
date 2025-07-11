# Poetry Migration Guide

## 🎉 New Development Workflow with Poetry

### Quick Start

```bash
# Install dependencies
make install

# Run development server
make dev

# Run tests
make test

# Format code
make format

# See all commands
make help
```

### Poetry Commands

```bash
# Install dependencies
poetry install

# Run development server
poetry run uvicorn api.main:app --reload

# Run tests
poetry run pytest

# Add new dependency
poetry add fastapi

# Add dev dependency
poetry add --group dev pytest

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree

# Activate shell
poetry shell
```

### Development Environment Setup

1. **Install Poetry** (if not already installed):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install project dependencies**:

   ```bash
   poetry install
   ```

3. **Set up pre-commit hooks**:

   ```bash
   poetry run pre-commit install
   ```

4. **Start development server**:
   ```bash
   make dev
   # or
   poetry run uvicorn api.main:app --reload
   ```

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **pytest**: Testing
- **pre-commit**: Git hooks for quality checks

### Migration Benefits

✅ **Better dependency management**
✅ **Automatic virtual environment handling**
✅ **Lock files for reproducible builds**
✅ **Cleaner project structure**
✅ **Integrated development tools**
✅ **Better CI/CD integration**

### Old vs New Commands

| Old (pip/venv)                    | New (Poetry)         |
| --------------------------------- | -------------------- |
| `source venv/bin/activate`        | `poetry shell`       |
| `pip install -r requirements.txt` | `poetry install`     |
| `pip install package`             | `poetry add package` |
| `python -m pytest`                | `poetry run pytest`  |
| `uvicorn api.main:app --reload`   | `make dev`           |

### Production Deployment

Poetry can still export requirements.txt for deployment:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
