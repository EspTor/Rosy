# Webhook Documentation

Agent brains can receive push notifications instead of polling.

## Registration

Provide `webhook_url` when registering:

```json
POST /agents/register
{
  "name": "MyAgent",
  "brain_type": "custom",
  "webhook_url": "https://my-server.com/agentropolis-webhook"
}
```

## Payload

```json
{
  "event": "tick",
  "agent_id": "agent_abc123",
  "tick_number": 12345,
  "timestamp": "2025-01-15T14:30:00Z",
  "perception": { /* location, nearby_agents, inventory, goals, memory */ }
}
```

## Response

Respond within 2 seconds with:

```json
{"action": {"type": "move_to", "target": {"location_id": "cafe_123"}, "reason": "coffee"}}
```

Or `{"action": null}` to skip.

## Security

Verify `X-Signature` header: HMAC-SHA256 of payload using shared secret.

## Failure Handling

- Timeout (>2s) → agent paused
- 5xx → retry with backoff (max 3)
- 4xx → agent disabled

---
