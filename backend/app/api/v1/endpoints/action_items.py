"""
Action Items API Endpoints

This module defines the API endpoints for action item management.
These are placeholder implementations that will be fully implemented in E04-E05.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas.action_item import (
    ActionItemCreate,
    ActionItemResponse,
    ActionItemStatusUpdate,
    ActionItemUpdate,
)

router = APIRouter()


@router.get("", response_model=List[ActionItemResponse])
async def list_action_items(meeting_id: int = None):
    """
    List action items.

    Returns all action items, optionally filtered by meeting_id.
    This endpoint will be fully implemented in E04.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint will be implemented in E04",
    )


@router.post("", response_model=ActionItemResponse, status_code=status.HTTP_201_CREATED)
async def create_action_item(action_item: ActionItemCreate):
    """
    Create a new action item.

    Creates a new action item associated with a meeting.
    This endpoint will be fully implemented in E04.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint will be implemented in E04",
    )


@router.get("/{action_item_id}", response_model=ActionItemResponse)
async def get_action_item(action_item_id: int):
    """
    Get an action item by ID.

    Returns the full action item details.
    This endpoint will be fully implemented in E04.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint will be implemented in E04",
    )


@router.put("/{action_item_id}", response_model=ActionItemResponse)
async def update_action_item(action_item_id: int, action_item: ActionItemUpdate):
    """
    Update an action item.

    Updates the action item with the provided information.
    This endpoint will be fully implemented in E05.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint will be implemented in E05",
    )


@router.patch("/{action_item_id}/status", response_model=ActionItemResponse)
async def update_action_item_status(
    action_item_id: int, status_update: ActionItemStatusUpdate
):
    """
    Update action item status.

    Updates only the status of an action item.
    This endpoint will be fully implemented in E05.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint will be implemented in E05",
    )


@router.delete("/{action_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_action_item(action_item_id: int):
    """
    Delete an action item.

    Deletes the specified action item.
    This endpoint will be fully implemented in E05.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint will be implemented in E05",
    )

