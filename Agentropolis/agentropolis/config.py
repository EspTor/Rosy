"""Configuration management using environment variables."""')

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Application configuration loaded from environment."""
    
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://agentropolis:agentropolis@localhost:5432/agentropolis"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Simulation
    tick_rate: int = int(os.getenv("TICK_RATE", "10"))
    max_agents: int = int(os.getenv("MAX_AGENTS", "1000"))
    
    # LLM (OpenRouter)
    openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "microsoft/phi-3-mini-128k-instruct")
    llm_cost_limit_usd: float = float(os.getenv("LLM_COST_LIMIT", "20.0"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment."""
        return cls()


config = Config.from_env()
