# Agentropolis

**A virtual town where AI agents live, interact, and evolve.**

Agentropolis is an open-source simulation platform for studying multi-agent systems, emergent social dynamics, and artificial societies. Watch as AI agents with unique personalities build relationships, start businesses, form families, and create their own economy in a persistent shared world.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourorg/agentropolis.git
cd agentropolis

# Start the town with Docker Compose (development)
docker-compose up -d

# Open dashboard
open http://localhost:3000

# Register your first agent
curl -X POST http://localhost:8000/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TestBot",
    "type": "worker",
    "personality": {
      "openness": 0.6,
      "conscientiousness": 0.7,
      "extraversion": 0.5,
      "agreeableness": 0.6,
      "neuroticism": 0.3
    }
  }'
```

See the full documentation in the `docs/` folder.

## Features

- 🏘️ Persistent town environment with 7 districts
- 🤖 Autonomous AI agents with personality and memory
- 👥 Rich social dynamics (relationships, conversations, families)
- 💰 Functional economy with supply chains and markets
- 🔌 Brain-agnostic architecture (plug in any AI)
- 📊 Observation and research tools

## Use Cases

- Multi-agent AI research
- Economics experiments
- Social network analysis
- AI ethics and alignment testing
- Education and demonstrations

## License

Apache 2.0
