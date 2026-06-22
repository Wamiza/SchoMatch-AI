"""
ORM models for SchoMatch-AI database.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, JSON, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    university: Mapped[str] = mapped_column(String(255))
    department: Mapped[str] = mapped_column(String(255))
    semester: Mapped[int] = mapped_column(Integer)
    gpa: Mapped[float] = mapped_column(Float)
    degree_level: Mapped[str] = mapped_column(String(50))
    skills: Mapped[dict] = mapped_column(JSON, default=list)
    interests: Mapped[dict] = mapped_column(JSON, default=list)
    preferred_countries: Mapped[dict] = mapped_column(JSON, default=list)
    opportunity_types: Mapped[dict] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sessions: Mapped[list["SearchSession"]] = relationship(back_populates="profile", cascade="all, delete-orphan")
    saved_opportunities: Mapped[list["SavedOpportunity"]] = relationship(back_populates="profile", cascade="all, delete-orphan")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(500))
    organization: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(100))
    deadline: Mapped[str] = mapped_column(String(100), nullable=True)
    funding_status: Mapped[str] = mapped_column(String(100))
    application_link: Mapped[str] = mapped_column(String(1000))
    opportunity_type: Mapped[str] = mapped_column(String(50))
    requirements: Mapped[dict] = mapped_column(JSON, default=dict)
    tags: Mapped[dict] = mapped_column(JSON, default=list)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    eligibility_summary: Mapped[str] = mapped_column(Text, nullable=True)
    degree_levels: Mapped[dict] = mapped_column(JSON, default=list)
    fields_of_study: Mapped[dict] = mapped_column(JSON, default=list)
    min_gpa: Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SearchSession(Base):
    __tablename__ = "search_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("student_profiles.id"))
    results: Mapped[dict] = mapped_column(JSON, default=list)
    agent_trace: Mapped[dict] = mapped_column(JSON, default=dict)
    total_matches: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile: Mapped["StudentProfile"] = relationship(back_populates="sessions")


class SavedOpportunity(Base):
    __tablename__ = "saved_opportunities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("student_profiles.id"))
    opportunity_id: Mapped[str] = mapped_column(String(36), ForeignKey("opportunities.id"))
    match_score: Mapped[int] = mapped_column(Integer, default=0)
    action_plan: Mapped[dict] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(50), default="saved")
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile: Mapped["StudentProfile"] = relationship(back_populates="saved_opportunities")
    opportunity: Mapped["Opportunity"] = relationship()
    reminders: Mapped[list["DeadlineReminder"]] = relationship(back_populates="saved_opportunity", cascade="all, delete-orphan")


class DeadlineReminder(Base):
    __tablename__ = "deadline_reminders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    saved_opportunity_id: Mapped[str] = mapped_column(String(36), ForeignKey("saved_opportunities.id"))
    reminder_date: Mapped[str] = mapped_column(String(20))
    reminder_type: Mapped[str] = mapped_column(String(50))
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    saved_opportunity: Mapped["SavedOpportunity"] = relationship(back_populates="reminders")
