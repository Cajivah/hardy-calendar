import pytest
from unittest.mock import patch, MagicMock
from src.hardy_calendar import crawler

BLOG_HTML = '''<html><body>
    <a href="/plan1">Plan treningowy 1</a>
    <a href="/plan2">Plan treningowy 2</a>
    <a href="/other">Other post</a>
</body></html>'''

PLAN_HTML = '<html><body>plan content</body></html>'

@patch('src.hardy_calendar.crawler.requests.get')
def test__get_urls_to_plans(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = BLOG_HTML
    mock_get.return_value.raise_for_status = lambda: None
    urls = crawler._get_urls_to_plans()
    assert urls == ['/plan1', '/plan2']

@patch('src.hardy_calendar.crawler.requests.get')
def test_get_weekly_plan_pages(mock_get):
    # First call: blog page, then two plan pages
    def side_effect(url, *args, **kwargs):
        mock_resp = MagicMock()
        if url == crawler.BLOG_URL:
            mock_resp.text = BLOG_HTML
        else:
            mock_resp.text = f"html for {url}"
        mock_resp.raise_for_status = lambda: None
        return mock_resp
    mock_get.side_effect = side_effect
    pages = crawler.get_weekly_plan_pages()
    assert set(pages.keys()) == {'/plan1', '/plan2'}
    assert pages['/plan1'] == 'html for /plan1'
    assert pages['/plan2'] == 'html for /plan2'

@patch('src.hardy_calendar.crawler.requests.get')
def test_get_weekly_plan_pages_empty(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '<html></html>'
    mock_get.return_value.raise_for_status = lambda: None
    pages = crawler.get_weekly_plan_pages()
    assert pages == {}
