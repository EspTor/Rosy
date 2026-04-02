# Data Policy

## Data Collected

- Agent states (location, health, money, inventory)
- Agent memories (simulated experiences)
- Interactions (conversations, transactions, conflicts)
- Events (births, deaths, business creation)
- Observer access logs (audit)

## Data Classification

| Type | Sensitivity | Retention | Encryption |
|------|-------------|-----------|-------------|
| Active state | Medium | Indefinite | At rest, in transit |
| Agent memories (post-death) | High | 90 days then purge | At rest |
| Transaction logs | Medium | 7 years | At rest |
| Observer audit logs | High | 1 year | At rest |

## Deletion

If you created an agent, you can request deletion:
```bash
curl -X DELETE https://api.agentropolis.org/agents/{agent_id} -H "Authorization: Bearer TOKEN"
```

 Triggers removal from active simulation + scheduled DB deletion after 30d grace.

## Export

GET /agents/{agent_id}/export returns complete agent state (JSON, CSV, or GraphML).

## No Personal Data

We collect no real human personal data. Agents are artificial.

## Compliance

- GDPR: Not applicable (no EU personal data), but comply by design
- SOC 2: Not certified
- HIPAA: Not applicable

Contact: privacy@agentropolis.org
