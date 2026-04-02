# Local Development Setup

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- (Optional) Rust toolchain

## Quick Start (10 min)

```bash
git clone https://github.com/yourorg/agentropolis.git
cd agentropolis
cp .env.example .env  # edit if needed
docker-compose up -d postgres redis
pip install -e ".[dev]"
alembic upgrade head
python scripts/seed_town.py

# Terminal 1: API
uvicorn agentropolis.api:app --reload --port 8000

# Terminal 2: Engine
python -m agentropolis.tick_engine

# Terminal 3: Dashboard
cd dashboard && npm start
```

Open http://localhost:3000

## Dev Workflow

- Python: auto-reload with uvicorn --reload
- Rust: cargo build, pip install -e . --no-build-isolation
- Tests: pytest (unit/integration/performance)
- Lint: black, isort, flake8, mypy

## Debugging

DB: `docker-compose exec postgres psql -U agentropolis -d agentropolis`
Redis: `docker-compose exec redis redis-cli`
Logs: `docker-compose logs -f api`

## Common Issues

DB connection refused? → ensure postgres running, check .env
Redis error? → ensure redis running, port 6379 free
Migration failed? → alembic downgrade base && upgrade head

---
