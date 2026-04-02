# API Specification

## Agent Connector API

### POST /agents/register
Register new agent brain. Returns agent_id, token, assigned_home.

### GET /agents/{agent_id}/tick
Provides perception: location, nearby agents/objects, inventory, physical state, active goals, memory summary.

### POST /agents/{agent_id}/decide
Submit chosen action. Engine validates and executes.

### POST /agents/{agent_id}/message
Send direct message to another agent.

## Observer API

### GET /observers/overview
Simulation status, active agents, last events.

### GET /agents
List/filter agents (by status, type, location).

### GET /agents/{agent_id}
Detailed agent info including relationships and life events.

### GET /locations/{location_id}
Location details, occupants, resources.

### GET /events
Search events by type, agent, location, time range.

### GET /economy/overview
Money supply, wealth distribution, unemployment, inflation.

### GET /economy/prices/{item}
Price history with volume.

### POST /observers/scenarios
Trigger scenarios (economic shock, natural disaster, etc.).

## Streaming (WebSockets)

Subscribe to: all_events, conversations, transactions, agent_updates.

## Admin API

Control: pause, resume, speed, reset, spawn/remove agents.

---
