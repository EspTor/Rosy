# Agentropolis Project Summary

## What

Open-source simulation platform where AI agents live in a virtual town, interacting socially and economically.

## Why

- Study emergent multi-agent behavior
- Benchmark for AI coordination/alignment
- Create observable artificial societies
- Demonstrate AI concepts interactively

## How (Technical)

- Engine: Rust/C++ (performance)
- Brains: Python with pluggable backends (rule-based, LLMs)
- Persistence: PostgreSQL + Redis + Chroma
- API: FastAPI + WebSocket
- Dashboard: React
- Scale: 100-10,000+ agents

## Current Status

Phase 0: planning complete. All documentation in /docs.

## Next Steps

1. Build prototype core (tick engine, agent state)
2. Implement rule-based brain
3. Populate town with 10 agents
4. Build observer dashboard
5. Release Phase 1 (~4 months)

## Get Involved

GitHub: https://github.com/yourorg/agentropolis
