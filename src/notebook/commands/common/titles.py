from typing import Any

from titlecase import titlecase


def titlecase_callback(string: str, **kwargs: Any) -> str | None:  # noqa: ANN401,ARG001
    if not string.isascii() or string == string.upper():
        return string

    return None


def title_case(string: str) -> str:
    """Something more intelligent than python's str.title()."""
    return titlecase(string, callback=titlecase_callback)


def is_title_case(string: str) -> bool:
    return title_case(string) == string
