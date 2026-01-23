# Completion checklist

- Run tests: `pytest`
- Run formatting: `black src/ tests/ --line-length 100`
- Run lint: `flake8 src/ tests/ --max-line-length 100 --extend-ignore E203`
- Verify any API/schema changes in docs and tests
- Check request ID propagation where endpoints touched
