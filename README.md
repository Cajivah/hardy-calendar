# hardy-calendar

This project crawls Hardy's website to find upcoming training schedules and creates events out of them in a Google Calendar. 

It's meant to be run periodically, not reactively, so mind the delay. CRON is set in [github actions](.github/workflows/crawler.yml) to run it every 6 hours.

## Dependencies

- Python 3.12+
- Poetry

## Env Variables
- `GOOGLE_API_CREDENTIALS`: It's a JSON file with keys from Google Cloud Console with the Calendar API enabled. It's generated for a service account that needs to have access to the calendar. Google it.
- `GOOGLE_CALENDAR_ID`: The ID of the calendar where the events will be created. It can be found in the calendar settings in Google Calendar.

## Usage

```bash
poetry install
poetry run hardy-calendar
```
