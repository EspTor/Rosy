# Development Roadmap (Low-Cost, 16 Weeks)

## Phase 0: Setup & Foundations (Weeks 1-2)

**Week 1:**
- Day 1-2: Set up Oracle Cloud VMs (or local Docker)
- Day 3-4: Database schema + migrations
- Day 5: Basic Python project structure (asyncio, logging, config)
- Day 6-7: GitHub repo, CI/CD setup

**Week 2:**
- Day 1-2: ECS framework implementation
- Day 3-4: Tick engine with 10/sec target
- Day 5-7: Unit tests for ECS, first integration test with 1 agent

**Deliverable**: Working tick engine that can run 1 agent for 1000 ticks without crashing.

---

## Phase 1: Rule-Based Agents & Town (Weeks 3-6)

**Week 3: Town Grid**
- 1000×1000 coordinate system
- 50 locations (homes, shops, workplaces)
- Pathfinding (A* algorithm)
- Spatial index (Redis GEO)

**Week 4: Agent State & Needs**
- Physical state (health, energy, hunger, happiness)
- Inventory system
- Need-driven goal activation
- Movement with collision avoidance

**Week 5: Rule-Based Brains**
- Need hierarchy implementation
- Priority rule system (10 rules)
- Simple schedules (work 9-5, sleep 00-06)
- Job system with workplaces

**Week 6: Economy Basics**
- Currency system
- Transactions (buy/sell)
- Basic market with fixed prices
- Agent earning/spending

**Deliverable**: 50 rule-based agents living, working, shopping in virtual town.

---

## Phase 2: Social Dynamics (Weeks 7-10)

**Week 7: Relationships**
- Relationship model (trust, affection, familiarity)
- Interaction history tracking
- Relationship decay/growth
- Friend/family/colleague types

**Week 8: Simple Conversations**
- Rule-based dialog system
- Greetings, small talk
- Gossip propagation
- Social network visualization

**Week 9: Groups & Events**
- Business creation (agent-owned)
- Event system (parties, festivals)
- Group activities
- Memory system (episodic storage)

**Week 10: Testing & Balance**
- Run simulation for 1000 virtual days
- Observe emergent relationships
- Tune rule parameters for interesting behavior
- Fix bugs, improve performance

**Deliverable**: Agents forming friendships, working together, some becoming entrepreneurs.

---

## Phase 3: LLM Integration (Weeks 11-12)

**Week 11: OpenRouter Integration**
- HTTP client with retries
- Prompt engineering (minimize tokens)
- Response parsing (structured JSON)
- Caching layer (Redis, 30s TTL)
- Rate limiting (6 calls/agent/hour)

**Week 12: Socialite Agents**
- Create "Socialite" agent type (10% of population)
- LLM only for conversation decisions
- Conversation pooling (multi-agent)
- Cost monitoring dashboard integration
- Fallback to rule-based if budget exceeded

**Deliverable**: 5 socialite agents having LLM-driven conversations, total cost <$1/day.

---

## Phase 4: Dashboard & Polish (Weeks 13-14)

**Week 13: Dashboard**
- React or Streamlit frontend
- Real-time agent positions on map
- Agent detail panels
- Event timeline
- Economy overview (charts)
- Cost monitoring display

**Week 14: Performance & Testing**
- Profiling, optimize hot paths
- Increase agent count to 100
- Stress test tick rate
- Full system integration tests
- Documentation finalization

**Deliverable**: Fully functional demo with 100 agents, observer dashboard, ready for demo.

---

## Phase 5: Demo & Release (Weeks 15-16)

**Week 15: Scenario Scripts**
- 3 interesting scenarios:
  1. Economic shock (store closes)
  2. New agent arrival (celebrity)
  3. Crime event (theft)
- Record simulation videos
- Generate analytics report

**Week 16: Documentation & Launch**
- User guide
- Developer quickstart
- Architecture deep-dive
- Video walkthrough
- GitHub release v0.1.0
- Social media announcement

**Deliverable**: Public GitHub release, demo video, documentation complete.

---

## Timeline Summary

| Phase | Weeks | Agents | LLM | Status |
|-------|-------|--------|-----|--------|
| 0: Setup | 2 | 0-1 | No | Foundation |
| 1: Rule-Based | 4 | 50 | No | Core simulation |
| 2: Social | 4 | 50 | Rule-based only | Emergent dynamics |
| 3: LLM Integration | 2 | 50-100 | 10% agents | Intelligence sprinkle |
| 4: Polish | 2 | 100 | Limited | Ready for demo |
| 5: Release | 2 | 100 | Live | Public launch |

**Total**: 16 weeks part-time (8-12 hours/week)

**Monetary Cost**: $0-5 (domain name, maybe)

---

## Milestones

- **M1** (Week 2): Engine runs, tick loop works
- **M2** (Week 6): 50 agents in town, economy functional
- **M3** (Week 10): Social dynamics observed
- **M4** (Week 12): LLM integration online, costs monitored
- **M5** (Week 14): Dashboard complete, 100 agents
- **M6** (Week 16): Public release

---

## Risk Mitigation

- **If Python too slow**: Profile bottlenecks, optimize, or upgrade VM CPU
- **If LLM costs exceed**: Lower rate limits, use cheaper models, increase rule-based
- **If Oracle Cloud issues**: Switch to local machine or other free tier
- **If lost motivation**: Smaller scope (fewer agents, simpler economy)

---

## Success Criteria (Post-MVP)

- 100 agents running for 1000 virtual days without crashes
- At least one interesting social phenomenon observed (e.g., friendship clusters, economic cycles)
- LLM contribution < $10 for entire demo month
- Documentation complete enough for contributor to join
- GitHub stars: 50+, forks: 10+

---
