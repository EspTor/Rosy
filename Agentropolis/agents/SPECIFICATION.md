# Agent System Specification (Low-Cost Version)

## Agent Anatomy (BODIES Framework)

### Brain (Hybrid: Rule + LLM)

**Goal System**
- Hierarchical goals: survival → social → economic → self-actualization
- Rule-based activation (if hunger > 70 → eat)
- LLM only for complex social decisions (once per 10 min max)

**Memory Store**
- Episodic: Recent events (last 50 ticks) stored in PostgreSQL
- Semantic: Facts about other agents (cached in Redis)
- **No vector search initially** (saves cost/complexity)
- Retrieval by recency and relationship strength

**Personality Engine** (OCEAN + traits)
- OCEAN model: 5 traits, 0.0-1.0
- Additional: Impulsivity, Risk tolerance, Social confidence
- Personality influences rule weights and LLM prompts

**Planning Module**
- **Rule-based planner**: If need=food and location has restaurant → move_to(restaurant)
- **LLM planner** (rare): For creative goals only, 1% of agents use this

---

### Body

**Location & Movement**
- Position (x, y) in 1000×1000 grid
- Movement speed: 2-4 units/sec (varies by age/fitness)
- A* pathfinding on road network (precomputed)
- Collision: Simple separation force (radius 1.5)

**Inventory**
- Limited to 10 items, weight affects speed
- Money, food, goods, keys

**Physical State** (0-100 scale, except happiness -50 to +50)
- Health: decreases from hunger, illness, injury
- Energy: depletes with activity, restores with sleep
- Hunger: increases ~1 per tick, decreases with food
- Happiness: affected by goal achievement, relationships, events
- Stress: from work pressure, conflict, finances

**Needs Hierarchy** (drives goals)
```
Critical (override): health<10, hunger>90, energy<10
High: hunger 50-90, energy 20-50, happiness<-20
Normal: hunger<50, energy>50, happiness 0-50
```

---

### Social Graph

**Relationships**
```
Relationship:
  agent_a, agent_b
  type: friend|family|colleague|romantic|rival|stranger
  trust: 0.0-1.0 (transactions, secrets)
  affection: -1.0 to +1.0 (liking)
  familiarity: 0.0-1.0 (how well known)
  interaction_count
  last_interaction_tick
```

**Social Roles**
- Family: parent, child, sibling (from relationships)
- Professional: employee, boss, freelancer
- Civic: taxpayer, resident

**Reputation**
- Per-agent audience (each agent has opinion of you)
- Derived from interactions, transactions, gossip

---

### Identity

- Agent ID (UUID)
- Name, age, appearance
- Origin story (randomly generated)
- Occupation/job
- Values (derived from personality)
- Birth tick, death tick (if applicable)

---

## Agent Types (Rule-Heavy Templates)

| Type | LLM % | Description | Typical Routine |
|------|-------|-------------|-----------------|
| **Worker** | 0% | Factory/office job | Home → Work → Shop → Home |
| **Socialite** | 10% | Party person, networker | Various locations, LLM for conversations |
| **Artist** | 5% | Creative, bohemian | Home → Cafe → Park → Events |
| **Student** | 0% | Young, learning | Home → University → Library |
| **Family Person** | 0% | Relationship-focused | Family activities, predictable |
| **Shopkeeper** | 0% | Runs business | At shop most of day |
| **Criminal** | 5% | Rule-breaker | Strategic theft, needs LLM for planning |

**Distribution in 100-agent town**:
- Workers: 35
- Socialites: 10
- Artists: 5
- Students: 10
- Family: 20
- Shopkeepers: 10
- Criminals: 5
- Others: 5

---

## Decision Flow (Per Tick)

```
1. PERCEPTION (async, cached)
   - Get nearby agents (Redis GEO, 50 unit radius)
   - Get location resources (Postgres cache)
   - Get relationship summaries (cached)
   - Read own state (needs, inventory)

2. MEMORY RETRIEVAL
   - Get last 5 interactions with nearby agents
   - Get recent events affecting this agent
   - Retrieve from Redis cache first

3. GOAL ACTIVATION
   - Evaluate need thresholds (hunger > 70 → eat)
   - Apply rule weights from personality
   - Select top 3 active goals

4. ACTION GENERATION
   - For rule-based goals: generate template actions
   - For social goals: if socialite AND co-located agents present → queue LLM call (async, not immediate)
   - Otherwise: use rule-based social actions

5. ACTION SELECTION
   - Rule-based: first high-priority action
   - LLM-based: when response arrives (may be previous tick), apply if still valid

6. EXECUTION
   - Submit to engine for validation
   - If invalid: log, fallback to idle
   - If valid: update state, create events

7. LEARNING (async)
   - Update relationships based on interaction outcome
   - Store episodic memory (every 10 ticks)
   - Update need levels
```

---

## Tick-by-Tick Example: Socialite Agent

**Tick 1-9**: Rule-based movement, work, eat. No LLM called.

**Tick 10**: At cafe, other agents present. LLM call queued.
- Prompt: "Alice, 28, socialite, at cafe. Bob and Carol here. Mood: happy. Choose action."
- Response: `{"action": "talk_to", "target": "Bob", "topic": "weekend_plans", "reason": "be_social"}`
- Cost: ~$0.0001, 60 tokens

**Tick 11-19**: Continue rule-based. Cached if same situation.

**Tick 20**: At bar, different agents → another LLM call.

**Total**: 2 LLM calls per 20 ticks (10% frequency).

---

## Lifecycle

- **Spawn**: Initial state from template + random variations
- **Daily**: Tick-based updates, needs cycle, work schedule
- **Aging**: 1 simulation year per 30 real days (configurable)
- **Death**: When health reaches 0 (unrecovered) or age 80+ natural causes
- **Respawn**: After death, optionally spawn new agent with fresh identity

---

## Cost-Saving Measures

1. **Rule-based for 90% of agents**: Only Socialite (10%) and Criminal (5%) use LLM
2. **Infrequent LLM**: Max 6 calls/agent/hour
3. **Prompt minimization**: ~50 tokens per call (vs 200 typical)
4. **Response caching**: Same situation → reuse cached response
5. **Batch conversations**: Multiple agents in same location → one LLM call generates multi-party chat
6. **Free models**: Use OpenRouter free tier (Mixtral, Dolphin, Gemma)
7. **Fallback**: If rate-limited → rule-based social instead

---

## Expected Cost for 100 Agents

| Agent Type | Count | LLM calls/day | Cost/day | Cost/month |
|------------|-------|---------------|----------|------------|
| Worker | 35 | 0 | $0.00 | $0.00 |
| Socialite | 10 | 1440 | $0.14 | $4.32 |
| Artist | 5 | 720 | $0.07 | $2.16 |
| Student | 10 | 0 | $0.00 | $0.00 |
| Family | 20 | 0 | $0.00 | $0.00 |
| Shopkeeper | 10 | 0 | $0.00 | $0.00 |
| Criminal | 5 | 720 | $0.07 | $2.16 |
| Other | 5 | 0 | $0.00 | $0.00 |
| **Total** | **100** | **2880** | **$0.28** | **$8.64** |

**Note**: At phi-3-mini cost (~$0.0001/call) = $8.64/month.

**Buffer**: With higher rate limits or slightly larger prompts: $10-15/month max.

---

## Implementation Priority

1. Rule-based brain (all agent types) - Week 4
2. Needs system - Week 4
3. Relationship system - Week 7
4. LLM brain (Socialite only) - Week 11
5. Cost monitoring - Week 11
6. Optimization (caching, batching) - Week 12

---

**Key Insight**: The emergent behavior comes from **many simple agents interacting**, not from each agent being super-intelligent. Rule-based agents create rich dynamics at the population level. LLM just adds spice for a few elite agents.
