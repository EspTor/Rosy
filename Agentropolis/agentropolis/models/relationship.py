"""Relationship model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from ..database import Base

class Relationship(Base):
    __tablename__ = "relationships"
    agent_a_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True)
    agent_b_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True)
    type: Mapped[str] = mapped_column(String(50), default="stranger")
    trust: Mapped[float] = mapped_column(Float, default=0.5)
    affection: Mapped[float] = mapped_column(Float, default=0.0)
    familiarity: Mapped[float] = mapped_column(Float, default=0.0)
    interaction_count: Mapped[int] = mapped_column(Integer, default=0)
    last_interaction_tick: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    agent_a: Mapped["Agent"] = relationship("Agent", foreign_keys=[agent_a_id], back_populates="relationships_as_a")
    agent_b: Mapped["Agent"] = relationship("Agent", foreign_keys=[agent_b_id], back_populates="relationships_as_b")
