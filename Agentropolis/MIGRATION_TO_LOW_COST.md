# Migration to Low-Cost Architecture

## What Changed

Original plan assumed:
- Rust engine (fast but complex)
- Kubernetes (heavy)
- Managed cloud services (expensive)
- LLM for all agents every tick (prohibitively expensive)

**Low-cost version**:
- Python engine (simpler, fast enough)
- Docker Compose on free VMs
- Self-hosted PostgreSQL + Redis
- 80% rule-based agents, LLM only for 10% social elite
- Hard cost controls and caching

---

## Document Updates

These planning documents have been **updated**:

1. **TECH_STACK.md** → Python/Docker/OpenRouter instead of Rust/K8s/GPT-4
2. **architecture/OVERVIEW.md** → Async Python, Redis GEO, simplified components
3. **agents/SPECIFICATION.md** → Hybrid brain, cost tables, 100-agent projections
4. **api/SPECIFICATION.md** → Simplified, observer-focused, optional external brains
5. **deployment/INFRASTRUCTURE.md** → Oracle Cloud Free, Docker Compose
6. **roadmap/PLAN.md** → 16 weeks (vs 12 months), $10/month budget

**New document created**:
7. **LOW_COST_ARCHITECTURE.md** → Comprehensive guide to low-cost approach

---

## Comparison Table

| Aspect | Original | Low-Cost |
|--------|----------|----------|
| Engine | Rust | Python asyncio |
| Scale Target | 10,000 agents | 100-500 agents |
| Infra | Kubernetes cluster | 4× free VMs or local |
| Databases | Managed services | Self-hosted |
| LLM | GPT-4/Claude every tick | OpenRouter free models, 10% agents |
| Monthly Cost | $200-500 | $0-10 |
| Timeline | 12 months | 16 weeks |
| Complexity | High | Low-Medium |

---

## What Stays the Same

- Core simulation concepts (tick, agents, locations, needs)
- Agent design (BODIES framework)
- Town structure (districts, zoning)
- Economy fundamentals (currency, production, markets)
- Social dynamics (relationships, groups)
- Data models (most tables remain similar)
- Security approach (still server-authoritative)
- Observer API (similar endpoints)
- Open source ethos

---

## Implementation Priority Shift

**Original order**:
1. Rust engine
2. Complex brain system
3. Scale to 1000
4. Add economics
5. Add social

**Low-cost order**:
1. **Rule-based simulation** (prove concept cheaply)
2. **Basic town + 50 agents** (simple economy)
3. **Social dynamics** (relationships, rule-based convos)
4. **LLM sprinkle** (only for socialite agents, after town works)
5. **Dashboard** (visualization)
6. **Optimize** (caching, performance)

Rationale: Get the town simulation working first with zero LLM cost. Then add LLM as polish, not core.

---

## Getting Started Now

1. **Read** `LOW_COST_ARCHITECTURE.md` for complete details
2. **Follow** `roadmap/PLAN.md` (16-week timeline)
3. **Use** `architecture/OVERVIEW.md` for technical design
4. **Reference** `agents/SPECIFICATION.md` for hybrid brain implementation
5. **Deploy** using `deployment/INFRASTRUCTURE.md` (Oracle Cloud Free or local)

---

## Cost Control Checklist

- [ ] Set BUDGET_HARD_LIMIT = $20/month in cost_monitor.py
- [ ] Implement LLM call rate limiting: MAX 6/agent/hour
- [ ] Use only free OpenRouter models (phi-3-mini, mixtral-8x7b, dolphin-2.9-llama-3-8b)
- [ ] Cache LLM responses with 30-second TTL in Redis
- [ ] Set up daily email alert at 80% budget usage
- [ ] Implement automatic LLM disable at 100%
- [ ] Monitor OpenRouter dashboard for rate limits
- [ ] Have fallback to 100% rule-based mode

---

## If You Exceed Budget

**Automatic responses**:
- 80% budget: Log warning, reduce LLM calls by 50% (only 5% of agents)
- 100% budget: Disable LLM entirely, switch to 100% rule-based
- System continues running (just less "intelligent" conversations)

**Manual override**:
- Increase budget limit (if willing to pay more)
- Switch to even cheaper models
- Reduce socialite agent count

---

## When to Scale Up

Once simulation is stable at 100 agents, consider:
1. Apply for Google Cloud research credits (~$5000) → switch to Vertex AI
2. Fine-tune small open model (7B) on your own data → better quality/cheaper
3. Add more Oracle Cloud VMs ($0.10/hour each beyond free tier)
4. Move to K8s if you need 1000+ agents

But **don't scale prematurely**. Prove the concept cheaply first.

---

## Questions?

The low-cost approach prioritizes **accessibility and learning** over raw scale. You can run Agentropolis on a laptop or free cloud tier, understand every component, and still observe emergent behavior.

If you later want to go bigger, you have a working foundation to optimize.
