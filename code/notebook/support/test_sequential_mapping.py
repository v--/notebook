import pytest

from .sequential_mapping import KeyExistsError, MissingKeyError, SequentialMapping


def test_set_success_duplicate() -> None:
    mapping = SequentialMapping[str, int]()
    mapping['test'] = 3
    mapping['test'] = 3


def test_set_failure_duplicate() -> None:
    mapping = SequentialMapping[str, int]()
    mapping.set('test', 3, exists_ok=False)

    with pytest.raises(KeyExistsError):
        mapping.set('test', 3, exists_ok=False)


def test_set_failure_duplicate_deep() -> None:
    mapping = SequentialMapping[str, int]()
    mapping.set('a', 3, exists_ok=False)
    mapping.set('b', 3, exists_ok=False)

    with pytest.raises(KeyExistsError):
        mapping.set('b', 3, exists_ok=False)


def test_get_success() -> None:
    mapping = SequentialMapping[str, int]()
    mapping['test'] = 3
    assert 'test' in mapping
    assert mapping['test'] == 3
    assert list(mapping.items()) == [('test', 3)]


def test_get_failure() -> None:
    mapping = SequentialMapping[str, int]()

    with pytest.raises(MissingKeyError):
        mapping['test']


def test_get_failsafe() -> None:
    mapping = SequentialMapping[str, int]()
    assert mapping.get('test', None) is None


def test_del_success() -> None:
    mapping = SequentialMapping[str, int]()
    mapping['test'] = 3
    del mapping['test']
    assert 'test' not in mapping
    assert list(mapping.items()) == []


def test_del_success_deep() -> None:
    mapping = SequentialMapping[str, int]()
    mapping['a'] = 3
    mapping['b'] = 3
    del mapping['a']
    assert 'a' not in mapping
    assert 'b' in mapping


def test_del_failure() -> None:
    mapping = SequentialMapping[str, int]()

    with pytest.raises(MissingKeyError):
        del mapping['test']
