import re
import requests
from bs4 import BeautifulSoup
from typing import Dict
from datetime import datetime
import pprint

BLOG_URL = "https://www.hardywyzszaforma.pl/blog"

def _fetch_plan_links() -> list[str]:
    resp = requests.get(BLOG_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.find_all("a", href=True, text=re.compile(r"Plan treningowy", re.I))
    return [post['href'] for post in posts]


def normalize_description(description: str) -> str:
    text = description.replace('\xa0', ' ')
    parts = text.split('⇒')
    result_parts = []

    for part in parts[1:]:
        section = part.strip()
        # Remove newlines after colons and replace with single space
        section = re.sub(r':\s*\n\s*', ': ', section)
        # Remove newlines before colons
        section = re.sub(r'\s*\n\s*:', ':', section)
        # Remove spaces before colons
        section = re.sub(r'\s+:', ':', section)
        # Remove multiple spaces
        section = re.sub(r' +', ' ', section)
        # Split into lines and clean each line
        lines = []
        for line in section.splitlines():
            line = line.strip()
            if line:
                lines.append(line)
            if line.lower().startswith("czas"):
                break
        if lines:
            clean_section = '\n'.join(lines)
            result_parts.append('⇒ ' + clean_section)

    return '\n\n'.join(result_parts)


def _parse_plan(html: str) -> Dict[datetime, str]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")
    header_pattern = re.compile(r"(\d{2}\s*\.\s*\d{2})\s+(\w+)", re.UNICODE)
    headers = [(m.start(), m.group(1), m.group(0)) for m in header_pattern.finditer(text)]
    result: Dict[datetime, str] = {}
    for i, (pos, date_str, header) in enumerate(headers):
        end = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        description = text[pos:end].strip()
        description = description[len(header):].strip()
        # Parse date (assume current year) - remove spaces around dot first
        clean_date_str = re.sub(r'\s*\.\s*', '.', date_str)
        day, month = map(int, clean_date_str.split('.'))
        # It won't work for the first week of January but...
        year = datetime.now().year
        date_obj = datetime(year, month, day)
        result[date_obj] = normalize_description(description)
    return result


def get_daily_plans() -> Dict[datetime, str]:
    all_plans = {}
    links = _fetch_plan_links()
    print(f"Found {len(links)} training plans:\n" + "\n".join(links))

    for link in links:
        html = requests.get(link).text
        plan = _parse_plan(html)
        all_plans.update(plan)

    print(f"Extracted {len(all_plans)} daily plans.")
    pprint.pprint(all_plans)
    
    return all_plans
