# Production Deployment Guide

This guide outlines production-readiness enhancements and deployment considerations for Sono-Eval.

## Overview of Production Hardening

Sono-Eval now includes comprehensive production features:

### 1. **Rate Limiting**
- Per-IP rate limiting: 60 requests/minute, 1000 requests/hour (configurable)
- Automatic rate limit headers in responses
- Graceful handling of rate limit exceeding requests

**Location**: `src/sono_eval/middleware/rate_limiter.py`

**Configuration**:
```python
# In src/sono_eval/api/main.py:
app.add_middleware(
    RateLimitMiddleware,
    max_requests_per_minute=60,
    max_requests_per_hour=1000,
)
```

### 2. **Circuit Breaker Pattern**
- Protects against cascading failures
- Automatic recovery with half-open state testing
- Per-service circuit breaker management

**Location**: `src/sono_eval/middleware/circuit_breaker.py`

**Usage**:
```python
from sono_eval.middleware.circuit_breaker import circuit_breaker_pool

breaker = circuit_breaker_pool.get_or_create("redis_service")
result = await breaker.call(redis_operation)

# Check circuit breaker status
status = circuit_breaker_pool.get_status()
```

### 3. **Performance Logging**
- Automatic request/response timing
- Slow request detection (>1s threshold)
- Structured JSON logging with request IDs
- Performance metrics in response headers

**Location**: `src/sono_eval/middleware/performance.py`

**Features**:
- `X-Process-Time` header in all responses
- Detailed logging for slow requests
- Request/response context preserved

### 4. **Response Caching**
- In-memory caching with TTL
- Automatic cache invalidation
- Cache statistics

**Location**: `src/sono_eval/middleware/cache.py`

**Usage**:
```python
from sono_eval.middleware.cache import cached

@cached(ttl_seconds=300)
async def expensive_operation(param):
    return result
```

### 5. **Health Check Endpoints**

#### System Status
- **`GET /api/v1/status/system`**: Full system status with circuit breaker states
- **`GET /api/v1/status/readiness`**: Kubernetes readiness probe
- **`GET /api/v1/status/liveness`**: Kubernetes liveness probe
- **`GET /health`**: Traditional health check

**Example Response** (`/api/v1/status/system`):
```json
{
  "timestamp": "2026-01-22T10:30:00.000000Z",
  "version": "0.1.1",
  "environment": "production",
  "health": {
    "status": "healthy",
    "components": {
      "assessment": "operational",
      "memory": "operational",
      "tagging": "operational",
      "database": "operational",
      "redis": "operational",
      "filesystem": "operational",
      "circuit_breakers": "operational"
    }
  },
  "circuit_breakers": {},
  "configuration": {
    "rate_limit_per_minute": 60,
    "rate_limit_per_hour": 1000,
    "request_timeout": "30s",
    "cache_enabled": true,
    "performance_logging": true
  }
}
```

## Deployment Configuration

### Environment Variables

```bash
# Application
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# Security
SECRET_KEY=<generate-strong-random-key>
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com

# Database (CRITICAL - do not use SQLite in production)
DATABASE_URL=postgresql://user:password@postgres.example.com:5432/sono_eval

# Redis
REDIS_HOST=redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=<strong-password>

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB

# Assessment
ASSESSMENT_ENABLE_EXPLANATIONS=true
ASSESSMENT_MULTI_PATH_TRACKING=true

# Superset
SUPERSET_HOST=superset.example.com
SUPERSET_SECRET_KEY=<generate-strong-random-key>
```

### Database Setup

**CRITICAL**: Never use SQLite in production!

```bash
# Create PostgreSQL database
createdb sono_eval

# Run migrations
alembic upgrade head

# Verify schema
psql -d sono_eval -c "\dt"
```

### Docker Deployment

```bash
# Build image
docker build -t sono-eval:0.1.1 .

# Run with health checks
docker run \
  -e APP_ENV=production \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_HOST=redis \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  -p 8000:8000 \
  sono-eval:0.1.1
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sono-eval-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sono-eval-api
  template:
    metadata:
      labels:
        app: sono-eval-api
    spec:
      containers:
      - name: sono-eval
        image: sono-eval:0.1.1
        ports:
        - containerPort: 8000
        env:
        - name: APP_ENV
          value: production
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: sono-eval-secrets
              key: database-url
        - name: REDIS_HOST
          value: redis-service
        livenessProbe:
          httpGet:
            path: /api/v1/status/liveness
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/v1/status/readiness
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### Monitoring & Observability

#### Log Collection
```bash
# Structured logs to external service
docker run \
  -e LOG_LEVEL=INFO \
  -v /var/log/sono-eval:/app/logs \
  sono-eval:0.1.1
```

#### Metrics (Production ready with Prometheus)
Add to your monitoring stack:
- Rate limit violations
- Circuit breaker state transitions
- Request latency histogram
- Cache hit/miss ratio
- Component health status

#### Example Prometheus queries:
```
# Rate of rate limit violations
rate(http_requests_limited_total[5m])

# Circuit breaker state
circuit_breaker_state{name="redis_service"}

# Request latency p99
histogram_quantile(0.99, rate(http_request_duration_seconds[5m]))
```

## Security Checklist

- [ ] Database URL uses PostgreSQL (not SQLite)
- [ ] `SECRET_KEY` is cryptographically strong
- [ ] `ALLOWED_HOSTS` restricts CORS to known domains
- [ ] File upload limits configured (`MAX_UPLOAD_SIZE`)
- [ ] Redis password set and strong
- [ ] `.env` file is NOT committed to version control
- [ ] HTTPS enabled on production endpoints
- [ ] Rate limiting active (default: 60/min, 1000/hour)
- [ ] Health checks configured for orchestration
- [ ] Structured logging enabled (`LOG_LEVEL=INFO`)
- [ ] Circuit breakers monitored for state transitions
- [ ] Database backups scheduled
- [ ] Security scans included in CI/CD (Bandit, Safety, pip-audit)

## Performance Tuning

### Assessment Engine
```bash
# Increase batch processing for throughput
MAX_CONCURRENT_ASSESSMENTS=8
BATCH_SIZE=64
```

### Caching
```python
from sono_eval.middleware.cache import get_cache_stats

# Monitor cache efficiency
stats = get_cache_stats()
print(f"Cached entries: {stats['cached_entries']}")
print(f"Memory usage: {stats['memory_usage_estimate']} bytes")
```

### Database Connection Pool
```python
# Adjust for your workload (PostgreSQL)
DATABASE_URL=postgresql://user:pass@host/db?max_connections=20
```

## Troubleshooting Production Issues

### Rate Limiting Too Strict
```python
# Adjust in api/main.py for your SLA
app.add_middleware(
    RateLimitMiddleware,
    max_requests_per_minute=120,  # Increase from 60
    max_requests_per_hour=2000,   # Increase from 1000
)
```

### Circuit Breaker Open for Redis
```bash
# Check Redis health
redis-cli ping
# Outputs: PONG

# Check circuit breaker status
curl http://localhost:8000/api/v1/status/system | jq .circuit_breakers
```

### Slow Requests
Check response headers and logs:
```bash
curl -i http://localhost:8000/api/v1/health
# Look for: X-Process-Time: 0.234
```

## Next Steps

1. **Monitoring**: Integrate Prometheus/Grafana or your APM solution
2. **Load Testing**: Run k6 or locust to verify rate limits and performance
3. **Disaster Recovery**: Test database failover and Redis recovery
4. **Security Audit**: Run OWASP ZAP or similar security scanner
5. **Capacity Planning**: Monitor resource usage and scale based on metrics

---

For more details, see:
- [SECURITY.md](../SECURITY.md) - Security best practices
- [docker-compose.yml](../docker-compose.yml) - Local environment setup
- [src/sono_eval/utils/config.py](../src/sono_eval/utils/config.py) - Configuration options
