from .....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from .names import get_main_human_name, normalize_human_name


@pytest_parametrize_lists(
    full_name=[
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


@pytest_parametrize_kwargs(
    dict(
        main='Андрей Николаевич',
        other='Колмогоров'
    ),
    dict(
        main='Георгий Георгиевич',
        other='Магарил-Ильяев'
    ),
    dict(
        main='Saunders',
        other='Mac Lane'
    ),
    dict(
        main='Jan',
        other='von Plato'
    )
)
def test_normalize_human_name_last_first(other: str, main: str) -> None:
    assert normalize_human_name(f'{other} {main}') == f'{other} {main}'
    assert normalize_human_name(f'{main}, {other}') == f'{other} {main}'


@pytest_parametrize_kwargs(
    dict(
        full_name='Андрей Николаевич Колмогоров',
        main='Колмогоров'
    ),
    dict(
        full_name='Георгий Георгиевич Магарил-Ильяев',
        main='Магарил-Ильяев'
    ),
    dict(
        full_name='Saunders Mac Lane',
        main='Mac Lane'
    ),
    dict(
        full_name='Jan von Plato',
        main='von Plato'
    ),
    dict(
        full_name='J. Author Seebach Jr.',
        main='Seebach'
    ),
    dict(
        full_name='Charles Staats III',
        main='Staats'
    ),
    dict(
        full_name='Euclid of Alexandria',
        main='Euclid of Alexandria'
    )
)
def test_get_main_human_name(full_name: str, main: str) -> None:
    assert get_main_human_name(full_name) == main
