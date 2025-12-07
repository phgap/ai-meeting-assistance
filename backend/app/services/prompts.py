"""
Prompt Templates for AI Meeting Assistant

This module contains all prompt templates used for LLM interactions.
Prompts are designed for structured JSON output to ensure consistent parsing.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


# =============================================================================
# Output Schemas
# =============================================================================

class MeetingSummaryOutput(BaseModel):
    """
    Structured output schema for meeting summary generation.
    
    This schema defines the expected JSON structure from the LLM
    when generating meeting summaries.
    """
    
    summary: str = Field(
        ...,
        description="A concise 3-5 sentence summary of the meeting, capturing the main purpose and outcomes",
    )
    topics: List[str] = Field(
        ...,
        description="List of core topics/agenda items discussed in the meeting",
    )
    decisions: List[str] = Field(
        default_factory=list,
        description="List of specific decisions made during the meeting",
    )
    discussion_points: List[str] = Field(
        default_factory=list,
        description="Key discussion points, arguments, and notable viewpoints raised",
    )


# =============================================================================
# System Prompts
# =============================================================================

MEETING_SUMMARY_SYSTEM_PROMPT = """You are a professional meeting notes assistant specializing in creating clear, actionable meeting summaries. Your role is to:

1. Analyze meeting content thoroughly
2. Extract key information in a structured format
3. Identify important decisions and discussion points
4. Write concise, professional summaries

Guidelines:
- Be objective and factual
- Focus on actionable information
- Use clear, professional language
- Preserve important context and nuances
- Do not invent information not present in the original content

You must always respond with valid JSON matching the specified schema."""


# =============================================================================
# User Prompt Templates
# =============================================================================

MEETING_SUMMARY_USER_PROMPT = """Please analyze the following meeting content and generate a structured summary.

Meeting Title: {title}
Meeting Time: {meeting_time}
Participants: {participants}

---
Meeting Content:
{content}
---

Generate a JSON response with the following structure:
{{
    "summary": "A concise 3-5 sentence summary capturing the meeting's main purpose and outcomes",
    "topics": ["List of core topics/agenda items discussed"],
    "decisions": ["List of specific decisions made (if any)"],
    "discussion_points": ["Key discussion points and notable viewpoints raised"]
}}

Requirements:
1. Summary should be 3-5 sentences, capturing the essence of the meeting
2. Topics should list the main subjects discussed (typically 2-5 items)
3. Decisions should only include explicit decisions made (leave empty if none)
4. Discussion points should capture key arguments and viewpoints

Respond with valid JSON only."""


# =============================================================================
# Helper Functions
# =============================================================================

def build_summary_prompt(
    title: str,
    content: str,
    meeting_time: Optional[str] = None,
    participants: Optional[List[str]] = None,
) -> List[dict]:
    """
    Build the messages list for meeting summary generation.
    
    Args:
        title: Meeting title
        content: Original meeting content/transcript
        meeting_time: Optional meeting time string
        participants: Optional list of participant names
        
    Returns:
        List of message dictionaries for the LLM API
    """
    # Format meeting time
    time_str = meeting_time or "Not specified"
    
    # Format participants
    if participants:
        participants_str = ", ".join(participants)
    else:
        participants_str = "Not specified"
    
    # Build user prompt
    user_prompt = MEETING_SUMMARY_USER_PROMPT.format(
        title=title,
        meeting_time=time_str,
        participants=participants_str,
        content=content,
    )
    
    return [
        {"role": "system", "content": MEETING_SUMMARY_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def get_summary_output_schema() -> dict:
    """
    Get the JSON schema for meeting summary output.
    
    Returns:
        JSON schema dictionary for validation
    """
    return MeetingSummaryOutput.model_json_schema()

