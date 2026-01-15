# Contributing to Sono-Eval

Thank you for your interest in contributing to Sono-Eval! This document provides guidelines and instructions for contributing.

## Quick Start (No Terminal)

New to contributing? Start here! You can make your first contribution entirely in your browser:

1. **Fork the repository** (click "Fork" button on GitHub)
2. **Edit a file in your fork**:
   - Navigate to the file you want to edit
   - Click the pencil icon (✏️) to edit
   - Make your changes (try adding a note to README.md about your experience)
   - Scroll down and click "Commit changes"
3. **Open a pull request**:
   - Click "Contribute" → "Open pull request" on your fork's main page
   - Add a description of your changes
   - Click "Create pull request"

That's it! No command line needed.

## Quick Start (Browser Dev Environment)

Want to test changes before submitting? Use GitHub Codespaces:

1. **Open in Codespaces**:
   - Click "Code" → "Codespaces" → "Create codespace on main"
   - Wait for environment to load (~2 minutes)
2. **Start the server**:
   - Open Terminal in VS Code web interface
   - Run: `./launcher.sh start`
   - Access `/docs` via the Ports tab
3. **Make changes**:
   - Edit files in the VS Code web interface
   - Test in real-time using the `/docs` interface
4. **Commit and open PR**:
   - Use the Source Control tab in VS Code
   - Commit your changes
   - Click "Publish Branch" and create a PR

## Quick Start (Local, Minimal Terminal)

Prefer working locally? Here's the minimal setup:

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/sono-eval.git
cd sono-eval

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Start development server
./launcher.sh dev
# OR manually: sono-eval server start --reload
```

### Testing Your Changes

```bash
# Run tests
pytest

# Format code
black src/ tests/

# Lint
flake8 src/ tests/
```

## Suggested First Issues (Low Friction)

Perfect for first-time contributors:

- **Documentation**: Add a "What I saw in /docs" note to README
- **Simple endpoint**: Add a log message to an existing endpoint
- **Testing**: Write a test for a static JSON endpoint
- **Samples**: Add example code submissions to `samples/`
- **Typos**: Fix typos in documentation or code comments

Look for issues labeled `good-first-issue` or `beginner-friendly`.

## PR Checklist

Before submitting your pull request:

- [ ] Tests added/updated if logic changed (`pytest`)
- [ ] Code formatted with `black`
- [ ] No linting errors (`flake8`)
- [ ] Documentation updated if needed
- [ ] Tested locally (try the `/docs` interface)

## Troubleshooting

**Issue**: Port 8000 already in use
**Solution**: `sono-eval server start --port 8001`

**Issue**: Permission denied on launcher.sh
**Solution**: `chmod +x launcher.sh`

**Issue**: SSL certificate errors
**Solution**: See `scripts/README.md` for SSL fix instructions

**Issue**: Tests failing
**Solution**: Make sure virtual environment is activated and dependencies are installed

**Need help?** Open a GitHub Discussion or Issue - we're friendly to beginners!

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Any relevant logs or screenshots

### Suggesting Features

We welcome feature suggestions! Please open an issue with:

- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Any relevant examples or references

### Pull Requests

1. **Fork the repository**

   ```bash
   git clone https://github.com/doronpers/sono-eval.git
   cd sono-eval
   ```

2. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**

   ```bash
   # Run tests
   pytest

   # Check coverage
   pytest --cov=src/sono_eval

   # Format code
   black src/ tests/

   # Lint
   flake8 src/ tests/
   ```

5. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push and create PR**

   ```bash
   git push origin feature/your-feature-name
   ```

   Then open a Pull Request on GitHub.

## Development Setup

### Local Environment

```bash
# Clone and setup
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Fix SSL certificate issues (if using Python 3.13 from python.org)
# See scripts/README.md for details
./scripts/fix-pre-commit-ssl.sh

# Copy environment config
cp .env.example .env
```

<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
read_file

### Docker Development

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f sono-eval

# Run tests in container
docker-compose exec sono-eval pytest
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use type hints where appropriate
- Write docstrings for all public functions/classes

Example:

```python
def assess_candidate(
    candidate_id: str,
    submission: Dict[str, Any],
    paths: Optional[List[PathType]] = None,
) -> AssessmentResult:
    """
    Assess a candidate's submission.

    Args:
        candidate_id: Unique identifier for the candidate
        submission: Submission data including code and metadata
        paths: Optional list of assessment paths to evaluate

    Returns:
        Complete assessment result with scores and explanations

    Raises:
        ValueError: If candidate_id is invalid
    """
    pass
```

### Testing

- Write unit tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Include docstrings in test functions

Example:

```python
def test_assessment_engine_technical_path():
    """Test that technical path assessment produces valid scores."""
    engine = AssessmentEngine()
    result = await engine.assess(test_input)

    assert result.overall_score >= 0
    assert result.overall_score <= 100
    assert len(result.path_scores) > 0
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new modules, classes, and functions
- Update API documentation for endpoint changes
- Include code examples where helpful

## Project Structure

```
sono-eval/
├── src/sono_eval/       # Source code
│   ├── assessment/      # Assessment engine
│   ├── memory/          # Memory storage
│   ├── tagging/         # Tagging system
│   ├── api/             # REST API
│   ├── cli/             # CLI interface
│   └── utils/           # Utilities
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── documentation/       # Documentation
├── config/              # Configuration
└── scripts/             # Utility scripts
```

## Areas for Contribution

We especially welcome contributions in:

### High Priority

- Batch assessment processing
- Additional assessment paths
- ML model fine-tuning utilities
- Performance optimizations

### Medium Priority

- Web UI for reviews
- Additional tagging strategies
- Enhanced analytics dashboards
- Integration with code platforms

### Documentation

- Tutorials and guides
- API examples
- Architecture documentation
- Translation to other languages

## Review Process

1. **Automated Checks**: All PRs must pass:
   - Unit tests
   - Code style checks (Black, Flake8)
   - Type checking (MyPy)

2. **Code Review**: Maintainers will review:
   - Code quality and style
   - Test coverage
   - Documentation
   - Adherence to architecture

3. **Feedback**: Address review comments and push updates

4. **Merge**: Once approved, maintainers will merge your PR

## Questions?

- Open an issue for questions about contributing
- Join discussions in existing issues
- Reach out to maintainers if needed

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Sono-Eval! 🎉
