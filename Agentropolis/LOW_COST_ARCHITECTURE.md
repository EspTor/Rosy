# Agentropolis: Low-Cost Architecture

## Executive Summary

Run Agentropolis for **$0-10/month** using:
- Self-hosted infrastructure (Oracle Cloud Free Tier or local machine)
- Free/cheap LLM models via OpenRouter
- Rule-based agent brains (80% of decisions)
- Aggressive caching and optimization

Target: 100 agents with full functionality under $10/month.

---

## 1. Infrastructure: $0

### Oracle Cloud Free Tier (Recommended)

4× always-free VMs (up to 24 GB RAM total):
- VM 1: PostgreSQL (4 GB)
- VM 2: Redis + Simulation Engine (8 GB)
- VM 3: API + Agent Workers (8 GB)
- VM 4: Dashboard (4 GB)

Cost: $0 forever

### Local Machine

16+ GB RAM, 4+ core CPU, 100 GB SSD.
Cost: $0 if you already own it.

---

## 2. LLM: Hybrid Brains

**Rule-based**: 80% of decisions (movement, needs, work, shopping) - $0
**LLM-enhanced**: 20% (complex social) - $0-10/month

### Free Models on OpenRouter

- `microsoft/phi-3-mini-128k-instruct` - ~$0.0001/call, decent
- `mistralai/mixtral-8x7b-instruct` - good, some free tier
- `cognitivecomputations/dolphin-2.9-llama-3-8b` - good, free tier
- `openchat/openchat-7b` - OK, free

### Cost Optimization

1. **Rate limit**: 6 LLM calls/agent/hour (max)
2. **Cache**: 30-second TTL for similar situations
3. **Batch**: Pool 3-5 agents per conversation → 1 LLM call
4. **Minimal prompts**: ~50 tokens instead of 200+
5. **Free models first**: Stay within OpenRouter free limits

**Projected cost for 100 agents (10% LLM usage)**: $8-12/month

---

## 3. Self-Hosted Databases (Free)

**PostgreSQL 15**: State storage
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=agentropolis postgres:15-alpine
```

**Redis 7**: Cache + spatial index (GEO)
```bash
docker run -d -p 6379:6379 redis:7-alpine redis-server --maxmemory 512mb
```

Both run on separate VMs or same VM as engine. $0.

---

## 4. Simulation Engine: Python

**Why not Rust?** Python async handles 100 agents at 10 ticks/sec easily.

**Tech**:
- `asyncio` for tick loop
- `sqlalchemy` for ORM
- `httpx` for async OpenRouter calls
- `numpy` for spatial math (optional)

**ECS Architecture**:
Entity with components (Position, Body, Brain). Systems update each tick.

---

## 5. Agent Brain Implementation

### Rule-Based Core (No LLM)

```python
class RuleBrain:
    def decide(self, agent):
        if agent.hunger > 70: return Action("move_to", "restaurant")
        if agent.energy < 20: return Action("move_to", "home")
        if agent.money < 50: return Action("go_to_work")
        return Action("idle")
```

### LLM Enhancement (Rare)

```python
class HybridBrain:
    def decide(self, agent):
        # 90% rule-based
        if self.should_use_rules(agent):
            return self.rule_brain.decide(agent)
        
        # 10% LLM for social
        if self.can_use_llm(agent):
            return self.cached_llm_call(agent)
        
        return self.rule_brain.decide(agent)
```

---

## 6. OpenRouter Integration Pattern

**Minimal Prompt** (~50 tokens):
```
{name}|{job}|H{health}|E{energy}|${money}
Loc:{loc}
Friends_here:{count}
---
Choose: move_to:loc | talk:agent:topic | work | shop | rest | idle
Reason: <10 words
```

**Structured Response**:
`{"action": "talk", "target": "Bob", "topic": "weather", "reason": "polite"}`

---

## 7. Deployment Architecture

```
VM1: PostgreSQL 15
VM2: Redis 7 + Python Tick Engine
VM3: FastAPI server + LLM workers
VM4: Streamlit/React dashboard

All connected via internal network. API port 8000 exposed.
Dashboard port 3000 exposed.
```

---

## 8. Cost Monitoring

```python
BUDGET_LIMIT = 20.00  # USD/month

class CostMonitor:
    def record(self, tokens_in, tokens_out, cost_per_1k):
        cost = (tokens_in + tokens_out) / 1000 * cost_per_1k
        self.spend += cost
        if self.spend >= self.limit:
            self.disable_llm()  # Auto-disable
```

Dashboard shows live $/day. Alerts at 80% of budget.

---

## 9. Monthly Cost Projection

| Item | Cost |
|------|------|
| Oracle Cloud (4 VMs) | $0 |
| PostgreSQL + Redis | $0 |
| OpenRouter LLM (careful) | $8-12 |
| Domain (optional) | $0-1 |
| **Total** | **$8-13/month** |

**Zero-cost mode**: Disable LLM entirely → $0/month.

---

## 10. Implementation Timeline (16 Weeks)

**Phase 0**: Setup (2w) → VMs, Docker, DB schema
**Phase 1**: Engine (2w) → ECS, tick loop, rule-based agents
**Phase 2**: Town (2w) → Grid, locations, pathfinding
**Phase 3**: Economy (2w) → Jobs, market, transactions
**Phase 4**: Social (2w) → Relationships, conversations, groups
**Phase 5**: LLM (2w) → OpenRouter integration, socialite agents, caching
**Phase 6**: Polish (4w) → Dashboard, optimization, documentation

---

## 11. Key Decisions

1. Python > Rust (speed sufficient for 100 agents)
2. Self-hosted > Managed (cost $0 vs $300/month)
3. Hybrid brains > All-LLM (cost & control)
4. Free models > Paid (OpenRouter free tier)
5. Docker Compose > Kubernetes (simplicity)
6. Aggressive caching > Raw API calls (cost control)
7. Fallback mode > Hard dependency (resilience)
8. 100-agent target > 10,000 (reasonable scope)

---

## Conclusion

Agentropolis can be built and run for nearly free. Start with 100% rule-based (Phase 1-4), then sprinkle in LLM for 10% of agents (Phase 5). You get emergent social dynamics without the $500/month cloud bill.

**Next**: Read full details in this document, then start Phase 0.
