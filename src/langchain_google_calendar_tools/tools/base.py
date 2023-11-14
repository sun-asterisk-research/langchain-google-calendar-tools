"""Base class for Google Calendar tools."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

import pytz
from langchain.pydantic_v1 import Field
from langchain.tools.base import BaseTool

from langchain_google_calendar_tools.utils import build_resource_service

if TYPE_CHECKING:
    # This is for linting and IDE typehints
    from googleapiclient.discovery import Resource  # type: ignore
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from googleapiclient.discovery import Resource
    except ImportError:
        pass


class CalendarBaseTool(BaseTool):
    """Base class for Google Calendar tools."""

    name: str = "calendar_base_tool"
    description: str = "Base class for Google Calendar tools."
    api_resource: Resource = Field(default_factory=build_resource_service)

    def format_date(self, date_data: datetime) -> str:
        """Format date to RFC3339 format."""
        return date_data.isoformat()

    @property
    def timezone(self):
        # TODO: get timezone from user's calendar
        return pytz.timezone("Asia/Ho_Chi_Minh")

    def add_timezone(self, date: datetime) -> datetime:
        if date.tzinfo:
            return date

        return self.timezone.localize(date, is_dst=None)

    @classmethod
    def from_api_resource(cls, api_resource: Resource) -> "CalendarBaseTool":
        """Create a tool from an api resource.

        Args:
            api_resource: The api resource to use.

        Returns:
            A tool.
        """
        return cls(api_resource=api_resource)
