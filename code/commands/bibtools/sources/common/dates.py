import re


def extract_year(date: str | None) -> str | None:
    year_match = date and re.match(r'(?P<year>\d{4})', date)
    return year_match.group('year') if year_match else None
