# Scalability & Performance

## Targets

| Agents | Ticks/sec | Memory | Scale Phase |
|--------|-----------|--------|-------------|
| 100 | 10 | 2 GB | Phase 1 |
| 1,000 | 30 | 20 GB | Phase 2 |
| 10,000 | 100 | 200 GB | Phase 3 |

## Bottlenecks

- Agent brain network (LLM latency)
- Spatial queries (nearby agents)
- Pathfinding (A* computations)
- Memory retrieval (vector search)
- Database writes (transactions)

## Mitigations

1. Spatial partitioning (grid cells)
2. Tick parallelization (agent workers)
3. Brain decision caching
4. Incremental observer updates
5. Connection pooling (PgBouncer)
6. Read replicas for queries
7. Event batch writes
8. Lazy memory loading
9. Pathfinding caching

## Scaling Architecture

Phase 2: Vertical + light horizontal (read replicas, agent workers)
Phase 3: Full horizontal (microservices, zone-based partitioning)

---
