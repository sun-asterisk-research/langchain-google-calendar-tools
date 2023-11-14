from datetime import datetime
from typing import Dict, List, Literal, Optional

from langchain.pydantic_v1 import BaseModel, EmailStr, Field


class RecurringConfig(BaseModel):
    # flake8: noqa
    frequency: Literal["SECONDLY", "MINUTELY", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"] = Field(
        ...,
        description="The frequency of the recurring event, must be one of the following: SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY",
    )

    interval: int = Field(
        ...,
        description="The interval between each event in the recurring event series, must be a positive integer, default is 1",
    )

    count: Optional[int] = Field(
        default=None,
        description="The number of times the event should recur. Optional.",
    )

    until: Optional[datetime] = Field(
        default=None,
        description="The date and time when the event should stop recurring. Optional. You can use either COUNT or UNTIL to specify the end of the event recurrence. Don't use both in the same rule.",
    )

    byday: Optional[Literal["SU", "MO", "TU", "WE", "TH", "FR", "SA"]] = Field(
        default=None,
        description="The days of the week that the event should recur. Optional. Must be one or more of the following: SU, MO, TU, WE, TH, FR, SA",
    )


class CreateEventArgsSchema(BaseModel):
    """Input for CreateNewEvent."""

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

    recurring_config: Optional[RecurringConfig] = Field(
        default=None,
        description="The recurring config of the event.",
    )
