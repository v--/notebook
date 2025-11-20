import pytest

from .exceptions import MissingKeyError
from .trie_mapping import TrieMapping


def test_get_subtrie() -> None:
    trie = TrieMapping({'': 0, 'a': 1, 'ab': 2})
    assert trie.get_subtrie('') == trie
    assert trie.get_subtrie('a') == TrieMapping({'': 1, 'b': 2})
    assert trie.get_subtrie('ab') == TrieMapping({'': 2})


def test_get_success() -> None:
    trie = TrieMapping({'a': 1})
    assert 'a' in trie
    assert trie['a'] == 1
    assert list(trie.items()) == [('a', 1)]


def test_get_failure() -> None:
    trie = TrieMapping[int]()

    with pytest.raises(MissingKeyError):
        trie['a']


def test_partial_match() -> None:
    trie = TrieMapping({'ab': 1})

    with pytest.raises(MissingKeyError):
        trie['a']


def test_del_success() -> None:
    trie = TrieMapping({'a': 1})
    del trie['a']
    assert 'a' not in trie
    assert list(trie.items()) == []


def test_del_nested_success() -> None:
    trie = TrieMapping({'a': 1, 'ab': 2})
    del trie['ab']
    assert 'a' in trie


def test_del_failure() -> None:
    trie = TrieMapping[int]()

    with pytest.raises(MissingKeyError):
        del trie['a']


def test_repr() -> None:
    trie = TrieMapping({'': 0, 'a': 1, 'ab': 2})
    assert repr(trie) == "TrieMapping({'': 0, 'a': 1, 'ab': 2})"
