# Security & Agent Identity

## Authentication

- **Agents**: JWT tokens with agent_id claim, expire after inactivity
- **Observers**: Separate tokens with read-only scope
- **Admins**: Restricted tokens with full access (logged)

## Authorization

Access control matrix:
- Agent: own state only, own memories
- Observer: all agents (metadata only), no memory content
- Researcher: all agents + memories (with consent)
- Developer/Admin: full access

## Simulation Integrity

Server-side validation of all actions:
- Resource conservation (no money/item creation)
- Movement validation (path exists, not blocked)
- Cooldown enforcement (prevent spamming)
- Tick ordering (no skipping ahead)

## Agent Sandboxing

Untrusted brain code runs in:
- WebAssembly runtime with syscall restrictions, or
- Docker container with: no network, read-only filesystem, 512MB RAM, 1s timeout

## Data Protection

- TLS 1.3 in transit
- Encrypted storage at rest
- Secrets in vault (not code)
- Audit logging for sensitive operations
- Rate limiting on APIs

## Incident Response

- Critical: <1 hour response
- High: 4 hours
- Medium: 24 hours
- Low: 1 week

---
