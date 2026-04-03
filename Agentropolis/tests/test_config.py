"""Configuration validation tests."""
import os
import pytest
from agentropolis.config import Config, config

def test_config_defaults():
    """Test default configuration values."""
    assert config.database_url is not None
    assert "agentropolis" in config.database_url or "localhost" in config.database_url
    assert config.secret_key is None
    assert config.debug is False

def test_config_env_override(monkeypatch):
    """Test environment variable overrides."""
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/testdb")
    monkeypatch.setenv("SECRET_KEY", "supersecret")
    monkeypatch.setenv("DEBUG", "true")

    new_config = Config()
    assert new_config.database_url == "postgresql+asyncpg://test:test@localhost/testdb"
    assert new_config.secret_key == "supersecret"
    assert new_config.debug is True

if __name__ == "__main__":
    import pytest as pt
    pt.main([__file__, "-v"])
