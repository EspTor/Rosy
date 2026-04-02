# Agent System Specification

## Agent Anatomy (BODIES Framework)

### Brain

**Goal System**
- Hierarchical goals (life → long-term → short-term → tactical)
- Activation based on need states and context
- Priority weights influenced by personality

**Memory Store**
- Episodic: specific events with emotional valence
- Semantic: facts and beliefs about other agents, locations
- Procedural: skills and their proficiency levels
- Retrieval using recency + relevance scoring

**Personality Engine**
- OCEAN model: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism (all 0.0-1.0)
- Additional traits: Impulsivity, Risk tolerance, Social confidence, Ambition, Greed
- Personality influences goal selection, action evaluation, relationship formation

**Planning Module**
- Hierarchical task decomposition
- Precondition/effect checking
- Multi-step plan generation with re-planning on failure

### Body

**Location & Movement**
- Current (x, y) coordinates and location_id
- Movement speed (2-6 units/sec, varies by agent)
- Pathfinding via A* with collision avoidance
- Encumbrance from inventory affects speed

**Inventory**
- List of carried items with quantities, weight, quality
- Affects movement (heavy inventory = slower)
- Provides access to resources

**Physical State**
- Health: 0-100 (0 = dead)
- Energy: 0-100 (depletes with activity, restores with sleep)
- Hunger: 0-100 (increases over time, decreases with food)
- Happiness: -50 to +50 (affected by events, relationships)
- Stress: 0-100 (from work pressure, conflict, financial problems)

Needs create drive states that activate goals when thresholds crossed.

### Social Graph

**Relationships**
```
Relationship {
  agent_a, agent_b,
  type: friend|family|colleague|romantic|rival|stranger,
  trust: 0.0-1.0,
  affection: -1.0 to +1.0,
  familiarity: 0.0-1.0,
  last_interaction, interaction_count
}
```

**Social Roles**
- Family: parent, child, sibling
- Professional: employee, boss, freelancer
- Civic: taxpayer, voter, volunteer
- Social: friend, mentor, leader

**Reputation**
- Audience-specific (friends, coworkers, neighbors)
- Affects how others interact with agent
- Can be invoked to influence others

### Identity

- Agent ID (UUID, never changes)
- Name and appearance
- Backstory/origin
- Long-term values and beliefs
- Age (in simulation years)

## Agent Types (Templates)

1. **Worker**: Steady income, factory/office jobs, conventional lifestyle
2. **Artist**: Creative expression, bohemian, lower material focus
3. **Entrepreneur**: Independence, business ownership, risk-tolerant
4. **Student**: Learning focus, attends university, lower income
5. **Family Person**: Relationship-focused, prioritizes family time
6. **Socialite**: Networking, high extraversion, status-seeking
7. **Lone Wolf**: Minimal social interaction, self-sufficient
8. **Criminal**: Low empathy, risk-seeking, rule-breaking

## Decision Flow (Per Tick)

1. **Perception**: Query nearby agents, objects, resources within radius
2. **Memory Retrieval**: Get relevant experiences, relationship data, knowledge
3. **Goal Activation**: Calculate activation score for each goal based on needs and context
4. **Action Generation**: For top 3 goals, generate 3-5 possible actions each
5. **Action Evaluation**: Score based on expected benefit, cost, risk, social impact
6. **Action Selection**: Choose highest score with exploration randomness
7. **Execution**: Submit to engine for validation
8. **Update**: Modify goals, relationships, memories based on outcome

## Lifecycle

- **Birth/Spawn**: Initial state from template or random
- **Daily Routine**: Schedule-based with flexibility for goals/social
- **Aging**: 1 simulation year per X real days
- **Death**: From old age, health neglect, accidents, crime
- **Memory Persistence**: Survives agent death (for research) for 90 days

---

*Next: Interacti
