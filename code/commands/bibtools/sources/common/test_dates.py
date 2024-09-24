import pytest

from .dates import extract_year


@pytest.mark.parametrize(
    ('string', 'year'),
    [
        ('2000', '2000'),
        ('Левенштейн1965', '1965'),
        ('Левенштейн1965ДвоичныеКоды', '1965'),
        ('0149.15905', '0149')
    ]
)
def test_extract_year(string: str, year: str) -> None:
    assert extract_year(string) == year


def test_extract_year_longer() -> None:
    assert extract_year('dan31411') is None

