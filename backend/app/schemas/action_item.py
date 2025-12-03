"""
ActionItem Pydantic Schemas

This module defines Pydantic models for action item data validation
and serialization. These schemas are used for API request/response
handling.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.action_item import ActionItemPriority, ActionItemStatus


class ActionItemBase(BaseModel):
    """Base schema with common action item fields."""

    title: str = Field(
        ..., min_length=1, max_length=255, description="Action item title"
    )
    description: Optional[str] = Field(None, description="Detailed description")
    owner: Optional[str] = Field(
        None, max_length=100, description="Person responsible"
    )
    due_date: Optional[datetime] = Field(None, description="Deadline for completion")
    priority: ActionItemPriority = Field(
        ActionItemPriority.MEDIUM, description="Priority level"
    )


class ActionItemCreate(ActionItemBase):
    """Schema for creating a new action item."""

    meeting_id: int = Field(..., description="ID of the parent meeting")


class ActionItemUpdate(BaseModel):
    """Schema for updating an existing action item."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Action item title"
    )
    description: Optional[str] = Field(None, description="Detailed description")
    owner: Optional[str] = Field(
        None, max_length=100, description="Person responsible"
    )
    due_date: Optional[datetime] = Field(None, description="Deadline for completion")
    status: Optional[ActionItemStatus] = Field(None, description="Current status")
    priority: Optional[ActionItemPriority] = Field(None, description="Priority level")


class ActionItemResponse(ActionItemBase):
    """Schema for action item response."""

    id: int
    meeting_id: int
    status: ActionItemStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemStatusUpdate(BaseModel):
    """Schema for updating action item status only."""

    status: ActionItemStatus = Field(..., description="New status")

