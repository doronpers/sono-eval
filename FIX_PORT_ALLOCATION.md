# Fix Port Allocation Issues

## Quick Diagnosis

Check which ports are in use:
```bash
# Check all Sono-Eval ports
lsof -i :8000  # API server
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :8088  # Superset

# Or on Linux
sudo netstat -tulpn | grep -E ':(8000|5432|6379|8088)'

# Or using Docker
docker ps | grep -E '8000|5432|6379|8088'
```

---

## Solution 1: Stop Conflicting Services

### Stop Sono-Eval if Already Running
```bash
# Stop all Sono-Eval containers
./launcher.sh stop

# Or manually
docker-compose down

# Verify ports are free
lsof -i :8000
```

### Stop Other Services Using Ports

**Port 8000 (API):**
```bash
# Find what's using port 8000
lsof -i :8000
# or
sudo lsof -i :8000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or if it's another Docker container
docker ps
docker stop <container-name>
```

**Port 5432 (PostgreSQL):**
```bash
# Check if local PostgreSQL is running
ps aux | grep postgres

# Stop local PostgreSQL (macOS)
brew services stop postgresql

# Stop local PostgreSQL (Linux)
sudo systemctl stop postgresql

# Or kill the process
sudo lsof -i :5432
kill -9 <PID>
```

**Port 6379 (Redis):**
```bash
# Check if local Redis is running
ps aux | grep redis

# Stop local Redis (macOS)
brew services stop redis

# Stop local Redis (Linux)
sudo systemctl stop redis

# Or kill the process
sudo lsof -i :6379
kill -9 <PID>
```

**Port 8088 (Superset):**
```bash
# Usually only Sono-Eval uses this, but check:
lsof -i :8088
kill -9 <PID>
```

---

## Solution 2: Change Ports in Docker Compose

Edit `docker-compose.yml` to use different ports:

```yaml
services:
  sono-eval:
    ports:
      - "9000:8000"  # Changed from 8000:8000
    # ... rest of config

  postgres:
    ports:
      - "5433:5432"  # Changed from 5432:5432

  redis:
    ports:
      - "6380:6379"  # Changed from 6379:6379

  superset:
    ports:
      - "8089:8088"  # Changed from 8088:8088
```

Then update your `.env` file:
```bash
API_PORT=9000
```

**New access points:**
- API: http://localhost:9000
- API Docs: http://localhost:9000/docs
- Mobile UI: http://localhost:9000/mobile/
- Superset: http://localhost:8089

---

## Solution 3: Use Docker Port Mapping (Recommended)

Keep internal ports the same, only change external ports:

```yaml
services:
  sono-eval:
    ports:
      - "8001:8000"  # External:Internal
    # Internal port stays 8000, external is 8001

  postgres:
    ports:
      - "5433:5432"  # External:Internal
    # Internal stays 5432, external is 5433
```

This way:
- Containers still communicate on standard ports internally
- You access from host on different ports
- No code changes needed

---

## Solution 4: Remove Port Exposing (Development Only)

If you don't need external access to some services:

```yaml
services:
  postgres:
    # Remove ports section entirely
    # Only accessible from other containers

  redis:
    # Remove ports section entirely
    # Only accessible from other containers
```

Keep ports for:
- `sono-eval` (you need API access)
- `superset` (you need dashboard access)

---

## Quick Fix Script

Create a script to check and free ports:

```bash
#!/bin/bash
# fix-ports.sh

echo "Checking Sono-Eval ports..."

PORTS=(8000 5432 6379 8088)
FOUND=false

for port in "${PORTS[@]}"; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "⚠️  Port $port is in use"
        PROCESS=$(lsof -ti :$port)
        echo "   Process ID: $PROCESS"
        read -p "   Kill process $PROCESS? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill -9 $PROCESS
            echo "   ✅ Killed process $PROCESS"
            FOUND=true
        fi
    else
        echo "✅ Port $port is free"
    fi
done

if [ "$FOUND" = true ]; then
    echo ""
    echo "Ports freed! You can now run: ./launcher.sh start"
else
    echo ""
    echo "All ports are free!"
fi
```

---

## Verify Ports Are Free

After fixing, verify:
```bash
# Check all ports
for port in 8000 5432 6379 8088; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "❌ Port $port still in use"
    else
        echo "✅ Port $port is free"
    fi
done
```

---

## Common Scenarios

### Scenario 1: Previous Sono-Eval Still Running
```bash
# Stop all Sono-Eval containers
docker-compose down

# Remove stopped containers
docker-compose rm -f

# Verify
docker ps -a | grep sono-eval
```

### Scenario 2: Local PostgreSQL Running
```bash
# macOS
brew services list | grep postgresql
brew services stop postgresql

# Linux
sudo systemctl status postgresql
sudo systemctl stop postgresql

# Or use different port in docker-compose.yml
```

### Scenario 3: Local Redis Running
```bash
# macOS
brew services list | grep redis
brew services stop redis

# Linux
sudo systemctl status redis
sudo systemctl stop redis

# Or use different port in docker-compose.yml
```

### Scenario 4: Another Application Using Ports
```bash
# Find what's using the port
sudo lsof -i :8000

# Check if it's safe to stop
# If yes, kill it
kill -9 <PID>

# If no, change Sono-Eval ports instead
```

---

## After Fixing Ports

1. **Verify ports are free:**
   ```bash
   lsof -i :8000 -i :5432 -i :6379 -i :8088
   ```

2. **Start services:**
   ```bash
   ./launcher.sh start
   ```

3. **Check status:**
   ```bash
   ./launcher.sh status
   docker-compose ps
   ```

4. **Test access:**
   ```bash
   curl http://localhost:8000/health
   ```

---

## Prevention

To avoid port conflicts in the future:

1. **Always stop Sono-Eval properly:**
   ```bash
   ./launcher.sh stop
   # or
   docker-compose down
   ```

2. **Check before starting:**
   ```bash
   # Quick check
   lsof -i :8000 || echo "Port 8000 is free"
   ```

3. **Use different ports for development:**
   - Keep production ports (8000, 5432, etc.) free
   - Use 9000+ range for development

---

## Still Having Issues?

If ports are still showing as in use after stopping everything:

1. **Check Docker containers:**
   ```bash
   docker ps -a
   docker rm -f $(docker ps -a -q)  # Remove all containers (careful!)
   ```

2. **Check Docker networks:**
   ```bash
   docker network ls
   docker network prune
   ```

3. **Restart Docker daemon:**
   ```bash
   # macOS (Docker Desktop)
   # Quit and restart Docker Desktop

   # Linux
   sudo systemctl restart docker
   ```

4. **Nuclear option (removes everything):**
   ```bash
   docker-compose down -v  # Removes volumes too
   docker system prune -a  # Removes all unused Docker resources
   ```

---

**Quick Command Reference:**
```bash
# Check ports
lsof -i :8000

# Stop Sono-Eval
./launcher.sh stop

# Stop local PostgreSQL (macOS)
brew services stop postgresql

# Stop local Redis (macOS)
brew services stop redis

# Change ports in docker-compose.yml
# Then restart
./launcher.sh start
```
