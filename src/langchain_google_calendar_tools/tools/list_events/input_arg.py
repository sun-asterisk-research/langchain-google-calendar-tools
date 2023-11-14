from datetime import datetime
from typing import Optional

from langchain.pydantic_v1 import BaseModel, Field


class SearchArgsSchema(BaseModel):
    """Input for GetMessageTool."""

    num_events: int = Field(
        ...,
        description="The number of events to return.",
    )

    end_date: Optional[datetime] = Field(
        default=None,
        description="The maximum end date of the events to return.",
    )
    start_date: Optional[datetime] = Field(
        default=None,
        description="The minimum start date of the events to return.",
    )

    summary: Optional[str] = Field(
        default=None,
        description="The summary of the events to return, use for filtering.",
    )
