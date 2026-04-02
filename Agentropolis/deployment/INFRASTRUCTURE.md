# Deployment & Infrastructure

## Options

- Cloud-native (AWS/GCP/Azure): EKS, RDS, ElastiCache, S3
- Self-hosted (VPS): Docker Compose or K8s on bare metal
- All-in-one: Single server for development

## Production Steps

1. Infrastructure provisioning (Terraform or manual)
2. Database migrations (alembic upgrade head)
3. Seed data (resource types, locations)
4. Build/push Docker images
5. Deploy K8s manifests
6. Configure TLS (cert-manager + Let's Encrypt)
7. Setup monitoring (Prometheus + Grafana)
8. Configure backups

## Health Checks

/health endpoint returns status of database, redis, tick engine.

## Backup Strategy

- PostgreSQL: Daily full + continuous WAL
- Redis: AOF hourly
- Snapshots: Every 10k ticks to S3

---
