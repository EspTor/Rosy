"""Quick verification that the package structure is correct."""

import sys
print("Testing Agentropolis package structure...")

try:
    import agentropolis
    print(f"✓ agentropolis v{agentropolis.__version__} imported")
except ImportError as e:
    print(f"✗ Failed to import agentropolis: {e}")
    sys.exit(1)

try:
    from agentropolis.config import config
    print(f"✓ config loaded: database_url={config.database_url[:50]}...")
except ImportError as e:
    print(f"✗ Failed to import config: {e}")
    sys.exit(1)

try:
    from agentropolis.database import Base, async_engine
    print("✓ database module imported")
except ImportError as e:
    print(f"✗ Failed to import database: {e}")
    sys.exit(1)

try:
    from agentropolis.models import Agent, Location, Relationship
    print("✓ models imported")
except ImportError as e:
    print(f"✗ Failed to import models: {e}")
    sys.exit(1)

print("\n✅ All basic imports successful!")
print("=" * 40)
print("Next steps:")
print("1. pip install -e '.[dev]'")
print("2. docker-compose up -d")
print("3. python scripts/seed_town.py")
print("4. pytest tests/")
