from datetime import datetime
from typing import Dict, List, Optional, Type

from googleapiclient.errors import HttpError  # type: ignore
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import EmailStr

from langchain_google_calendar_tools.tools.base import CalendarBaseTool
from langchain_google_calendar_tools.tools.create_new_event.input_arg import (
    CreateEventArgsSchema,
    RecurringConfig,
)


class CreateNewEvent(CalendarBaseTool):
    """Tool that create new event in the user's calendar."""

    name: str = "create_new_event"
    description: str = (
        "Use this tool to create new event (not recurring events)"
        + " User must provide summary, start and end time."
        + " In addition, user can provide location, description, attendees."
        + " Reminder is not supported yet."
        + " Returns the event summary"
    )
    args_schema: Type[CreateEventArgsSchema] = CreateEventArgsSchema

    def __format_recurring_config(self, recurring_config: RecurringConfig) -> str:
        """Format recurring config to RFC3339 format."""

        rules = [
            f"FREQ={recurring_config.frequency}",
        ]

        if recurring_config.interval:
            rules.append(f"INTERVAL={recurring_config.interval}")

        if recurring_config.until is not None and recurring_config.count is not None:
            raise ValueError("UNTIL and COUNT cannot be used together")

        if recurring_config.count:
            rules.append(f"COUNT={recurring_config.count}")

        if recurring_config.until:
            rules.append(f"UNTIL={self.format_date(recurring_config.until)}")

        if recurring_config.byday:
            rules.append(f"BYDAY={','.join(recurring_config.byday)}")

        return 'RRULE:' + ';'.join(rules)

    def _run(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        location: Optional[str] = None,
        description: Optional[str] = None,
        attendees: Optional[List[EmailStr]] = None,
        recurring_config: Optional[RecurringConfig] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict:
        """Run the tool."""

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
            event["attendees"] = [{"email": attendee} for attendee in attendees]  # type: ignore

        if recurring_config:
            try:
                event["recurrence"] = self.__format_recurring_config(recurring_config)
            except ValueError as e:
                return {"error": str(e)}

        try:
            response = self.api_resource.events().insert(calendarId="primary", body=event).execute()
        except HttpError as e:
            return {"error": {"code": e.resp.status, "message": e.reason}}

        return response
