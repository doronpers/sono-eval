# Quick Reference: Security & Best Practices

## For Developers Working on Sono-Eval

This is a quick reference guide. For comprehensive information, see:

- 📘 [SECURITY.md](../../SECURITY.md) - Full security documentation
- 📊 [CODE_REVIEW_REPORT.md](../Reports/CODE_REVIEW_REPORT.md) - Detailed code analysis
- 🗺️ [IMPROVEMENT_ROADMAP.md](../Governance/IMPROVEMENT_ROADMAP.md) - Development roadmap
- 📋 [ASSESSMENT_SUMMARY.md](../Reports/ASSESSMENT_SUMMARY.md) - Executive summary

---

## ⚠️ Before You Deploy

### Production Checklist (Critical)

**DO NOT deploy to production without**:

- [ ] Change `SECRET_KEY` from default
- [ ] Change `SUPERSET_SECRET_KEY` from default
- [ ] Set `ALLOWED_HOSTS` to specific domains (not `*`)
- [ ] Set strong `REDIS_PASSWORD`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS/TLS
- [ ] Change Superset admin password
- [ ] Review firewall rules

**Commands to generate secure keys**:

```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# SUPERSET_SECRET_KEY
openssl rand -base64 42
```

---

## 🔒 Security Essentials

### Input Validation Pattern

**ALWAYS validate user input**:

```python
from pydantic import BaseModel, Field, field_validator
import re

class MyRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)

    @field_validator("user_id")
    def validate_user_id(cls, v):
        # Only allow alphanumeric, dash, underscore
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Invalid format')
        return v
```

### SQL Injection Prevention

**DO**: Use SQLAlchemy ORM

```python
# GOOD
candidate = session.query(Candidate).filter_by(id=candidate_id).first()
```

**DON'T**: String concatenation

```python
# BAD - Vulnerable to SQL injection
query = f"SELECT * FROM candidates WHERE id = '{candidate_id}'"
```

### Path Traversal Prevention

```python
from pathlib import Path

def safe_path(base_dir: Path, user_path: str) -> Path:
    """Ensure path is within base directory."""
    full_path = (base_dir / user_path).resolve()
    if not str(full_path).startswith(str(base_dir.resolve())):
        raise ValueError("Invalid path")
    return full_path
```

### XSS Prevention

```python
from markupsafe import escape

# Escape user content before displaying
safe_name = escape(user_provided_name)
```

---

## 🧪 Testing Patterns

### Basic Test Structure

```python
import pytest
from sono_eval.assessment.engine import AssessmentEngine

@pytest.mark.asyncio
async def test_assessment_validates_input():
    """Test that invalid input is rejected."""
    engine = AssessmentEngine()

    # Test invalid candidate_id
    with pytest.raises(ValueError):
        await engine.assess(AssessmentInput(
            candidate_id="invalid@#$",  # Should fail
            ...
        ))
```

### API Test Pattern

```python
from fastapi.testclient import TestClient
from sono_eval.api.main import app

def test_api_endpoint():
    """Test API endpoint."""
    client = TestClient(app)
    response = client.post(
        "/api/v1/assessments",
        json={"candidate_id": "test", ...}
    )
    assert response.status_code == 200
```

---

## 📝 Code Style

### Docstrings

```python
async def assess(self, assessment_input: AssessmentInput) -> AssessmentResult:
    """
    Perform comprehensive assessment.

    Args:
        assessment_input: Assessment input data with candidate info

    Returns:
        Complete assessment result with scores and explanations

    Raises:
        ValueError: If input validation fails
        RuntimeError: If assessment engine not initialized
    """
    pass
```

### Type Hints

```python
from typing import List, Optional, Dict, Any

def process_data(
    data: Dict[str, Any],
    options: Optional[List[str]] = None
) -> bool:
    """Always use type hints."""
    pass
```

### Error Handling

```python
# Good error handling
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise HTTPException(
        status_code=400,
        detail="Clear error message for user"
    )
```

---

## 🚀 Performance Tips

### Use Async/Await

```python
# Good - non-blocking
async def fetch_data():
    result = await async_database_call()
    return result

# Bad - blocking
def fetch_data():
    result = sync_database_call()  # Blocks the event loop
    return result
```

### Cache Expensive Operations

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(param: str) -> int:
    """Cache results of expensive operations."""
    # Heavy computation here
    return result
```

### Lazy Loading

```python
class TagGenerator:
    def __init__(self):
        self.model = None
        self._initialized = False

    def initialize(self):
        """Lazy load model only when needed."""
        if not self._initialized:
            self.model = load_heavy_model()
            self._initialized = True
```

---

## 🐛 Debugging

### Logging Levels

```python
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)

# Use appropriate levels
logger.debug("Detailed info for debugging")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure")
```

### What NOT to Log

```python
# DON'T log sensitive data
logger.info(f"User login: {username}:{password}")  # BAD
logger.info(f"API key: {api_key}")  # BAD
logger.info(f"Credit card: {cc_number}")  # BAD

# DO log safely
logger.info(f"Login attempt for user: {username}")  # GOOD
logger.info("API key validation succeeded")  # GOOD
```

---

## 🔧 Common Patterns

### Pydantic Models

```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    """Use Pydantic for validation."""

    name: str = Field(..., min_length=1, max_length=100)
    score: float = Field(ge=0.0, le=100.0)

    class Config:
        # Enable ORM mode if needed
        from_attributes = True
```

### FastAPI Endpoints

```python
from fastapi import HTTPException

@app.post("/api/v1/resource")
async def create_resource(data: MyRequest) -> MyResponse:
    """
    Create a new resource.

    - **data**: Resource data

    Returns resource with generated ID.
    """
    if not service.is_initialized():
        raise HTTPException(
            status_code=503,
            detail="Service not initialized"
        )

    try:
        result = await service.create(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Environment Configuration

```python
from sono_eval.utils.config import get_config

config = get_config()

# Access configuration
if config.app_env == "production":
    # Production-specific logic
    pass

# Check required settings
if not config.secret_key:
    raise ValueError("SECRET_KEY must be set")
```

---

## 📦 Dependencies

### Adding New Dependencies

1. Add to `pyproject.toml`:

   ```toml
   dependencies = [
       "newpackage>=1.0.0",
   ]
   ```

2. **Security Check** (REQUIRED):

   ```bash
   # Install safety
   pip install safety

   # Check for vulnerabilities
   safety check

   # Or use pip-audit
   pip install pip-audit
   pip-audit
   ```

3. Update requirements:

   ```bash
   pip install -e ".[dev]"
   pip freeze > requirements.txt
   ```

### Security Scanning

```bash
# Before committing new dependencies
bandit -r src/  # Code security
safety check    # Dependency vulnerabilities
```

---

## 🔥 Common Mistakes to Avoid

### 1. Hardcoded Secrets ❌

```python
# BAD
API_KEY = "sk-1234567890abcdef"

# GOOD
from sono_eval.utils.config import get_config
config = get_config()
api_key = config.api_key
```

### 2. Ignoring Validation ❌

```python
# BAD
@app.post("/api/v1/users")
async def create_user(user_id: str):  # No validation
    ...

# GOOD
class UserCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)

@app.post("/api/v1/users")
async def create_user(user: UserCreate):
    ...
```

### 3. Blocking the Event Loop ❌

```python
# BAD - Blocks async event loop
async def process():
    time.sleep(10)  # Blocking!

# GOOD
async def process():
    await asyncio.sleep(10)  # Non-blocking
```

### 4. Not Handling Errors ❌

```python
# BAD
def risky_operation():
    result = might_fail()
    return result

# GOOD
def risky_operation():
    try:
        result = might_fail()
        return result
    except SpecificError as e:
        logger.error(f"Operation failed: {e}")
        raise
```

### 5. Exposing Internal Errors ❌

```python
# BAD - Exposes internal details
@app.get("/api/v1/data")
async def get_data():
    try:
        return fetch_data()
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # BAD!

# GOOD - Generic error message
@app.get("/api/v1/data")
async def get_data():
    try:
        return fetch_data()
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        raise HTTPException(500, detail="Internal server error")
```

---

## 🏃 Quick Commands

### Development

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/sono_eval

# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

### Docker

```bash
# Start all services
./launcher.sh start

# View logs
./launcher.sh logs

# Stop services
./launcher.sh stop

# Restart
./launcher.sh restart
```

### Security Scans

```bash
# Code security
bandit -r src/

# Dependency vulnerabilities
safety check

# Docker security
trivy image sono-eval:latest
```

---

## 📚 Reference Links

- **Security**: [SECURITY.md](../../SECURITY.md)
- **Code Review**: [CODE_REVIEW_REPORT.md](../Reports/CODE_REVIEW_REPORT.md)
- **Roadmap**: [IMPROVEMENT_ROADMAP.md](../Governance/IMPROVEMENT_ROADMAP.md)
- **Summary**: [ASSESSMENT_SUMMARY.md](../Reports/ASSESSMENT_SUMMARY.md)

### External Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

## 🆘 Getting Help

- Check documentation first
- Search existing issues
- Ask in team chat
- Create detailed issue with:
  - Clear description
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details

---

**Last Updated**: January 10, 2026  
**Version**: 0.1.1  
**Maintainer**: Sono-Eval Team

---

Remember: **Security first, always validate input, test thoroughly!**
