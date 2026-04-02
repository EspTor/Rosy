# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Observer Interface                      │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                Town Simulation Engine                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐ │
│  │   Physics   │  │  Time Step  │  │  Event Queue    │ │
│  │  Simulator  │  │  Controller │  │  (async actions) │ │
│  └─────────────┘  └─────────────┘  └──────────────────┘ │
└─────────────┬───────────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌──────┐ ┌──────┐ ┌──────┐
│Agent │ │Agent │ │Agent │ │ ...
└──────┘ └──────┘ └──────┘
```

## Core Components

### 1. Town Simulation Engine
- Entity-Component-System (ECS) architecture
- Spatial partitioning for efficient queries
- Deterministic tick progression
- Coordinates agent lifecycle

### 2. Agent Architecture (BODIES)

**Brain**: Goal system, memory store, personality engine, planning module
**Body**: Location, inventory, physical state (health, energy, hunger, happiness)
**Social Graph**: Relationships, social roles, reputation
**Identity**: Persistent ID, name, appearance, backstory, values

### 3. Town Map & Environment
- 1000×1000 grid with 7 districts
- Location types: residential, commercial, industrial, civic, recreational
- Resource distribution (natural, commercial, social)
- Pathfinding with A* on navigation mesh
- Daily, weekly, seasonal cycles

### 4. Interaction System
- Direct communication (conversations)
- Economic transactions (buy/sell/gift)
- Collaborative actions (joint tasks)
- Conflict and competition
- Social relationship development
- Information spread and gossip
- Group formation (families, businesses, clubs)

### 5. Economy System
- Currency and banking
- Jobs and labor market
- Business operations and production chains
- Dynamic pricing (supply/demand)
- Property ownership
- Taxation and government budget

### 6. Persistence Layer
- PostgreSQL for structured state
- Redis for hot cache and spatial index
- Chroma/Pinecone for vector memories (semantic retrieval)
- TimescaleDB for time-series event logs
- Snapshot system for fast restart

### 7. Observer API & Dashboard
- REST API for querying state
- WebSocket for real-time updates
- Web dashboard with map visualization
- Event timeline and analytics
- Export capabilities

## Technology Stack

- **Core Engine**: Rust or C++ (performance-critical)
- **Agent Brains**: Python (flexibility, ML libraries)
- **API**: FastAPI (async, auto-docs)
- **Frontend**: React + TypeScript
- **Database**: PostgreSQL + TimescaleDB
- **Cache**: Redis Cluster
- **Vector DB**: Chroma or Pinecone
- **Message Queue**: NATS or Kafka
- **Deployment**: Docker + Kubernetes
- **Monitoring**: Prometheus + Grafana

## Key Design Decisions

1. **Server-authoritative**: Engine validates all actions
2. **Deterministic**: Reproducible simulations with fixed seed
3. **Brain-agnostic**: Support multiple AI backends
4. **Observable**: Everything logged for analysis
5. **Extensible**: Plugin architecture for new features

---

*Next: Agent specifications in agents/SPECIFICATION.md*
