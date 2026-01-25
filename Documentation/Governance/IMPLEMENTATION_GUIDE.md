# Sono-Eval Implementation Guide

This guide provides detailed implementation patterns and architectural references for the Sono-Eval system. It consolidates technical specifications for security, machine learning, testing, and deployment.

**Note**: For project status and feature planning, refer to [ROADMAP.md](../../../ROADMAP.md).

---

## 1. Security Implementation

### Authentication System

Recommended implementation pattern using `fastapi-users` or custom JWT:

```python
# Use fastapi-users or implement custom
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

# Add to api/main.py
jwt_authentication = JWTAuthentication(
    secret=settings.SECRET_KEY,
    lifetime_seconds=3600,
)
```

### Rate Limiting

Implementation using `slowapi`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@limiter.limit("10/minute")
@app.post("/api/v1/assessments")
async def create_assessment(...):
    ...
```

### Input Validation

Pydantic validation pattern:

```python
from pydantic import Field, field_validator
import re

class CandidateCreateRequest(BaseModel):
    candidate_id: str = Field(..., min_length=1, max_length=100)

    @field_validator("candidate_id")
    def validate_id(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Invalid candidate_id format')
        return v
```

### CORS Enforcement

Production startup check pattern:

```python
# In api/main.py startup
if config.app_env == "production" and config.allowed_hosts == "*":
    raise ValueError("ALLOWED_HOSTS must be set in production")
```

### Security Headers

Middleware configuration:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

if config.app_env == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=config.allowed_hosts.split(",")
    )
```

### Audit Logging

Context-aware logging pattern:

```python
# Add audit logger
audit_logger = logging.getLogger('audit')

@app.post("/api/v1/assessments")
async def create_assessment(
    assessment_input: AssessmentInput,
    user: User = Depends(get_current_user)
):
    audit_logger.info(
        f"Assessment created by {user.id} for {assessment_input.candidate_id}"
    )
```

---

## 2. ML Architecture

### ML Assessment Engine

Structure for the ML-based assessment engine:

```python
class MLAssessmentEngine(AssessmentEngine):
    def __init__(self):
        super().__init__()
        self.model = self._load_model()

    def _load_model(self):
        """Load trained ML model."""
        from transformers import AutoModelForSequenceClassification
        return AutoModelForSequenceClassification.from_pretrained(
            self.config.assessment_model_path
        )

    async def _evaluate_path(self, path: PathType, input_data: AssessmentInput):
        """Real ML-based evaluation."""
        features = self._extract_features(input_data)
        prediction = self.model.predict(features)
        return self._format_results(prediction)
```

**Key Considerations**:

- Use transfer learning from CodeBERT/GraphCodeBERT
- Fine-tune BERT for specific code understanding tasks
- Implement caching for common patterns

---

## 3. Testing Strategy

### API Integration Tests

Using `TestClient`:

```python
# tests/integration/test_api.py
from fastapi.testclient import TestClient

def test_create_assessment_authenticated():
    """Test assessment creation with authentication."""
    client = TestClient(app)
    token = get_test_token()
    response = client.post(
        "/api/v1/assessments",
        headers={"Authorization": f"Bearer {token}"},
        json=test_data
    )
    assert response.status_code == 200
```

### CLI Tests

Using `click.testing`:

```python
# tests/test_cli.py
from click.testing import CliRunner
from sono_eval.cli.main import cli

def test_assess_command():
    """Test assess command."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        'assess', 'run',
        '--candidate-id', 'test',
        '--file', 'test.py'
    ])
    assert result.exit_code == 0
```

### Security Tests

Injection prevention verification:

```python
# tests/security/test_injection.py
def test_sql_injection_prevention():
    """Test that SQL injection is prevented."""
    malicious_id = "test'; DROP TABLE candidates; --"
    response = client.post(
        "/api/v1/candidates",
        json={"candidate_id": malicious_id}
    )
    assert response.status_code == 422  # Validation error
```

### Performance Tests

Locust load testing pattern:

```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between

class AssessmentUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_assessment(self):
        self.client.post("/api/v1/assessments", json=test_data)
```

---

## 4. Deployment Configuration

### Docker Production Setup

Recommended `docker-compose.prod.yml` configuration:

```yaml
services:
  sono-eval:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
```

### Monitoring via Prometheus

FastAPI instrumentation:

```python
# Add to api/main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```
