"""
ActionItem Database Model

This module defines the ActionItem model representing a task or action
extracted from a meeting. Action items have status, priority, owner,
and due date for tracking completion.
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.meeting import Meeting


class ActionItemStatus(str, Enum):
    """
    Enumeration of action item statuses.

    - TODO: Not started
    - IN_PROGRESS: Currently being worked on
    - DONE: Completed
    - CANCELLED: No longer needed
    """

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class ActionItemPriority(str, Enum):
    """
    Enumeration of action item priorities.

    - HIGH: Urgent/important tasks
    - MEDIUM: Normal priority
    - LOW: Can be deferred
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionItem(Base):
    """
    ActionItem model representing a task extracted from a meeting.

    Attributes:
        id: Primary key
        meeting_id: Foreign key to the parent meeting
        title: Action item title (required)
        description: Detailed description (optional)
        owner: Person responsible for this action item
        due_date: Deadline for completion
        status: Current status (todo/in_progress/done/cancelled)
        priority: Priority level (high/medium/low)
        created_at: Record creation timestamp
        updated_at: Record last update timestamp
        meeting: Parent meeting (many-to-one relationship)
    """

    __tablename__ = "action_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False
    )

    # Core fields
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Status and priority
    status: Mapped[str] = mapped_column(
        String(50), default=ActionItemStatus.TODO.value, nullable=False
    )
    priority: Mapped[str] = mapped_column(
        String(50), default=ActionItemPriority.MEDIUM.value, nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="action_items")

    def __repr__(self) -> str:
        return f"<ActionItem(id={self.id}, title='{self.title}', status='{self.status}')>"
