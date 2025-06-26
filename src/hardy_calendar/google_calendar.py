import os
import re
import json
import datetime
from typing import Any
from dateutil import parser as dtparser
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service() -> Any:
    creds_json: str | None = os.environ.get('GOOGLE_API_CREDENTIALS')
    if creds_json is None:
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')) as f:
            creds_json = f.read()
    creds_info: dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_info)
    return build("calendar", "v3", credentials=creds)

def remove_existing_events(service: Any, cal_id: str, date: datetime.date) -> None:
    # Use RFC3339 full-day range in UTC
    time_min = date.strftime("%Y-%m-%dT00:00:00Z")
    time_max = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    events_result = service.events().list(
        calendarId=cal_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        q="Hardy Day",
        timeZone="Europe/Warsaw"
    ).execute()
    events = events_result.get("items", [])
    for event in events:
        if event.get("summary") == "Hardy Day":
            print(f"Removing existing event on {date.isoformat()}")
            service.events().delete(calendarId=cal_id, eventId=event["id"]).execute()


def create_event(service: Any, cal_id: str, day: datetime.date, description: str) -> None:
    remove_existing_events(service, cal_id, day)

    if isinstance(day, datetime.datetime):
        day = day.date()

    event = {
        "summary": "Hardy Day",
        "description": description,
        "start": {"date": day.isoformat()},
        "end": {"date": (day + datetime.timedelta(days=1)).isoformat()}
    }

    try:
        ev = service.events().insert(calendarId=cal_id, body=event).execute()
        print(f"Created event: {ev['summary']} on {day.isoformat()}")
    except Exception as e:
        print("Failed to create event. Event payload was:")
        print(event)
        raise