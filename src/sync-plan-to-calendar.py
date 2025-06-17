import os
import re
import datetime
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dtparser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BLOG_URL = "https://www.hardywyzszaforma.pl/blog"
CALENDAR_NAME = "Hardy Plan"
EVENT_TIME = datetime.time(8, 0)
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def fetch_plan_links():
    resp = requests.get(BLOG_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.find_all("a", href=True, text=re.compile(r"Plan treningowy", re.I))
    links = [post['href'] for post in posts]
    return links


def user_confirm_post(html):
    soup = BeautifulSoup(html, "html.parser")
    print("\n---------- PREVIEW POST ----------")
    print(soup.find("h1").text.strip())
    snippet = soup.get_text("\n")[:1000]
    print(snippet)
    print("...\n")
    return input("Use this post? [y/n]: ").strip().lower() == 'y'


def parse_plan(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")
    date_headers = re.findall(r"(\d{2}\.\d{2})\s+(\w+)", text)
    schedule = []
    header_positions = [(m.start(), d, dn) for m, (d, dn) in zip(re.finditer(r"(\d{2}\.\d{2})\s+(\w+)", text), date_headers)]
    for i, (pos, date_str, day_name) in enumerate(header_positions):
        end = header_positions[i+1][0] if i+1 < len(header_positions) else len(text)
        day_block = text[pos:end]
        blocks = parse_day_block(day_block)
        if blocks:
            schedule.append({"date": date_str, "day": day_name, "blocks": blocks})
    return schedule


def parse_day_block(day_text):
    pattern = (
        r"\u21d2\s*(?P<type>[^\n:]+)\n"
        r"\u0106wiczenia:\s*(?P<ex>[^\n]+)\n"
        r"Metoda treningowa:\s*(?P<met>[^\n]+)\n"
        r"Czas pracy.*?:\s*(?P<dur>[^\n]+)"
    )
    return [m.groupdict() for m in re.finditer(pattern, day_text, re.MULTILINE)]


def get_calendar_service():
    creds = None
    if os.path.exists("credentials.json"):
        creds = Credentials.from_authorized_user_file("credentials.json", SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        raise RuntimeError("credentials.json not found. Run the initial authorization manually.")

    return build("calendar", "v3", credentials=creds)


def ensure_calendar(service):
    calendars = service.calendarList().list().execute().get("items", [])
    for cal in calendars:
        if cal.get("summary") == CALENDAR_NAME:
            return cal["id"]
    new = {"summary": CALENDAR_NAME, "timeZone": "Europe/Warsaw"}
    created = service.calendars().insert(body=new).execute()
    return created["id"]


def event_exists(service, cal_id, dt, summary):
    time_min = dt.isoformat()
    time_max = (dt + datetime.timedelta(hours=2)).isoformat()
    events = service.events().list(calendarId=cal_id, timeMin=time_min, timeMax=time_max).execute().get("items", [])
    for event in events:
        if event.get("summary") == summary:
            return True
    return False


def create_event(service, cal_id, date_str, day_name, block):
    today = datetime.datetime.now()
    dt = dtparser.parse(f"{date_str}.{today.year} 08:00", dayfirst=True)
    duration_min = int(re.search(r"(\d+)", block["dur"]).group(1))
    end = dt + datetime.timedelta(minutes=duration_min)
    summary = f"{day_name} – {block['type']}"
    if event_exists(service, cal_id, dt, summary):
        print(f"Skipping duplicate event: {summary} on {date_str}")
        return
    event = {
        "summary": summary,
        "description": (
            f"Ćwiczenia: {block['ex']}\n"
            f"Metoda: {block['met']}\n"
            f"Czas główny: {block['dur']}"
        ),
        "start": {"dateTime": dt.isoformat(), "timeZone": "Europe/Warsaw"},
        "end": {"dateTime": end.isoformat(), "timeZone": "Europe/Warsaw"}
    }
    ev = service.events().insert(calendarId=cal_id, body=event).execute()
    print(f"Created event: {ev['summary']} on {date_str}")


def main():
    service = get_calendar_service()
    cal_id = ensure_calendar(service)
    print(f"Using calendar ID: {cal_id}")

    for link in fetch_plan_links():
        html = requests.get(link).text
        if user_confirm_post(html):
            schedule = parse_plan(html)
            for day in schedule:
                for block in day["blocks"]:
                    create_event(service, cal_id, day["date"], day["day"], block)
            break


if __name__ == "__main__":
    main()
