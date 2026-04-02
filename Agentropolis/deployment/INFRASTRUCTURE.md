# Deployment Infrastructure (Low-Cost)

## Option 1: Oracle Cloud Free (Recommended)

**4 VMs (all always-free):**

| VM | Purpose | RAM | OS |
|----|---------|-----|-----|
| 1 | PostgreSQL | 4 GB | Ubuntu 22.04 |
| 2 | Redis + Simulation Engine | 8 GB | Ubuntu 22.04 |
| 3 | API + Agent Workers | 8 GB | Ubuntu 22.04 |
| 4 | Dashboard + Monitoring | 4 GB | Ubuntu 22.04 |

**Setup**:
1. Create 4 A1 VMs (always-free)
2. Install Docker on each
3. Configure networking (internal VCN)
4. Deploy services via docker-compose (see below)
5. Set up SSH keys, firewall

**Cost**: $0 forever

---

## Option 2: Single Machine (Local)

If you have a decent laptop/desktop:
- Run everything on one machine with Docker Compose
- 16 GB RAM minimum
- All services in separate containers
- Access via localhost

**Cost**: $0

---

## Docker Compose (Simplified)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: agentropolis
      POSTGRES_DB: agentropolis
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 512mb
    volumes:
      - redis_data:/data
    ports: ["6379:6379"]

  engine:
    build: ./docker/engine
    depends_on: [postgres, redis]
    environment:
      DATABASE_URL: postgresql://agentropolis:agentropolis@postgres/agentropolis
      REDIS_URL: redis://redis:6379/0
    # No ports exposed - internal only

  api:
    build: ./docker/api
    depends_on: [postgres, redis, engine]
    environment:
      DATABASE_URL: postgresql://agentropolis:agentropolis@postgres/agentropolis
      REDIS_URL: redis://redis:6379/0
    ports: ["8000:8000"]

  dashboard:
    build: ./docker/dashboard
    depends_on: [api]
    ports: ["3000:3000"]

volumes:
  postgres_data:
  redis_data:
```

---

## Multi-VM Deployment (Split)

If using 4 VMs, split docker-compose services:

**VM 1** (postgres): postgres service only
**VM 2** (engine): redis + engine services
**VM 3** (api): api service only
**VM 4** (dashboard): dashboard service only

Configure networking so API can reach DB on internal IPs.

---

## Initial Setup Steps

1. Provision VMs
2. Install Docker, Docker Compose on all
3. Clone repository to all VMs
4. Copy .env.example to .env with correct DB/Redis hostnames
5. Run initial DB migrations
6. Seed town data
7. Start services: `docker-compose up -d`
8. Verify: `curl http://api-vm:8000/health`
9. Open dashboard: http://dashboard-vm:3000

---

## Backups

**PostgreSQL**:每日 dump to object storage (Oracle Cloud Object Storage free tier)
```bash
docker exec postgres pg_dump -U agentropolis agentropolis > backup_$(date +%F).sql
```

**Redis**: RDB snapshots stored to same volume, copy daily.

---

## Monitoring

- Prometheus scrapes /metrics from API and engine
- Grafana dashboard for costs, performance, agent counts
- Alerts on high LLM spend, tick duration >100ms

---

## CI/CD

GitHub Actions:
- On push to main: build Docker images, push to GitHub Container Registry
- (Optional) Deploy to VMs via SSH

Simple and free.

---

## Cost Monitoring

LLM spend tracked in database. Dashboard shows live $/day.
Email alert at 80% of monthly budget. Auto-disable at 100%.

---
