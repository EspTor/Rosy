# Task 1 Testing Guide

## Quick Quality Check (2 minutes)

Run the all-in-one test runner:

```bash
cd "/home/ubuntu/Documents/Obsidian Vault/Agentropolis"
python run_tests.py
```

This will:
1. ✅ Check all required files exist
2. ✅ Verify package imports
3. ✅ Validate configuration
4. ❓ Prompt: "Is docker-compose running?" → Type `y` if yes
5. ✅ Run pytest on all test files
6. ✅ Show pass/fail summary

---

## Manual Test Steps

### Step 1: Structural Validation

```bash
python test_verify.py
```

**Expected:**
```
✓ agentropolis v0.1.0 imported
✓ config loaded
✓ database module imported
✓ models imported
✅ All basic imports successful!
```

---

### Step 2: Database Connection

```bash
python -c "from agentropolis.database import test_connection; test_connection()"
```

**Expected:** `✓ Database connection OK`

**If fails:**
- Start Docker: `docker-compose up -d`
- Check `.env` file exists (copy from `.env.example`)
- Verify Postgres container is running: `docker ps`

---

### Step 3: Create Tables

```bash
python scripts/create_tables.py
```

**Expected:** `✅ Tables created successfully!`

**Verify manually:**
```bash
docker exec -it agentropolis-postgres psql -U agentropolis -d agentropolis -c "\\dt"
```

Should show:
```
               List of relations
 Schema |      Name      | Type  |  Owner   
--------+----------------+-------+----------
 public | agents         | table | agentropolis
 public | locations      | table | agentropolis
 public | relationships  | table | agentropolis
```

---

### Step 4: Seed Data

```bash
python scripts/seed_town.py
```

**Expected:**
```
✓ Created 5 locations
✓ Created 5 agents
✓ Updated location occupancy
```

**Verify count:**
```bash
docker exec -it agentropolis-postgres psql -U agentropolis -d agentropolis -c "SELECT COUNT(*) FROM agents;"
# Should return: 5

docker exec -it agentropolis-postgres psql -U agentropolis -d agentropolis -c "SELECT COUNT(*) FROM locations;"
# Should return: 5
```

---

### Step 5: Run Pytest Suite

```bash
pytest tests/ -v
```

**Expected tests:**
- `tests/test_config.py::test_default_config` ✅
- `tests/test_config.py::test_env_override` ✅
- `tests/test_database.py::test_sync_connection` ✅
- `tests/test_database.py::test_async_engine_creation` ✅
- `tests/test_database.py::test_init_db_creates_tables` ✅
- `tests/test_models.py::test_agent_creation` ✅
- `tests/test_models_integration.py::test_agent_location_relationship` ✅
- `tests/e2e/test_full_flow.py::test_full_pipeline` ✅

All should pass.

---

### Step 6: Performance Benchmarks (Optional)

```bash
python scripts/benchmark.py
```

**Targets for Low-Cost Architecture (Oracle Cloud Free Tier, 1 CPU):**
- Insert 1000 agents: < 5 seconds
- Location query: < 0.1 seconds
- Relationship query: < 0.1 seconds

**Sample good output:**
```
Inserted 1000 agents in 2.345s (426 agents/sec)
Queried 100 agents by location in 0.045678s
Fetched 2 relationships for one agent in 0.023456s
✅ Benchmarks complete!
```

If benchmarks are slow (>10s for 1000 inserts):
- Check Docker has enough RAM (≥2GB)
- Ensure `docker-compose.yml` has proper `shm_size: 256mb`
- Consider adding indexes (we already have some)

---

## Troubleshooting

### "No module named 'agentropolis'"

**Fix:**
```bash
pip install -e ".[dev]"
```

---

### "Connection refused" to Postgres

**Fix:**
```bash
docker-compose up -d
# Wait 5 seconds
docker-compose ps  # Should show both containers "Up"
```

---

### "permission denied for schema public"

**Fix:** Wrong database user. Check `.env`:
```
POSTGRES_USER=agentropolis
POSTGRES_PASSWORD=agentropolis
```

---

### "relation 'agents' does not exist"

**Fix:** You haven't created tables yet.
```bash
python scripts/create_tables.py
```

---

### Tests fail with "duplicate key value violates unique constraint"

**Fix:** Previous test run left data. Clean Docker volumes:
```bash
docker-compose down -v
docker-compose up -d
python scripts/create_tables.py
```

---

## Quality Scorecard

Check off each item:

### ✅ Structure (5 points)
- [ ] `agentropolis/` package is importable
- [ ] `models/`, `systems/`, `brains/` directories exist
- [ ] `scripts/` contains `seed_town.py` and `create_tables.py`
- [ ] `tests/` has `conftest.py`, unit tests, and e2e tests
- [ ] `pyproject.toml` has dependencies: sqlalchemy, asyncpg, pytest, redis

### ✅ Database (5 points)
- [ ] `docker-compose up -d` starts successfully
- [ ] `test_connection()` returns `True`
- [ ] Tables created by `init_db()` exist in Postgres
- [ ] Seed script creates 5 agents, 5 locations
- [ ] Foreign key constraints work (agent.location_id → location.id)

### ✅ Models (5 points)
- [ ] `Agent` has all fields: name, type, location_id, x/y, health, energy, hunger, happiness, money, is_active, is_llm_enabled, timestamps
- [ ] `Location` has services: provides_food, provides_sleep, provides_entertainment, provides_work, provides_healthcare
- [ ] `Relationship` has agent_a_id/agent_b_id composite PK, trust/affection/familiarity scores
- [ ] Model relationships load correctly (`agent.location`, `location.occupants`)
- [ ] `current_occupancy` updates manually

### ✅ Tests (5 points)
- [ ] `pytest tests/ -v` runs without errors
- [ ] Config tests pass (defaults + env override)
- [ ] Database tests pass (connection, table creation)
- [ ] Model tests pass (CRUD + relationships)
- [ ] E2E test passes (full pipeline)

### ✅ Performance (5 points)
- [ ] `benchmark.py` runs without crashing
- [ ] Insert 1000 agents < 5s
- [ ] Location query < 0.1s
- [ ] Relationship query < 0.1s
- [ ] No memory leaks after multiple runs

---

**Total: 25 points**

**Passing score: 20+ points**

If you score 20+ → Task 1 is **high quality** and ready for Task 2.  
If 15-19 → Minor issues, fix before proceeding.  
If <15 → Significant problems, revisit implementation.

---

## What "Quality" Means for Task 1

Task 1 is **infrastructure scaffolding**. Quality criteria:

1. **Correctness**: Models match specification (Agent, Location, Relationship)
2. **Completeness**: All required fields present, types correct
3. **Testability**: Tests can actually run and pass
4. **Performance**: Can handle 500 agents without lag (our target)
5. **Maintainability**: Code is clean, typed, documented

**Note:** Task 1 doesn't need "production-grade" perfection. It needs to:
- ✅ Import without errors
- ✅ Create tables in Postgres
- ✅ Seed sample data
- ✅ Run tests successfully
- ✅ Be ready for ECS framework in Task 2

---

## Next Steps After Verification

Once all tests pass, you're ready for **Task 2**:

```bash
# Your next task will be:
python run_next_phase.py  # (but just ask me to continue!)
```

Task 2 will add:
- `agentropolis/models/entity.py` (ECS entity)
- Component classes (Position, Body, Brain)
- `agentropolis/systems/` package
- `agentropolis/engine.py` (TickEngine)
- `agentropolis/brains/rule_brain.py` (Rule engine)
- `scripts/run_engine.py` (simulation runner)

**Still no LLM required!** Rule-based only. 🎯
