"""
Database Schemas for Consultancy LMS

Each Pydantic model represents a MongoDB collection. The collection name
is the lowercase of the class name (e.g., User -> "user").

These schemas are used for validation and for the auto database viewer.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class User(BaseModel):
    """
    Users of the platform: consultants and clients
    Collection: "user"
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Unique email address")
    role: str = Field("client", description="Role of the user: consultant | client | admin")
    avatar_url: Optional[str] = Field(None, description="Profile image URL")
    bio: Optional[str] = Field(None, description="Short bio or headline")
    is_active: bool = Field(True, description="Whether the user is active")


class Course(BaseModel):
    """
    Courses offered by consultants. Each course can have many lessons.
    Collection: "course"
    """
    title: str = Field(..., description="Course title")
    description: Optional[str] = Field(None, description="What this course covers")
    consultant_id: str = Field(..., description="Owner consultant user id (string ObjectId)")
    tags: List[str] = Field(default_factory=list, description="Keywords for discovery")
    is_published: bool = Field(False, description="Visibility flag")


class Lesson(BaseModel):
    """
    Lessons are pieces of content inside a course
    Collection: "lesson"
    """
    course_id: str = Field(..., description="Parent course id (string ObjectId)")
    title: str = Field(..., description="Lesson title")
    content: Optional[str] = Field(None, description="Markdown/HTML or plain text content")
    order: int = Field(1, ge=1, description="Ordering within the course")


class Enrollment(BaseModel):
    """
    Link between a user and a course
    Collection: "enrollment"
    """
    user_id: str = Field(..., description="User id (string ObjectId)")
    course_id: str = Field(..., description="Course id (string ObjectId)")
    status: str = Field("active", description="active | completed | cancelled")


class Session(BaseModel):
    """
    1:1 or group session booking
    Collection: "session"
    """
    title: str = Field(..., description="Session title or topic")
    user_id: str = Field(..., description="Client user id (string ObjectId)")
    consultant_id: str = Field(..., description="Consultant user id (string ObjectId)")
    course_id: Optional[str] = Field(None, description="Related course id if applicable")
    start_time: datetime = Field(..., description="Start datetime in ISO format")
    duration_minutes: int = Field(60, ge=15, le=480, description="Duration in minutes")
    notes: Optional[str] = Field(None, description="Additional context or agenda")
