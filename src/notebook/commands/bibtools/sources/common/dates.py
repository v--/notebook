import re
from datetime import datetime


def extract_year(date: str | None) -> str | None:
    if date and (year_match := re.search(r'([^\d]+|^)(?P<year>\d{4})([^\d]+|$)', date)):
        return year_match.group('year')

    return None


def to_iso_date(datetime_: datetime) -> str:
    return datetime_.strftime('%Y-%m-%d')
