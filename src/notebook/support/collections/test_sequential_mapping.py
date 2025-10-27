import pytest

from .exceptions import MissingKeyError
from .sequential_mapping import SequentialMapping


def test_get_success() -> None:
    mapping = SequentialMapping({'a': 3})
    assert 'a' in mapping
    assert mapping['a'] == 3
    assert list(mapping.items()) == [('a', 3)]


def test_get_failure() -> None:
    mapping = SequentialMapping[str, int]()

    with pytest.raises(MissingKeyError):
        mapping['a']


def test_get_failsafe() -> None:
    mapping = SequentialMapping[str, int]()
    assert mapping.get('a', None) is None


def test_del_success() -> None:
    mapping = SequentialMapping({'a': 3})
    del mapping['a']
    assert 'a' not in mapping
    assert list(mapping.items()) == []


def test_del_success_deep() -> None:
    mapping = SequentialMapping({'a': 3, 'b': 4})
    del mapping['a']
    assert 'a' not in mapping
    assert 'b' in mapping


def test_del_failure() -> None:
    mapping = SequentialMapping[str, int]()

    with pytest.raises(MissingKeyError):
        del mapping['a']


def test_repr() -> None:
    mapping = SequentialMapping({'a': 3, 'b': 4})
    assert repr(mapping) == "SequentialMapping([('a', 3), ('b', 4)])"
