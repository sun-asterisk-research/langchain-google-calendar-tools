from datetime import datetime
from typing import List, Optional

from langchain.pydantic_v1 import BaseModel, EmailStr, Field


class UpdateExistEventArgsSchema(BaseModel):
    """Input for UpdateExistEvent."""

    event_id: str = Field(
        ...,
        description="The id of the event to update. You can get it from list_events tool. It must not be empty.",
    )

    summary: str = Field(
        ...,
        description="The summary of the event.",
    )

    start_time: datetime = Field(
        ...,
        description="The start time of the event.",
    )

    end_time: datetime = Field(
        ...,
        description="The end time of the event.",
    )

    location: Optional[str] = Field(
        default=None,
        description="The location of the event.",
    )

    description: Optional[str] = Field(
        default=None,
        description="The description of the event.",
    )

    attendees: List[EmailStr] = Field(
        default=[],
        description="The attendees of the event.",
    )
