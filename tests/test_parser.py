import pytest
from datetime import datetime
from src.hardy_calendar import parser

def test_normalize_description_basic():
    desc = """
    ⇒ Speed\nĆwiczenia: cal SKI, burpee box step\nMetoda treningowa: 2 x 12 min EMOM\nCzas pracy w części głównej: 25 min\n"""
    result = parser.normalize_description(desc)
    # The function preserves line breaks, so check for the expected structure
    assert result.startswith("⇒ Speed\nĆwiczenia: cal SKI, burpee box step")
    assert "Czas pracy" in result

def test_normalize_description_handles_nbsp():
    desc = "⇒ Test\xa0line: value"
    assert "\xa0" not in parser.normalize_description(desc)

def test_normalize_description_multiple_sections():
    desc = "⇒ A: 1\n⇒ B: 2\nCzas: 10"
    result = parser.normalize_description(desc)
    assert result.count("⇒") == 2

def test_normalize_description_empty():
    assert parser.normalize_description("") == ""

def test_parse_weekly_plan_page_extracts_dates_and_descriptions():
    html = '''<html><body>
    03.07 Poniedziałek\n⇒ Speed\nĆwiczenia: cal SKI\nCzas pracy w części głównej: 25 min\n
    04.07 Wtorek\n⇒ Strength\nĆwiczenia: push-up\nCzas pracy w części głównej: 20 min\n
    </body></html>'''
    url = "http://example.com/plan"
    plans = parser.parse_weekly_plan_page(url, html)
    assert len(plans) == 2
    assert any(isinstance(k, datetime) for k in plans)
    assert any("Speed" in v or "Strength" in v for v in plans.values())

def test_parse_weekly_plan_page_handles_no_headers():
    html = "<html><body>No dates here</body></html>"
    url = "http://example.com/plan"
    assert parser.parse_weekly_plan_page(url, html) == {}

def test_parse_weekly_plan_page_handles_malformed_dates():
    html = "<html><body>bad header\n⇒ Desc"  # No valid date
    url = "http://example.com/plan"
    assert parser.parse_weekly_plan_page(url, html) == {}
