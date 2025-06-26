import os
from typing import Any

from .extractor import get_daily_plans
from .google_calendar import create_event, get_calendar_service

def main() -> None:
    calendarId: str | None = os.environ.get('GOOGLE_CALENDAR_ID')
    service: Any = get_calendar_service()

    plans: dict[str, str] = get_daily_plans()
    for day, description in plans.items():
        create_event(service, calendarId, day, description)

if __name__ == "__main__":
    main()