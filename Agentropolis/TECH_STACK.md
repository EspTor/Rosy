# Technology Stack

## Core Technologies

| Layer | Technology | Reason |
|-------|------------|--------|
| Simulation Engine | Rust (or C++) | Performance, safety, control |
| Agent Brains | Python | Flexibility, ML libraries |
| API | FastAPI | Auto docs, async, fast |
| Frontend | React + TypeScript | Modern, interactive |
| Database | PostgreSQL + TimescaleDB | Reliable, time-series |
| Cache | Redis Cluster | Sub-millisecond lookups |
| Vector DB | Chroma / Pinecone | Semantic memory search |
| Message Queue | NATS / Kafka | Async event streaming |
| Deployment | Docker + Kubernetes | Scalable, manageable |
| Monitoring | Prometheus + Grafana | Metrics, alerting |
| CI/CD | GitHub Actions | Integrated |

## Rationale

Rust for engine: deterministic, no GC, safe concurrency. Python for brains: easy ML integration. TypeScript for dashboard: type safety, React ecosystem.

---
