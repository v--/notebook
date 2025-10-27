from .....support.pytest import pytest_parametrize_kwargs
from .dates import extract_year


@pytest_parametrize_kwargs(
    dict(
        string='2000',
        year='2000'
    ),
    dict(
        string='Левенштейн1965',
        year='1965'
    ),
    dict(
        string='Левенштейн1965ДвоичныеКоды',
        year='1965'
    ),
    dict(
        string='0149.15905',
        year='0149'
    ),
    dict(
        string='Основы теории меры. Том 1-РХД (2003)',
        year='2003'
    )
)
def test_extract_year(string: str, year: str) -> None:
    assert extract_year(string) == year


def test_extract_year_longer() -> None:
    assert extract_year('dan31411') is None

