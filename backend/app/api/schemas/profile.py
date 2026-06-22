"""Pydantic schemas for student profiles."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class StudentProfileCreate(BaseModel):
    """Input schema for creating a student profile."""
    university: str = Field(..., min_length=2, max_length=255, description="University name")
    department: str = Field(..., min_length=2, max_length=255, description="Degree program / department")
    semester: int = Field(..., ge=1, le=16, description="Current semester")
    gpa: float = Field(..., ge=0.0, le=4.0, description="GPA / CGPA on 4.0 scale")
    degree_level: Literal["bachelor", "master", "phd"] = Field(..., description="Current degree level")
    skills: list[str] = Field(default_factory=list, description="Skills list")
    interests: list[str] = Field(default_factory=list, description="Academic and career interests")
    preferred_countries: list[str] = Field(default_factory=list, description="Preferred countries")
    opportunity_types: list[Literal[
        "scholarship", "internship", "research", "fellowship", "exchange", "summer_school"
    ]] = Field(default_factory=list, description="Types of opportunities sought")

    class Config:
        json_schema_extra = {
            "example": {
                "university": "Stanford University",
                "department": "Computer Science",
                "semester": 6,
                "gpa": 3.7,
                "degree_level": "bachelor",
                "skills": ["Python", "Machine Learning", "Data Analysis", "Research"],
                "interests": ["Artificial Intelligence", "Natural Language Processing"],
                "preferred_countries": ["United States", "United Kingdom", "Germany"],
                "opportunity_types": ["scholarship", "internship", "research"],
            }
        }


class StudentProfileResponse(BaseModel):
    """Response schema for a student profile."""
    id: str
    university: str
    department: str
    semester: int
    gpa: float
    degree_level: str
    skills: list[str]
    interests: list[str]
    preferred_countries: list[str]
    opportunity_types: list[str]

    class Config:
        from_attributes = True
