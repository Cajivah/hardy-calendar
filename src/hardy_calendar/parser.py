import re
from bs4 import BeautifulSoup
from typing import Dict
from datetime import datetime
import pprint

BLOG_URL = "https://www.hardywyzszaforma.pl/blog"

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


def parse_date_from_header(date_str: str) -> datetime:
    # Parse date (assume current year) - remove spaces around dot first
    clean_date_str = re.sub(r'\s*\.\s*', '.', date_str)
    day, month = map(int, clean_date_str.split('.'))
    # It won't work for the first week of January but...
    year = datetime.now().year
    return datetime(year, month, day)


def parse_weekly_plan_page(url: str, html: str) -> Dict[datetime, str]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")
    header_pattern = re.compile(r"(\d{2}\s*\.\s*\d{2})\s+(\w+)", re.UNICODE)
    headers = [(m.start(), m.group(1), m.group(0)) for m in header_pattern.finditer(text)]
    result: Dict[datetime, str] = {}
    for i, (pos, date_str, header) in enumerate(headers):
        end = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        description = text[pos:end].strip()
        description = description[len(header):].strip()
        description = normalize_description(description)
        # Add source and feedback links
        description += f"\n\nSource: {url}\nGot questions? Ideas? Come here: https://github.com/cajivah/hardy-calendar/issues"
        
        date = parse_date_from_header(date_str)
        result[date] = description
    return result
