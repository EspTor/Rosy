# System Architecture (Low-Cost Version)

## High-Level Overview

```
┌─────────────────────────────────────────────┐
│         Dashboard (Streamlit/React)         │
└───────────────┬─────────────────────────────┘
                │ WebSocket / REST
                ▼
┌─────────────────────────────────────────────┐
│        API Server (FastAPI on VM 3)         │
│  • Agent registration                      │
│  • Observer queries                        │
│  • Webhook endpoint (optional)             │
│  • Cost monitoring                         │
└───────────────┬─────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────┐
│     Simulation Engine (async Python)        │
│  ┌─────────────┐  ┌─────────────┐        │
│  │ Tick Loop   │  │  Systems    │        │
│  │ (10/sec)    │  │  - Movement │        │
│  └─────────────┘  │  - Needs     │        │
│                   │  - Economy   │        │
│                   │  - Social    │        │
│                   └─────────────┘        │
└───────────────┬─────────────────────────────┘
                │
        ┌───────┼───────┐
        ▼       ▼       ▼
┌─────────┐ ┌──────┐ ┌──────┐
│PostgreSQL│ │ Redis│ │File │
│(VM 1)    │ │(VM 2)│ │Cache│
└─────────┘ └──────┘ └──────┘
```

## Key Changes from Original Spec

### 1. No Rust
- **Original**: Rust for engine performance
- **Reality**: Python async can handle 100 agents at 10 ticks/sec on one core
- **Why**: Development speed > perf for this scale. Optimize only if needed.

### 2. No Kubernetes
- **Original**: K8s for scaling
- **Reality**: Docker Compose on 4 VMs (or single machine)
- **Why**: Overkill for 100 agents, adds complexity

### 3. LLM Integration
- **Original**: Every agent calls LLM every tick
- **Reality**: 80% rule-based, 20% LLM only for social interactions
- **Implementation**: OpenRouter with caching, rate limiting, batching

### 4. Infrastructure
- **Original**: Cloud managed services (RDS, ElastiCache, etc.)
- **Reality**: Self-hosted on Oracle Cloud Free or local machine
- **Cost**: $0 vs $300+/month

---

## Core Components

### 1. Tick Engine (Python + asyncio)

Simulated code here.

### 2. Agent Brain: Hybrid

Rule-based core + LLM enhancement.
LLM calls: ~6/agent/hour for socialite agents.
Cost: ~$0.43/month per socialite agent.

### 3. Spatial Index: Redis GEO

Fast neighbor queries. O(log N) performance.

### 4. PostgreSQL Schema (Simplified)

Tables: agents, agent_profiles, relationships, events, transactions, locations.

---

## Data Flow

Tick → Perception → Brain (rule/LLM) → Validation → Execution → Persistence

---

## Performance

100 agents on 8GB VM: 10 ticks/sec, 50-80ms/tick, 2GB RAM, 30% CPU.

---

## What Got Removed for Cost

- ✗ Rust engine
- ✗ Kubernetes
- ✗ Managed cloud databases
- ✗ Expensive LLMs
- ✗ Vector database (only if needed)
- ✗ Microservices

**This architecture delivers 90% of the value for 5% of the cost.**
