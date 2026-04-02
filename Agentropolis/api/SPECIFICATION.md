# API Specification (Low-Cost)

## Agent Connector API (for external brains - optional)

If you want to connect custom brains (e.g., running your own LLM locally):

### POST /agents/register
Register new agent (if not using built-in brains).

### GET /agents/{agent_id}/tick
Polling mode: Get current perception.

### POST /agents/{agent_id}/decide
Submit chosen action.

### POST /agents/{agent_id}/message
Send direct message.

**Note**: For low-cost setup, most agents are built-in rule-based or use OpenRouter directly from engine. External agent connectors rarely needed.

## Observer API

### GET /observers/overview
Status, active agents count, last events.

### GET /agents
List/filter (by type, location, status).

### GET /agents/{agent_id}
Full agent state + relationships + recent events.

### GET /locations/{location_id}
Occupants, resources, properties.

### GET /events
Filter by tick range, agent, type.

### GET /economy/overview
Money supply, unemployment rate, business count.

### GET /economy/prices/{item}
Price history.

## Streaming

WebSocket at /ws for real-time updates:
- Subscribe to all_events, agent_updates, conversations
- Simple JSON protocol

## Admin API

- POST /admin/pause
- POST /admin/resume
- POST /admin/spawn_agent (for testing)
- POST /admin/trigger_event (scenario)
- GET /admin/stats (performance)

---

**All endpoints authenticate with JWT. Rate limits apply to prevent abuse.**
