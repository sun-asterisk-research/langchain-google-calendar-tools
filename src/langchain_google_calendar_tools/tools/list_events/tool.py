from datetime import datetime, timedelta
from typing import Dict, Optional, Type

from googleapiclient.errors import HttpError  # type: ignore
from langchain.callbacks.manager import CallbackManagerForToolRun

from langchain_google_calendar_tools.tools.base import CalendarBaseTool
from langchain_google_calendar_tools.tools.list_events.input_arg import SearchArgsSchema


class ListEvents(CalendarBaseTool):
    """Tool that gets k events from the user's calendar. You can filter by start date, end date and event summary."""

    name: str = "list_events"
    description: str = (
        "Use this tool to get k events from the user's calendar. "
        + " You can filter by start date, end date and event summary."
        + " Returns all events and their details."
    )

    args_schema: Type[SearchArgsSchema] = SearchArgsSchema

    def _run(
        self,
        num_events: int,
        summary: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict:
        """Run the tool."""

        summary = summary.strip() if summary is not None else None

        if start_date is not None and start_date == end_date:
            end_date = start_date + timedelta(days=1)

        if start_date is not None:
            start_date = self.add_timezone(start_date)
        else:
            start_date = self.add_timezone(datetime.now())

        start_text = self.format_date(start_date)

        if end_date is not None:
            end_date = self.add_timezone(end_date)
            end_text = self.format_date(end_date)

        query = self.api_resource.events().list(
            calendarId="primary",
            timeMin=start_text,
            timeMax=end_text,
            maxResults=num_events,
            singleEvents=True,
            orderBy="startTime",
            q=summary,
        )

        try:
            response = query.execute()
        except HttpError as err:
            return {"error": {"code": err.resp.status, "message": err.reason}}

        return {
            "events": [
                {
                    "event_id": event.get("id"),
                    "summary": event.get("summary"),
                    "creator": event.get("creator", {}).get("email"),
                    "organizer": event.get("organizer", {}).get("email"),
                    "htmlLink": event.get("htmlLink"),
                    "start": {
                        "date": event.get("start", {}).get("date"),
                        "dateTime": event.get("start", {}).get("dateTime"),
                        "timeZone": event.get("start", {}).get("timeZone"),
                    },
                    "end": {
                        "date": event.get("start", {}).get("date"),
                        "dateTime": event.get("start", {}).get("dateTime"),
                        "timeZone": event.get("start", {}).get("timeZone"),
                    },
                    "location": event.get("location"),
                    "attendees": event.get("attendees", []),
                }
                for event in response.get("items", [])
                if summary is None or summary.lower() == event.get("summary", "").lower()
            ]
        }
