import re
import requests
from bs4 import BeautifulSoup
from typing import Dict
from datetime import datetime
import pprint

BLOG_URL = "https://www.hardywyzszaforma.pl/blog"

def _get_urls_to_plans() -> list[str]:
    resp = requests.get(BLOG_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.find_all("a", href=True, string=re.compile(r"Plan treningowy", re.I))
    return [post['href'] for post in posts]


def get_weekly_plan_pages() -> dict[str, str]:
    links = _get_urls_to_plans()
    print(f"Found {len(links)} training plans:\n" + "\n".join(links))
    return {link: requests.get(link).text for link in links}
