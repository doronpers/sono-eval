---
description: Standardize linting configuration across repositories
---

# Standardize Linting Configuration

This workflow applies the "Golden Configuration" for linting to the current
repository. It sets up `pre-commit`, `flake8`, and `pyproject.toml` to
ensure consistent code quality and ignore non-critical errors.

1. **Create/Update `.flake8`**
   - Sets `max-line-length = 100`
   - Ignores strict docstring rules (`D400`, `D412`, etc.)

```bash
cat > .flake8 << 'EOF'
[flake8]
max-line-length = 100
extend-ignore = E203, W503, D400, D401, D412, D205, D413, D100, D101, D102, \
                D103, D106, D107
exclude = .git,__pycache__,venv,.venv,node_modules,dist,build,.mypy_cache,.pytest_cache
EOF
```

1. **Create/Update `.pre-commit-config.yaml`**
   - Configures `flake8` to use the config file: `args: [--config=.flake8]`
   - Adds `black`, `isort`, `bandit`, `mypy`, `check-yaml`, \
     `trailing-whitespace`, etc.

```bash
cat > .pre-commit-config.yaml << 'EOF'
# Pre-commit hooks configuration
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=1000]

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3
        args: [--line-length=100]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--config=.flake8]
        additional_dependencies:
          - flake8-docstrings
          - flake8-bugbear

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black, --line-length=100]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
EOF
```

1. **Install Pre-commit Hooks**

```bash
pre-commit install
```

1. **Run Validation**

```bash
pre-commit run --all-files
```
