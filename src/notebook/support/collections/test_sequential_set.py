import pytest

from .exceptions import MissingKeyError
from .sequential_set import SequentialSet


def test_add() -> None:
    ss = SequentialSet[int]()
    ss.add(3)
    assert 3 in ss


def test_add_multiple() -> None:
    ss = SequentialSet[int]()
    ss.add(3)
    ss.add(4)
    assert 3 in ss
    assert 4 in ss


def test_uniqueness() -> None:
    ss = SequentialSet[int]()
    ss.add(3)
    ss.add(3)
    assert list(ss) == [3]


def test_del_success() -> None:
    ss = SequentialSet[int]()
    ss.add(3)
    del ss[3]
    assert 3 not in ss


def test_del_success_deep() -> None:
    ss = SequentialSet[int]()
    ss.add(3)
    ss.add(4)
    del ss[4]
    assert 4 not in ss


def test_del_failure() -> None:
    ss = SequentialSet[int]()

    with pytest.raises(MissingKeyError):
        del ss[3]


def test_repr() -> None:
    ss = SequentialSet[int]()
    ss.add(3)
    ss.add(4)
    assert repr(ss) == 'SequentialSet([3, 4])'
