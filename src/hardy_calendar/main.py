import os
from typing import Any
from datetime import datetime

from .parser import parse_weekly_plan_page
from .crawler import get_weekly_plan_pages
from .google_calendar import create_event, get_calendar_service

def main() -> None:
    calendarId: str | None = os.environ.get('GOOGLE_CALENDAR_ID')
    service: Any = get_calendar_service()

    pages: dict[str, str] = get_weekly_plan_pages()
    # Parse each page and flatten all dicts into one dict
    all_plans = {k: v for url, html in pages.items() for k, v in parse_weekly_plan_page(url, html).items()}
    for day, description in all_plans.items():
        create_event(service, calendarId, day, description)

if __name__ == "__main__":
    main()