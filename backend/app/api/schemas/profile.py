"""Pydantic schemas for student profiles."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class StudentProfileCreate(BaseModel):
    """Input schema for creating a student profile."""
    university: str = Field(..., min_length=2, max_length=255, description="University name")
    department: str = Field(..., min_length=2, max_length=255, description="Degree program / department")
    semester: int = Field(..., ge=1, le=8, description="Current semester")
    gpa: float = Field(..., ge=0.0, description="GPA / CGPA")
    gpa_scale: float = Field(default=4.0, ge=1.0, le=10.0, description="GPA scale (4.0, 5.0, 10.0, etc.)")
    degree_level: Literal["bachelor", "master", "phd"] = Field(..., description="Current degree level")
    skills: list[str] = Field(default_factory=list, description="Skills list")
    interests: list[str] = Field(default_factory=list, description="Academic and career interests")
    preferred_countries: list[str] = Field(default_factory=list, description="Preferred countries")
    opportunity_types: list[Literal[
        "scholarship", "internship", "research", "fellowship", "exchange", "summer_school"
    ]] = Field(default_factory=list, description="Types of opportunities sought")

    @model_validator(mode='after')
    def validate_gpa(self) -> 'StudentProfileCreate':
        if self.gpa > self.gpa_scale:
            raise ValueError(f"GPA ({self.gpa}) cannot be greater than the GPA scale ({self.gpa_scale})")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "university": "Stanford University",
                "department": "Computer Science",
                "semester": 6,
                "gpa": 3.7,
                "gpa_scale": 4.0,
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
    gpa_scale: float
    degree_level: str
    skills: list[str]
    interests: list[str]
    preferred_countries: list[str]
    opportunity_types: list[str]

    class Config:
        from_attributes = True
