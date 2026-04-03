"""Configuration management using environment variables."""

import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

@dataclass
class Config:
    """Application configuration loaded from environment."""

    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql+asyncpg://localhost/agentropolis"))
    secret_key: Optional[str] = field(default_factory=lambda: os.getenv("SECRET_KEY"))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")

config = Config()
