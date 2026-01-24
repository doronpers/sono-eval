# Production Deployment Guide

**Version**: 0.2.0  
**Last Updated**: January 2026

## Overview

This guide covers deploying Sono-Eval to production environments with security, scalability, and reliability best practices.

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 20GB disk space
- Linux server (Ubuntu 20.04+ or RHEL 8+)
- SSL/TLS certificates for HTTPS

## Quick Start (Secure Production)

```bash
# 1. Clone repository
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval

# 2. Create production environment file
cp .env.example .env

# 3. Generate secure secrets
python3 -c "import secrets; print(secrets.token_urlsafe(32))"  # SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"  # SUPERSET_SECRET_KEY

# 4. Edit .env with production values
nano .env

# 5. Start services
docker-compose up -d

# 6. Verify health
curl http://localhost:8000/health
```

## Environment Configuration

### Critical Security Variables

**MUST change these in production:**

```bash
# Application
APP_ENV=production                             # CRITICAL: Set to production
SECRET_KEY=<generated-32-char-key>             # Generate with secrets.token_urlsafe(32)
DEBUG=false                                     # NEVER true in production

# Database
DATABASE_URL=postgresql://user:password@host:5432/sono_eval  # Strong password
POSTGRES_PASSWORD=<strong-password>             # NOT "postgres"

# Superset
SUPERSET_SECRET_KEY=<generated-32-char-key>    # Generate unique key
SUPERSET_ADMIN_PASSWORD=<strong-password>       # NOT "admin"

# Security
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com  # NOT "*"
ALLOWED_ORIGINS=https://yourdomain.com           # NOT "*"
```

### Optional Configuration

```bash
# API Settings
API_PORT=8000
API_WORKERS=4
MAX_UPLOAD_SIZE=10485760  # 10MB

# Rate Limiting
RATE_LIMIT_PER_MINUTE=600
RATE_LIMIT_BURST=100

# Assessment
ASSESSMENT_ENABLE_EXPLANATIONS=true
DARK_HORSE_MODE=enabled
```

## Docker Production Setup

### 1. Production docker-compose.yml

The included `docker-compose.yml` has production-ready features:

✅ **Health checks** for all services  
✅ **Resource limits** (CPU/memory)  
✅ **Restart policies** (unless-stopped)  
✅ **Volume persistence**  

**Required changes for production:**

```yaml
# Update sono-eval service
services:
  sono-eval:
    environment:
      - APP_ENV=production  # Change from development
    deploy:
      resources:
        limits:
          cpus: "4"         # Adjust based on load
          memory: 8G        # Increase for production
```

### 2. Secrets Management

**Option A: Environment Variables** (recommended for Docker)

```bash
# Use .env file (NOT committed to git)
# Docker Compose automatically loads .env

export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
export DATABASE_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")
```

**Option B: Docker Secrets** (for Swarm)

```bash
# Create secrets
echo "your-secret-key" | docker secret create sono_eval_secret_key -
echo "db-password" | docker secret create postgres_password -

# Reference in compose file
services:
  sono-eval:
    secrets:
      - sono_eval_secret_key
      - postgres_password
```

### 3. HTTPS/TLS Setup

Use a reverse proxy (nginx/Traefik) for SSL termination:

```nginx
# /etc/nginx/sites-available/sono-eval
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring & Health Checks

### Health Endpoints

```bash
# Basic health check
GET /health
# Returns: {"status": "healthy", "version": "0.2.0"}

# Detailed health check
GET /api/v1/health
# Returns: Component status and details
```

### Monitoring Setup

**Recommended tools:**

- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and visualization
- **ELK Stack**: Log aggregation

**Key metrics to monitor:**

- Request rate and latency (p50, p95, p99)
- Error rates (4xx, 5xx)
- Database connection pool usage
- Redis memory usage
- Celery queue length
- System resources (CPU, memory, disk)

### Logging

```bash
# View logs
docker-compose logs -f sono-eval
docker-compose logs -f celery-worker

# Structured JSON logging is enabled in production
# Logs include: timestamp, level, message, request_id, user_id
```

## Backup & Recovery

### Database Backups

```bash
# Daily automated backup
0 2 * * * docker exec sono-eval-postgres pg_dump -U postgres sono_eval | gzip > /backups/sono_eval_$(date +\%Y\%m\%d).sql.gz

# Restore from backup
gunzip < backup.sql.gz | docker exec -i sono-eval-postgres psql -U postgres sono_eval
```

### Volume Backups

```bash
# Backup data volumes
docker run --rm -v sono-eval_postgres-data:/data -v /backups:/backup alpine tar czf /backup/postgres-data.tar.gz /data
docker run --rm -v sono-eval_redis-data:/data -v /backups:/backup alpine tar czf /backup/redis-data.tar.gz /data
```

## Performance Tuning

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_assessments_candidate ON assessments(candidate_id);
CREATE INDEX idx_assessments_timestamp ON assessments(created_at);
```

### Redis Configuration

```bash
# In production, consider Redis cluster for HA
# Or use managed Redis (AWS ElastiCache, Azure Cache)
```

### Scaling

**Horizontal scaling:**

```yaml
# Scale Celery workers
docker-compose up -d --scale celery-worker=4

# Load balance API instances (use nginx/HAProxy)
docker-compose up -d --scale sono-eval=3
```

## Security Checklist

- [ ] Changed all default passwords
- [ ] Generated strong SECRET_KEY (32+ chars)
- [ ] Set APP_ENV=production
- [ ] Set DEBUG=false
- [ ] Configured ALLOWED_HOSTS (not "*")
- [ ] Configured ALLOWED_ORIGINS (not "*")
- [ ] Enabled HTTPS with valid certificates
- [ ] Restricted database access (firewall rules)
- [ ] Set up regular backups
- [ ] Configured log rotation
- [ ] Reviewed and applied security headers
- [ ] Rate limiting enabled and tested
- [ ] Secrets stored securely (not in git)

## Deployment Process

### Initial Deployment

```bash
1. Prepare server (install Docker, configure firewall)
2. Clone repository to /opt/sono-eval
3. Configure .env with production values
4. Generate and set secrets
5. Start services: docker-compose up -d
6. Run migrations: docker-compose exec sono-eval alembic upgrade head
7. Verify health: curl http://localhost:8000/health
8. Configure nginx reverse proxy
9. Obtain SSL certificates (Let's Encrypt)
10. Test end-to-end with authentication
```

### Updates and Rollbacks

```bash
# Update to new version
git pull
docker-compose pull
docker-compose up -d --build

# Rollback if needed
git checkout <previous-tag>
docker-compose up -d --build
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs sono-eval

# Common issues:
# - Default secrets in production (check APP_ENV)
# - Database connection (verify DATABASE_URL)
# - Port conflicts (check if 8000 is available)
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Check database connections
docker exec sono-eval-postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Check Redis memory
docker exec sono-eval-redis redis-cli INFO memory
```

## Support & Resources

- **Documentation**: `/documentation/README.md`
- **Security**: `SECURITY.md`
- **Issues**: <https://github.com/doronpers/sono-eval/issues>
- **API Reference**: `/documentation/Guides/user-guide/api-reference.md`

---

**Version**: 0.2.0 | **Last Updated**: January 2026
