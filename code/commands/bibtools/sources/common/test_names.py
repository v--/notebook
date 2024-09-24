import pytest

from .names import get_main_human_name, normalize_human_name


@pytest.mark.parametrize(
    'full_name',
    [
        'Андрей Николаевич Колмогоров',
        'Георгий Георгиевич Магарил-Ильяев',
        'Saunders Mac Lane',
        'Jan von Plato',
        'J. Author Seebach Jr.',
        'Charles Staats III',
        'Euclid of Alexandria'
    ]
)
def test_normalize_human_name_noop(full_name: str) -> None:
    assert normalize_human_name(full_name) == full_name


@pytest.mark.parametrize(
    ('first', 'last'),
    [
        ('Колмогоров', 'Андрей Николаевич'),
        ('Магарил-Ильяев', 'Георгий Георгиевич'),
        ('Mac Lane', 'Saunders'),
        ('von Plato', 'Jan')
    ]
)
def test_normalize_human_name_last_first(first: str, last: str) -> None:
    assert normalize_human_name(f'{first} {last}') == f'{first} {last}'
    assert normalize_human_name(f'{last}, {first}') == f'{first} {last}'


@pytest.mark.parametrize(
    ('full_name', 'main'),
    [
        ('Андрей Николаевич Колмогоров', 'Колмогоров'),
        ('Георгий Георгиевич Магарил-Ильяев', 'Магарил-Ильяев'),
        ('Saunders Mac Lane', 'Mac Lane'),
        ('Jan von Plato', 'von Plato'),
        ('J. Author Seebach Jr.', 'Seebach'),
        ('Charles Staats III', 'Staats'),
        ('Euclid of Alexandria', 'Euclid of Alexandria')
    ]
)
def test_get_main_human_name(full_name: str, main: str) -> None:
    assert get_main_human_name(full_name) == main
