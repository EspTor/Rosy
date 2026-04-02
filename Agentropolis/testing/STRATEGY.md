# Testing Strategy

## Test Types

1. **Unit**: Individual functions (pytest, 80% coverage target)
2. **Integration**: Component interactions (test DB)
3. **E2E Simulation**: Full town runs (validate emergent outcomes)
4. **Property-Based**: Hypothesis tests for invariants
5. **Performance**: Benchmarks (tick duration, API latency)
6. **Chaos**: Fault injection (DB down, brain timeout)

## Test Data

Fixtures in tests/fixtures/: tiny_town.json, medium_town.json, economic_test.json

## CI/CD

GitHub Actions runs:
- Unit tests on every push
- Integration tests (with services)
- Performance regression check
- Security scanning (Snyk, Trivy)

## Load Testing

Locust for agent registration surge; k6 for observer API load.

---
