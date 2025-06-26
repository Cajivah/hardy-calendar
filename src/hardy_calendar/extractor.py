import re
import requests
from bs4 import BeautifulSoup
from typing import Dict
from datetime import datetime

BLOG_URL = "https://www.hardywyzszaforma.pl/blog"

def _fetch_plan_links() -> list[str]:
    resp = requests.get(BLOG_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.find_all("a", href=True, text=re.compile(r"Plan treningowy", re.I))
    return [post['href'] for post in posts]


def normalize_description(description: str) -> str:
    # Replace non-breaking spaces with regular spaces
    text = description.replace('\xa0', ' ')
    
    # First, split on ⇒ to handle each section separately
    parts = text.split('⇒')
    
    # Process the first part (before any ⇒)
    if parts[0].strip():
        # If there's content before the first ⇒, keep it
        result_parts = [parts[0].strip()]
    else:
        result_parts = []
    
    # Process each section that starts with ⇒
    for i, part in enumerate(parts[1:], 1):
        # Clean up this section
        section = part.strip()
        
        # Remove newlines after colons and replace with single space
        section = re.sub(r':\s*\n\s*', ': ', section)
        # Remove newlines before colons
        section = re.sub(r'\s*\n\s*:', ': ', section)
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
        
        # Rejoin the lines for this section
        clean_section = '\n'.join(lines)
        
        # Add the ⇒ back and add to results
        result_parts.append('⇒ ' + clean_section)
    
    # Join all parts with double newlines (blank line between sections)
    return '\n\n'.join(result_parts)


def _parse_plan(html: str) -> Dict[datetime, str]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")
    header_pattern = re.compile(r"(\d{2}\.\d{2})\s+(\w+)", re.UNICODE)
    headers = [(m.start(), m.group(1), m.group(0)) for m in header_pattern.finditer(text)]
    result: Dict[datetime, str] = {}
    for i, (pos, date_str, header) in enumerate(headers):
        end = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        description = text[pos:end].strip()
        description = description[len(header):].strip()
        # Parse date (assume current year)
        day, month = map(int, date_str.split('.'))
        # It won't work for the first week of January but...
        year = datetime.now().year
        date_obj = datetime(year, month, day)
        result[date_obj] = normalize_description(description)
    return result


def get_daily_plans() -> Dict[datetime, str]:
    all_plans = {}
    for link in _fetch_plan_links():
        html = requests.get(link).text
        with open("plan.html", "w", encoding="utf-8") as f:
            f.write(html)
        plan = _parse_plan(html)
        all_plans.update(plan)
    return all_plans
