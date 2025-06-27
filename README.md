# hardy-calendar

This project crawls Hardy's website to find upcoming training schedules and creates events out of them in a Google Calendar. 

It's meant to be run periodically, not reactively, so mind the delay. CRON is set in [github actions](.github/workflows/crawler.yml) to run it every 6 hours.

The calendar is available there: [Google Calendar](https://calendar.google.com/calendar/embed?src=a4ac48cba1826f488d829fd46a655cef84ba8eb5757c17a2fd3738cf0d4b7711%40group.calendar.google.com&ctz=Africa%2FCeuta)

## Dependencies

- Python 3.12+
- Poetry

## Env Variables
- `GOOGLE_API_CREDENTIALS`: It's a JSON file with keys from Google Cloud Console with the Calendar API enabled. It's generated for a service account that needs to have access to the calendar. Google it.
- `GOOGLE_CALENDAR_ID`: The ID of the calendar where the events will be created. It can be found in the calendar settings in Google Calendar.

## Usage

```bash
poetry install
poetry run pytest
poetry run hardy-calendar
```

