#!/usr/bin/env bash
#
# start_agentropolis.sh - Prerequisites check + simulation launcher
# Usage:
#   bash start_agentropolis.sh          # start everything including simulation
#   bash start_agentropolis.sh --setup  # only run prerequisites, don't start sim
#
set -euo pipefail

PROJECT_DIR="$HOME/Documents/Obsidian Vault/Agentropolis"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python3"

cd "$PROJECT_DIR"

echo "=== Agentropolis Startup ==="
echo "Project: $PROJECT_DIR"
echo ""

# ---- 1. Verify virtual environment ----
echo "[1/5] Checking virtual environment..."
if [[ ! -f "$VENV_PYTHON" ]]; then
    echo "ERROR: Virtual environment not found at $VENV_PYTHON"
    echo "Run: python3 -m venv venv && venv/bin/pip install -e ."
    exit 1
fi
echo "  venv OK: $( "$VENV_PYTHON" --version 2>&1 )"

# ---- 2. Ensure DB and Redis are running ----
echo "[2/5] Checking database services..."

# Try docker compose v2 first, fall back to v1
compose_cmd=""
if docker compose version &>/dev/null; then
    compose_cmd="docker compose"
elif command -v docker-compose &>/dev/null; then
    compose_cmd="docker-compose"
else
    echo "WARNING: Neither 'docker compose' nor 'docker-compose' found. Skipping service check."
    echo "  Make sure PostgreSQL (port 5432) and Redis (port 6379) are running."
fi

if [[ -n "$compose_cmd" ]]; then
    # Check if containers are already running
    if docker ps --format '{{.Names}}' | grep -q "agentropolis_postgres" && \
       docker ps --format '{{.Names}}' | grep -q "agentropolis_redis"; then
        echo "  Services already running."
    else
        echo "  Starting services..."
        $compose_cmd up -d
    fi
fi

# Wait for PostgreSQL to become healthy
echo "  Waiting for PostgreSQL to be ready..."
for i in $(seq 1 12); do
    if "$VENV_PYTHON" -c "import asyncio,asyncpg; async def c(): conn=await asyncpg.connect(host='localhost',port=5432,user='agentropolis',password='changeme'); await conn.close(); asyncio.run(c())" &>/dev/null; then
        echo "  PostgreSQL is ready."
        break
    fi
    # Fallback: simple tcp check
    if echo | nc -z -w1 localhost 5432 2>/dev/null; then
        echo "  PostgreSQL port is open."
        break
    fi
    if [[ $i -eq 12 ]]; then
        echo "  WARNING: PostgreSQL did not become ready after 60s. Continuing anyway."
        break
    fi
    sleep 5
done

# ---- 3. Install / verify Python dependencies ----
echo "[3/5] Verifying Python dependencies..."
"$VENV_PYTHON" -c "import sqlalchemy; import asyncpg" 2>/dev/null && \
    echo "  Key dependencies OK." || {
        echo "  Installing dependencies..."
        "$VENV_PYTHON" -m pip install -e . -q
    }

# ---- 4. Create database tables (idempotent) ----
echo "[4/5] Ensuring database tables exist..."
"$VENV_PYTHON" scripts/create_tables.py 2>&1 || {
    echo "  WARNING: Table creation reported issues (may already exist). Continuing..."
}

# Seed data only if tables are empty (one-time setup)
AGENT_COUNT=$("$VENV_PYTHON" -c "
import asyncio
from agentropolis.database import async_engine
from sqlalchemy import text as sa_text, func
async def main():
    async with async_engine.connect() as conn:
        result = await conn.execute(sa_text('SELECT COUNT(*) FROM agents'))
        print(result.scalar())
asyncio.run(main())
" 2>/dev/null || echo "0")

if [[ "$AGENT_COUNT" == "0" ]]; then
    echo "  Database is empty - seeding initial town data..."
    "$VENV_PYTHON" scripts/seed_town.py 2>&1 || echo "  WARNING: Seeding had issues."
else
    echo "  Database already has $AGENT_COUNT agents - skipping seed."
fi

# ---- 5. Start simulation (unless --setup only) ----
if [[ "${1:-}" == "--setup" ]]; then
    echo ""
    echo "=== Setup complete! ==="
    echo "  Run: bash start_agentropolis.sh  (to start the simulation)"
    exit 0
fi

echo ""
echo "[5/5] Starting Agentropolis simulation..."
echo "  Press Ctrl+C to stop."
echo "================================"
exec "$VENV_PYTHON" run_simulation.py
