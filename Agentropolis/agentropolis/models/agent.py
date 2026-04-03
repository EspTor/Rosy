"""Agent model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from ..database import Base

class Agent(Base):
    __tablename__ = "agents"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    occupation: Mapped[str] = mapped_column(String(100), nullable=True)
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id"), nullable=True, index=True)
    x: Mapped[float] = mapped_column(Float, default=0.0)
    y: Mapped[float] = mapped_column(Float, default=0.0)
    health: Mapped[int] = mapped_column(Integer, default=100)
    energy: Mapped[int] = mapped_column(Integer, default=100)
    hunger: Mapped[int] = mapped_column(Integer, default=0)
    happiness: Mapped[int] = mapped_column(Integer, default=25)
    money: Mapped[float] = mapped_column(Float, default=100.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_llm_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_tick: Mapped[int] = mapped_column(Integer, nullable=True)
    died_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    location: Mapped["Location"] = relationship("Location", back_populates="occupants")
    relationships_as_a: Mapped[list["Relationship"]] = relationship("Relationship", foreign_keys="Relationship.agent_a_id", back_populates="agent_a", cascade="all, delete-orphan")
    relationships_as_b: Mapped[list["Relationship"]] = relationship("Relationship", foreign_keys="Relationship.agent_b_id", back_populates="agent_b", cascade="all, delete-orphan")
