# Contributing to Agentropolis

Thank you for considering contributing!

## Ways to Contribute

- 🐛 Report bugs (with reproduction steps)
- 💡 Suggest features (discuss first in GitHub Discussions)
- 📖 Improve documentation
- 🧪 Write tests
- 🔧 Submit pull requests

## Getting Started

```bash
git clone https://github.com/yourorg/agentropolis.git
cd agentropolis
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
docker-compose up postgres redis
alembic upgrade head
uvicorn agentropolis.api:app --reload
```

## Development Workflow

1. Check existing issues
2. Discuss major features first
3. Branch from main
4. Write tests (TDD encouraged)
5. Follow style: Black, isort, flake8
6. Commit often with clear messages
7. Update documentation
8. Ensure CI passes before PR

## PR Process

- Fill PR template with description, motivation, test plan
- At least one review from core team
- No merge conflicts
- Squash commits
- Merge after approvals + green CI

## Code Style (Python)

- Black (line length 88)
- isort (black profile)
- flake8
- Type hints for public functions
- Google-style docstrings

## Commit Messages

Conventional Commits: `feat(agents): add personality traits`, `fix(economy): prevent negative balance`

---

Questions? GitHub Discussions or Discord.
