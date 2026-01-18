# Security Policy

## Supported Versions

Currently, Sono-Eval is in **alpha** (version 0.1.0). Security updates are
provided for:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: <security@sono-eval.example>
(or create a private security advisory on GitHub)

When reporting a vulnerability, please include:

1. **Type of vulnerability** (e.g., XSS, SQL injection, etc.)
2. **Full paths** of affected source files
3. **Location** of the affected code (tag/branch/commit)
4. **Step-by-step instructions** to reproduce the issue
5. **Proof-of-concept or exploit code** (if possible)
6. **Impact** of the vulnerability
7. **Suggested fix** (if you have one)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: Next release cycle

## Security Best Practices

### For Deployment

#### 1. Environment Variables

**CRITICAL**: Change default secrets before production deployment:

```bash
# .env file - NEVER commit this file
SECRET_KEY=<generate-strong-random-key>
SUPERSET_SECRET_KEY=<generate-strong-random-key>
REDIS_PASSWORD=<strong-password>
DATABASE_URL=postgresql://user:<strong-password>@host:5432/db
```

Generate secure keys:

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate SUPERSET_SECRET_KEY
openssl rand -base64 42
```

#### 2. CORS Configuration

**Default**: Allows all origins (development only)

**Production**: Restrict CORS to your domains:

```bash
# .env
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

In production, the API automatically restricts CORS based on `ALLOWED_HOSTS`.

#### 3. File Uploads

**Current Limits**:

- Max file size: 10MB (configurable via `MAX_UPLOAD_SIZE`)
- Allowed extensions: py, js, ts, java, cpp, c, go, rs, rb

**Recommendations**:

- Use virus scanning for uploaded files
- Store uploads in isolated storage
- Validate file content, not just extensions
- Implement rate limiting

#### 4. Database Security

**SQLite** (default): Only for development

- Not suitable for production
- No concurrent write support
- No user authentication

**PostgreSQL** (recommended): For production

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/sono_eval
```

Security checklist:

- [ ] Use strong database passwords
- [ ] Restrict database network access
- [ ] Enable SSL/TLS connections
- [ ] Regular backups
- [ ] Apply security updates

#### 5. API Security

**Current State**: No authentication (alpha version)

**Before Production**:

- [ ] Implement API key authentication
- [ ] Add rate limiting
- [ ] Add request validation
- [ ] Enable HTTPS only
- [ ] Add audit logging
- [ ] Implement RBAC (Role-Based Access Control)

Example rate limiting (recommended):

```python
# Add to requirements.txt: slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@limiter.limit("10/minute")
@app.post("/api/v1/assessments")
async def create_assessment(...):
    ...
```

#### 6. Network Security

**Docker Deployment**:

```yaml
# Production docker-compose.yml
services:
  sono-eval:
    networks:
      - internal
    # Don't expose ports directly

  nginx:
    networks:
      - internal
      - external
    ports:
      - "443:443"  # HTTPS only
```

**Firewall Rules**:

- Only expose necessary ports
- Use reverse proxy (nginx/traefik)
- Enable HTTPS/TLS
- Block direct database access from internet

### For Development

#### 1. Code Security

**Input Validation**: Always validate and sanitize user input

```python
from pydantic import BaseModel, Field, validator

class AssessmentInput(BaseModel):
    candidate_id: str = Field(..., min_length=1, max_length=100)

    @validator('candidate_id')
    def validate_candidate_id(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('candidate_id must be alphanumeric')
        return v
```

**SQL Injection Prevention**: Use ORMs (SQLAlchemy) with parameterized queries

```python
# GOOD: Using SQLAlchemy ORM
candidate = session.query(Candidate).filter_by(id=candidate_id).first()

# BAD: String concatenation (vulnerable to SQL injection)
# query = f"SELECT * FROM candidates WHERE id = '{candidate_id}'"
```

**Path Traversal Prevention**: Validate file paths

```python
from pathlib import Path

def safe_path(base_dir: Path, user_path: str) -> Path:
    """Ensure path is within base directory."""
    full_path = (base_dir / user_path).resolve()
    if not str(full_path).startswith(str(base_dir.resolve())):
        raise ValueError("Invalid path")
    return full_path
```

**XSS Prevention**: Escape user content in responses

```python
from markupsafe import escape

@app.get("/api/v1/candidates/{candidate_id}")
async def get_candidate(candidate_id: str):
    # candidate_id is automatically validated by Pydantic
    # But escape when displaying user content
    return {"name": escape(candidate.name)}
```

#### 2. Dependency Security

**Regular Updates**: Check for vulnerabilities

```bash
# Install safety
pip install safety

# Check dependencies
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

**Known Issues**:

- Review `requirements.txt` and `pyproject.toml` regularly
- Update dependencies with security patches
- Use `dependabot` for automated alerts

#### 3. Secret Management

**NEVER commit**:

- API keys
- Passwords
- Private keys
- `.env` files
- Database credentials

**Use**:

- Environment variables
- Secret management services (AWS Secrets Manager, HashiCorp Vault)
- `.env.example` for documentation (without real values)

#### 4. Logging and Monitoring

**Do Log**:

- Authentication attempts
- Authorization failures
- Input validation failures
- System errors

**Don't Log**:

- Passwords
- API keys
- Personal identifiable information (PII)
- Session tokens
- Credit card numbers

```python
# GOOD
logger.info(f"Login attempt for user: {username}")

# BAD
logger.info(f"Login attempt: {username}:{password}")
```

## Known Security Limitations (v0.1.0)

### Critical Issues

1. **No Authentication**: API endpoints are publicly accessible
   - **Risk**: Anyone can access all data and functionality
   - **Mitigation**: Deploy behind firewall, use VPN
   - **Fix**: Planned for v0.2.0

2. **Default Secret Keys**: Hardcoded in `.env.example`
   - **Risk**: If used in production, system is compromised
   - **Mitigation**: MUST change before deployment
   - **Fix**: Add validation to reject default keys

3. **CORS Allows All Origins**: Default accepts requests from any domain
   - **Risk**: Cross-site attacks possible
   - **Mitigation**: Set `ALLOWED_HOSTS` environment variable
   - **Fix**: Enforce in production mode

### High Priority Issues

1. **No Rate Limiting**: APIs can be abused
   - **Risk**: DoS attacks, resource exhaustion
   - **Mitigation**: Use reverse proxy with rate limiting
   - **Fix**: Planned for v0.2.0

2. **No Input Sanitization**: File uploads not validated
   - **Risk**: Malicious file uploads
   - **Mitigation**: Restrict file extensions, scan uploads
   - **Fix**: Add content validation

3. **Superset Default Credentials**: admin/admin
   - **Risk**: Unauthorized access to analytics
   - **Mitigation**: Change immediately after setup
   - **Fix**: Force password change on first login

### Medium Priority Issues

1. **HTTP Only**: No HTTPS enforcement
   - **Risk**: Data transmitted in clear text
   - **Mitigation**: Use reverse proxy with TLS
   - **Fix**: Add HTTPS redirect option

2. **No Audit Logging**: No record of who did what
   - **Risk**: Can't track security incidents
   - **Mitigation**: Enable web server logging
   - **Fix**: Planned for v0.2.0

3. **Placeholder Assessment Logic**: Not real ML
   - **Risk**: Predictable outputs, gaming system
   - **Mitigation**: Document as alpha limitation
   - **Fix**: Implement real ML models

## Security Checklist for Production

Before deploying to production:

### Essential (Must Do)

- [ ] Change `SECRET_KEY` from default
- [ ] Change `SUPERSET_SECRET_KEY` from default
- [ ] Set strong `REDIS_PASSWORD`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure `ALLOWED_HOSTS` for CORS
- [ ] Enable HTTPS/TLS
- [ ] Change Superset admin password
- [ ] Review and restrict exposed ports
- [ ] Set up firewall rules
- [ ] Enable backup strategy

### Recommended (Should Do)

- [ ] Implement API authentication
- [ ] Add rate limiting
- [ ] Enable audit logging
- [ ] Set up monitoring and alerts
- [ ] Implement input validation for all endpoints
- [ ] Add virus scanning for uploads
- [ ] Use secret management service
- [ ] Enable automated security scanning
- [ ] Set up intrusion detection
- [ ] Document incident response plan

### Optional (Nice to Have)

- [ ] Enable Web Application Firewall (WAF)
- [ ] Implement Content Security Policy (CSP)
- [ ] Add security headers
- [ ] Enable HSTS (HTTP Strict Transport Security)
- [ ] Implement multi-factor authentication
- [ ] Set up security information and event management (SIEM)

## Security Resources

### Tools

- **OWASP ZAP**: Web application security scanner
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner
- **pip-audit**: Python package vulnerability auditor
- **Trivy**: Container vulnerability scanner

### References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)

## Contact

For security concerns, contact: <security@sono-eval.example>

For general issues: <https://github.com/doronpers/sono-eval/issues>

---

**Last Updated**: January 10, 2026  
**Version**: 0.1.0
