from collections.abc import Iterable, Iterator, Mapping, MutableMapping, MutableSequence
from typing import NamedTuple

from ..iteration import string_accumulator
from .exceptions import MissingKeyError


class TrieMappingNode[T](NamedTuple):
    head: str
    subtrie: TrieMapping[T]


class TrieMapping[T](MutableMapping[str, T]):
    _payload: MutableSequence[TrieMappingNode[T]]
    _value: T | None

    def __init__(self, items: Mapping[str, T] | Iterable[tuple[str, T]] | None = None) -> None:
        self._payload = []
        self._value = None

        if items is None:
            return

        items_iter = items.items() if isinstance(items, Mapping) else items

        for key, value in items_iter:
            self[key] = value

    def get_subtrie(self, key: str) -> TrieMapping[T]:
        if key == '':
            return self

        head = key[0]
        tail = key[1:]

        for subtrie_head, subtrie in self._payload:
            if subtrie_head != head:
                continue

            try:
                return subtrie.get_subtrie(tail)
            except MissingKeyError:
                continue

        raise MissingKeyError(key)

    def matches_empty_string(self) -> bool:
        return self._value is not None

    def is_empty(self) -> bool:
        return self._value is None and len(self._payload) == 0

    def __getitem__(self, key: str) -> T:
        subtrie = self.get_subtrie(key)
        value = subtrie._value  # noqa: SLF001

        if value is None:
            raise MissingKeyError(key)

        return value

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return NotImplemented

        try:
            self.get_subtrie(key)
        except MissingKeyError:
            return False
        else:
            return True

    def __len__(self) -> int:
        return len(self._payload) + sum(len(subtrie) for _, subtrie in self._payload)

    def __iter__(self) -> Iterator[str]:
        if self._value is not None:
            yield ''

        for head, subtrie in self._payload:
            for substring in subtrie:
                yield head + substring

    def __setitem__(self, key: str, value: T) -> None:
        if key == '':
            self._value = value
            return

        head = key[0]
        tail = key[1:]

        try:
            subtrie = next(subtrie for subtrie_head, subtrie in self._payload if subtrie_head == head)
        except StopIteration:
            subtrie = TrieMapping()
            self._payload.append(TrieMappingNode(head, subtrie))

        subtrie[tail] = value

    def __delitem__(self, key: str) -> None:
        if key == '':
            self._value = None
            return

        head = key[0]
        tail = key[1:]

        for i, (subtrie_head, subtrie) in enumerate(self._payload):
            if subtrie_head != head:
                continue

            try:
                del subtrie[tail]
            except MissingKeyError:
                continue
            else:
                if subtrie.is_empty():
                    del self._payload[i]

                return

        raise MissingKeyError(key)

    @string_accumulator()
    def __repr__(self) -> Iterable[str]:
        yield 'TrieMapping({'

        for i, (key, value) in enumerate(self.items()):
            if i > 0:
                yield ', '

            yield repr(key)
            yield ': '
            yield repr(value)

        yield '})'
