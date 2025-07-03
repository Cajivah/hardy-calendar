import unittest
from unittest.mock import MagicMock
import datetime
from src.hardy_calendar import google_calendar

class TestGoogleCalendar(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        self.cal_id = "test_cal_id"
        self.day = datetime.date(2025, 7, 3)
        self.description = "Test event description"

    def test_day_to_summary(self):
        self.assertEqual(google_calendar.day_to_summary(self.day), "Hardy 03.07")
        self.assertEqual(google_calendar.day_to_summary(datetime.date(2025, 1, 1)), "Hardy 01.01")

    def test_remove_existing_events_none(self):
        # No events to remove
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": []}
        google_calendar.remove_existing_events(self.mock_service, self.cal_id, self.day)
        self.mock_service.events.return_value.delete.assert_not_called()

    def test_remove_existing_events_one(self):
        # One matching event
        event = {"id": "abc", "summary": google_calendar.day_to_summary(self.day)}
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": [event]}
        google_calendar.remove_existing_events(self.mock_service, self.cal_id, self.day)
        self.mock_service.events.return_value.delete.assert_called_once_with(calendarId=self.cal_id, eventId="abc")

    def test_remove_existing_events_multiple(self):
        # Multiple events, only matching summary should be deleted
        event1 = {"id": "abc", "summary": google_calendar.day_to_summary(self.day)}
        event2 = {"id": "def", "summary": "Other summary"}
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": [event1, event2]}
        google_calendar.remove_existing_events(self.mock_service, self.cal_id, self.day)
        self.mock_service.events.return_value.delete.assert_called_once_with(calendarId=self.cal_id, eventId="abc")

    def test_create_event_success(self):
        # No existing events, event is created
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": []}
        self.mock_service.events.return_value.insert.return_value.execute.return_value = {"summary": "Hardy 03.07"}
        google_calendar.create_event(self.mock_service, self.cal_id, self.day, self.description)
        self.mock_service.events.return_value.insert.assert_called_once()

    def test_create_event_removes_existing(self):
        # Existing event is removed before creating new one
        event = {"id": "abc", "summary": google_calendar.day_to_summary(self.day)}
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": [event]}
        self.mock_service.events.return_value.insert.return_value.execute.return_value = {"summary": "Hardy 03.07"}
        google_calendar.create_event(self.mock_service, self.cal_id, self.day, self.description)
        self.mock_service.events.return_value.delete.assert_called_once_with(calendarId=self.cal_id, eventId="abc")
        self.mock_service.events.return_value.insert.assert_called_once()

    def test_create_event_with_datetime(self):
        # Accepts datetime.datetime as day
        dt = datetime.datetime(2025, 7, 3, 12, 0)
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": []}
        self.mock_service.events.return_value.insert.return_value.execute.return_value = {"summary": "Hardy 03.07"}
        google_calendar.create_event(self.mock_service, self.cal_id, dt, self.description)
        args, kwargs = self.mock_service.events.return_value.insert.call_args
        self.assertEqual(kwargs["body"]["start"], {"date": "2025-07-03"})
        self.assertEqual(kwargs["body"]["end"], {"date": "2025-07-04"})

    def test_create_event_raises_on_insert_error(self):
        # Insert raises exception
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": []}
        self.mock_service.events.return_value.insert.return_value.execute.side_effect = Exception("API error")
        with self.assertRaises(Exception):
            google_calendar.create_event(self.mock_service, self.cal_id, self.day, self.description)

    def test_create_event_raises_on_delete_error(self):
        # Delete raises exception
        event = {"id": "abc", "summary": google_calendar.day_to_summary(self.day)}
        self.mock_service.events.return_value.list.return_value.execute.return_value = {"items": [event]}
        self.mock_service.events.return_value.delete.return_value.execute.side_effect = Exception("Delete error")
        with self.assertRaises(Exception):
            google_calendar.create_event(self.mock_service, self.cal_id, self.day, self.description)

    def test_remove_existing_events_handles_no_items_key(self):
        # No 'items' key in response
        self.mock_service.events.return_value.list.return_value.execute.return_value = {}
        google_calendar.remove_existing_events(self.mock_service, self.cal_id, self.day)
        self.mock_service.events.return_value.delete.assert_not_called()

if __name__ == "__main__":
    unittest.main()