import os
import re
import datetime
from dateutil import parser as dtparser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from extractor import GymPlanExtractor

BLOG_URL = "https://www.hardywyzszaforma.pl/blog"
CALENDAR_ID = "a4ac48cba1826f488d829fd46a655cef84ba8eb5757c17a2fd3738cf0d4b7711@group.calendar.google.com"
EVENT_TIME = datetime.time(8, 0)
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    if not os.path.exists("token.json"):
        raise RuntimeError("token.json not found. Run the initial authorization manually.")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("calendar", "v3", credentials=creds)


def event_exists(service, cal_id, dt, summary):
    time_min = dt.isoformat()
    time_max = (dt + datetime.timedelta(hours=2)).isoformat()
    events = service.events().list(
        calendarId=cal_id,
        timeMin=time_min,
        timeMax=time_max,
        timeZone="Europe/Warsaw",
        singleEvents=True
    ).execute().get("items", [])
    for event in events:
        if event.get("summary") == summary:
            return True
    return False


def normalize_type(training_type):
    return training_type.strip().capitalize()


def create_event(service, cal_id, date_str, day_name, block):
    today = datetime.datetime.now()
    dt = dtparser.parse(f"{date_str}.{today.year}", dayfirst=True).date()
    end_date = dt + datetime.timedelta(days=1)

    summary = f"{normalize_type(block['type'])}"

    # if event_exists(service, cal_id, dt, summary):
    #     print(f"Skipping duplicate event: {summary} on {date_str}")
    #     return

    event = {
        "summary": summary,
        "description": (
            f"Ćwiczenia: {block['ex']}\n"
            f"Metoda treningowa: {block['met']}\n"
            f"Czas pracy: {block['dur']}"
        ),
        "start": {"date": dt.isoformat()},
        "end": {"date": end_date.isoformat()}
    }

    ev = service.events().insert(calendarId=cal_id, body=event).execute()
    print(f"Created event: {ev['summary']} on {date_str}")


def main():
    service = get_calendar_service()

    extractor = GymPlanExtractor()
    plans = extractor.get_plans()
    for day in plans:
        for block in day["blocks"]:
            create_event(service, CALENDAR_ID, day["date"], day["day"], block)

        # User manually confirms each plan; process all confirmed plans


if __name__ == "__main__":
    main()
