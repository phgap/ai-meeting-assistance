"""
Meeting Pydantic Schemas

This module defines Pydantic models for meeting data validation
and serialization. These schemas are used for API request/response
handling.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.meeting import MeetingStatus


class MeetingBase(BaseModel):
    """Base schema with common meeting fields."""

    title: str = Field(..., min_length=1, max_length=255, description="Meeting title")
    start_time: Optional[datetime] = Field(None, description="Meeting start time")
    end_time: Optional[datetime] = Field(None, description="Meeting end time")


class MeetingCreate(MeetingBase):
    """Schema for creating a new meeting."""

    original_text: Optional[str] = Field(
        None, max_length=50000, description="Original meeting content/transcript"
    )


class MeetingUpdate(BaseModel):
    """Schema for updating an existing meeting."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Meeting title"
    )
    start_time: Optional[datetime] = Field(None, description="Meeting start time")
    end_time: Optional[datetime] = Field(None, description="Meeting end time")
    original_text: Optional[str] = Field(
        None, max_length=50000, description="Original meeting content/transcript"
    )
    summary: Optional[str] = Field(None, description="AI-generated meeting summary")
    status: Optional[MeetingStatus] = Field(None, description="Meeting status")


class ActionItemBrief(BaseModel):
    """Brief action item info for embedding in meeting response."""

    id: int
    title: str
    status: str
    priority: str
    owner: Optional[str] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class MeetingResponse(MeetingBase):
    """Schema for meeting response."""

    id: int
    original_text: Optional[str] = None
    summary: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    action_items: List[ActionItemBrief] = []

    class Config:
        from_attributes = True


class MeetingListResponse(BaseModel):
    """Schema for meeting list item (without full content)."""

    id: int
    title: str
    start_time: Optional[datetime] = None
    status: str
    created_at: datetime
    action_item_count: int = 0

    class Config:
        from_attributes = True

