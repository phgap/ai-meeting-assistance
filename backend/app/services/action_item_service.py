"""
Action Item Extraction Service

This module provides the service layer for extracting action items from meeting content
using AI. It identifies actionable tasks, responsible persons, deadlines, and priorities.
"""

import logging
from datetime import date, datetime
from typing import List, Optional

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.action_item import ActionItem
from app.models.meeting import Meeting
from app.services.llm_service import (
    LLMError,
    LLMResponseParseError,
    get_llm_service,
)
from app.services.prompts import (
    ActionItemsExtractionOutput,
    build_action_items_prompt,
)

logger = logging.getLogger(__name__)


class ActionItemExtractionError(Exception):
    """Raised when action item extraction fails."""
    pass


class MeetingNotFoundError(Exception):
    """Raised when meeting is not found."""
    pass


class ActionItemExtractionService:
    """
    Service for extracting action items from meeting content using AI.
    
    This service handles the complete flow of:
    1. Loading meeting from database
    2. Building prompts with meeting content
    3. Calling LLM for action item extraction
    4. Parsing and validating the response
    5. Storing results back to database
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the extraction service.
        
        Args:
            db: Async database session
        """
        self.db = db
        self.llm = get_llm_service()
    
    async def extract_action_items(self, meeting_id: int) -> List[ActionItem]:
        """
        Extract action items from a meeting's content.
        
        This is the main entry point for action item extraction. It:
        1. Loads the meeting from database
        2. Validates that it has content to extract from
        3. Calls LLM to extract action items
        4. Saves extracted items to database
        
        Args:
            meeting_id: ID of the meeting to extract action items from
            
        Returns:
            List of created ActionItem objects
            
        Raises:
            MeetingNotFoundError: If meeting doesn't exist
            ActionItemExtractionError: If extraction fails
        """
        # Load meeting
        meeting = await self._get_meeting(meeting_id)
        if not meeting:
            raise MeetingNotFoundError(f"Meeting with id {meeting_id} not found")
        
        # Validate content exists
        if not meeting.original_text or not meeting.original_text.strip():
            raise ActionItemExtractionError(
                "Meeting has no content to extract action items from. "
                "Please add original_text first."
            )
        
        try:
            # Extract action items using LLM
            extraction_output = await self._extract_from_llm(meeting)
            
            # Save to database
            action_items = await self._save_action_items(
                meeting_id, extraction_output.action_items
            )
            
            logger.info(
                f"Successfully extracted {len(action_items)} action items "
                f"for meeting {meeting_id}"
            )
            
            return action_items
            
        except Exception as e:
            logger.error(f"Failed to extract action items for meeting {meeting_id}: {e}")
            raise ActionItemExtractionError(f"Action item extraction failed: {e}")
    
    async def _get_meeting(self, meeting_id: int) -> Optional[Meeting]:
        """Load a meeting from the database."""
        result = await self.db.execute(
            select(Meeting).where(Meeting.id == meeting_id)
        )
        return result.scalar_one_or_none()
    
    async def _extract_from_llm(self, meeting: Meeting) -> ActionItemsExtractionOutput:
        """
        Extract action items using LLM.
        
        Args:
            meeting: Meeting object with content
            
        Returns:
            Validated ActionItemsExtractionOutput object
            
        Raises:
            ActionItemExtractionError: If LLM call or parsing fails
        """
        # Determine meeting date for relative time conversion
        meeting_date: Optional[date] = None
        if meeting.start_time:
            meeting_date = meeting.start_time.date()
        
        # Build prompt messages
        messages = build_action_items_prompt(
            meeting_content=meeting.original_text,
            participants=meeting.participants,
            meeting_date=meeting_date,
        )
        
        try:
            # Call LLM with JSON mode
            response = await self.llm.generate_json(
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent output
            )
            
            # Validate response against schema
            extraction_output = ActionItemsExtractionOutput(**response)
            return extraction_output
            
        except LLMResponseParseError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise ActionItemExtractionError(f"Failed to parse AI response: {e}")
        except ValidationError as e:
            logger.error(f"LLM response validation failed: {e}")
            raise ActionItemExtractionError(f"AI response validation failed: {e}")
        except LLMError as e:
            logger.error(f"LLM API error: {e}")
            raise ActionItemExtractionError(f"AI service error: {e}")
    
    async def _save_action_items(
        self,
        meeting_id: int,
        items: List,
    ) -> List[ActionItem]:
        """
        Save extracted action items to database.
        
        Args:
            meeting_id: ID of the parent meeting
            items: List of ActionItemOutput objects from LLM
            
        Returns:
            List of created ActionItem database objects
        """
        action_items = []
        
        for item in items:
            # Parse due_date if provided
            due_date: Optional[datetime] = None
            if item.due_date:
                try:
                    due_date = datetime.strptime(item.due_date, "%Y-%m-%d")
                except ValueError:
                    logger.warning(
                        f"Invalid due_date format '{item.due_date}', setting to None"
                    )
            
            # Create ActionItem record
            db_item = ActionItem(
                meeting_id=meeting_id,
                title=item.title,
                description=item.description or "",
                owner=item.owner,
                due_date=due_date,
                priority=item.priority,
                status="todo",  # Initial status
            )
            self.db.add(db_item)
            action_items.append(db_item)
        
        # Flush to get IDs assigned
        await self.db.flush()
        
        # Refresh all items to get complete data
        for item in action_items:
            await self.db.refresh(item)
        
        logger.info(
            f"Saved {len(action_items)} action items for meeting {meeting_id}"
        )
        
        return action_items


async def extract_meeting_action_items(
    db: AsyncSession, 
    meeting_id: int
) -> List[ActionItem]:
    """
    Convenience function to extract action items from a meeting.
    
    Args:
        db: Database session
        meeting_id: ID of the meeting to extract from
        
    Returns:
        List of created ActionItem objects
    """
    service = ActionItemExtractionService(db)
    return await service.extract_action_items(meeting_id)

