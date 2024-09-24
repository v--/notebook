import re


def normalize_pages(pages: str) -> str:
    return re.sub(r'-+', '-', pages)
