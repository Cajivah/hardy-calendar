from typing import Any
from datetime import datetime
import json

from .parser import parse_weekly_plan_page
from .crawler import get_weekly_plan_pages
from .google_calendar import create_event, get_calendar_service

def save_plans_to_file(plans: dict[datetime, str]) -> None:
    with open("plans.json", "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in plans.items()}, f, ensure_ascii=False, indent=2)

def crawl_and_sync(dry_run: bool) -> None:
    service: Any = get_calendar_service()

    pages: dict[str, str] = get_weekly_plan_pages()
    # Parse each page and flatten all dicts into one dict
    all_plans: dict[datetime, str] = {k: v for url, html in pages.items() for k, v in parse_weekly_plan_page(url, html).items()}

    save_plans_to_file(all_plans)

    if dry_run:
        print("[DRY RUN] plans.json artifact written, skipping event creation.")
        return

    for day, description in all_plans.items():
        create_event(service, day, description)