"""Base class for Google Calendar tools."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools.base import BaseTool


class GetCurrentDatetime(BaseTool):
    """Helper tool that get current datetime."""

    name: str = "get_current_datetime"
    description: str = "Use this tool to get current datetime."

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return datetime.now().isoformat() + 'Z'
