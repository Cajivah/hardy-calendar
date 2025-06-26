from extractor import get_daily_plans
from google_calendar import create_event

def main():
    calendarId = os.environ.get('GOOGLE_CALENDAR_ID')
    service = get_calendar_service()

    plans = get_daily_plans()
    for day in plans:
        create_event(service, calendarId, day)


if __name__ == "__main__":
    main()