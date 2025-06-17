import re
import requests
from bs4 import BeautifulSoup

BLOG_URL = "https://www.hardywyzszaforma.pl/blog"


class GymPlanExtractor:

    def fetch_plan_links(self):
        resp = requests.get(BLOG_URL)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        posts = soup.find_all("a", href=True, text=re.compile(r"Plan treningowy", re.I))
        return [post['href'] for post in posts]

    def get_plans(self):
        for link in self.fetch_plan_links():
            html = requests.get(link).text
            plan = self._parse_plan(html)
            if self._user_confirm_post(plan):
                return plan

    def _user_confirm_post(self, plan):
        print("\n---------- PREVIEW POST ----------")
        print(plan)
        print("\n---------- PREVIEW POST ----------")
        return input("Use this post? [y/n]: ").strip().lower() == 'y'

    def _parse_plan(self, html):
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n")
        date_headers = re.findall(r"(\d{2}\.\d{2})\s+(\w+)", text)
        schedule = []
        header_positions = [
            (m.start(), d, dn)
            for m, (d, dn) in zip(re.finditer(r"(\d{2}\.\d{2})\s+(\w+)", text), date_headers)
        ]
        for i, (pos, date_str, day_name) in enumerate(header_positions):
            end = header_positions[i + 1][0] if i + 1 < len(header_positions) else len(text)
            day_block = text[pos:end]
            blocks = self._parse_day_block(day_block)
            if blocks:
                schedule.append({"date": date_str, "day": day_name, "blocks": blocks})
        return schedule

    def _parse_day_block(self, day_text):
        pattern = (
            r"⇒\s*(?P<type>[^\n:]+)\n"
            r"Ćwiczenia:\s*(?P<ex>[^\n]+)\n"
            r"Metoda treningowa:\s*(?P<met>[^\n]+)\n"
            r"Czas pracy.*?:\s*(?P<dur>[^\n]+)"
        )
        return [m.groupdict() for m in re.finditer(pattern, day_text, re.MULTILINE)]
