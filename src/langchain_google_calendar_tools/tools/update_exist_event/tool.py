from datetime import datetime
from typing import Dict, List, Optional, Type

from googleapiclient.errors import HttpError  # type: ignore
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import EmailStr

from langchain_google_calendar_tools.tools.base import CalendarBaseTool
from langchain_google_calendar_tools.tools.update_exist_event.input_arg import (
    UpdateExistEventArgsSchema,
)


class UpdateExistEvent(CalendarBaseTool):
    """Tool that update exist event in the user's calendar."""

    name: str = "update_exist_event"
    # flake8: noqa
    description: str = (
        "Use this tool to update exist event"
        + " You must provide all 4 fields including: event_id, summary, end date and start date to update the event, it can be get from list_events tool. "
        + " In case summary, end date and start date need to be updated, use new data."
        + " You can update summary, start time, end time, location, description, attendees."
        + " Updating recurring event is not supported."
    )
    args_schema: Type[UpdateExistEventArgsSchema] = UpdateExistEventArgsSchema

    def _run(
        self,
        event_id: str,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        location: Optional[str] = None,
        description: Optional[str] = None,
        attendees: Optional[List[EmailStr]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict:
        """Run the tool."""

        if not event_id:
            return {"error": "event_id must not be empty. You can get it from list_events tool."}

        start_time = self.add_timezone(start_time)

        end_time = self.add_timezone(end_time)

        event = {
            "summary": summary,
            "start": {
                "dateTime": self.format_date(start_time),
                "timeZone": start_time.tzinfo.zone,  # type: ignore
            },
            "end": {
                "dateTime": self.format_date(end_time),
                "timeZone": end_time.tzinfo.zone,  # type: ignore
            },
        }

        if location:
            event["location"] = location

        if description:
            event["description"] = description

        if attendees:
            event["attendees"] = [{"email": str(attendee)} for attendee in attendees]  # type: ignore

        try:
            response = self.api_resource.events().update(eventId=event_id, calendarId="primary", body=event).execute()
        except HttpError as e:
            return {"error": {"code": e.resp.status, "message": e.reason}}

        return response
