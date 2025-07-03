import os
from typing import Any
from datetime import datetime
import json

from .parser import parse_weekly_plan_page
from .crawler import get_weekly_plan_pages
from .google_calendar import create_event, get_calendar_service

def main() -> None:
    calendarId: str | None = os.environ.get('GOOGLE_CALENDAR_ID')
    service: Any = get_calendar_service()

    pages: dict[str, str] = get_weekly_plan_pages()
    # Parse each page and flatten all dicts into one dict
    all_plans = {k: v for url, html in pages.items() for k, v in parse_weekly_plan_page(url, html).items()}

    with open("plans.json", "w", encoding="utf-8") as f:
        json.dump(all_plans, f, ensure_ascii=False, indent=2)

    dry_run = os.environ.get("DRY_RUN", "0") == "1"
    if dry_run:
        print("[DRY RUN] plans.json artifact written, skipping event creation.")
        return

    for day, description in all_plans.items():
        create_event(service, calendarId, day, description)

if __name__ == "__main__":
    main()