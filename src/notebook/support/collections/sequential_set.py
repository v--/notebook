from collections.abc import Iterable, Iterator, MutableSet

from ..iteration import string_accumulator
from .exceptions import MissingKeyError


class SequentialSetItem[T]:
    value: T
    next: SequentialSetItem[T] | None

    def __init__(self, value: T) -> None:
        self.value = value
        self.next = None


class SequentialSet[T](MutableSet[T]):
    _payload: SequentialSetItem[T] | None

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._payload = None

        if values is None:
            return

        for value in values:
            self.add(value)

    def _iter_items(self) -> Iterator[SequentialSetItem[T]]:
        item = self._payload

        while item:
            yield item
            item = item.next

    def __iter__(self) -> Iterator[T]:
        for item in self._iter_items():
            yield item.value

    def __len__(self) -> int:
        return sum(1 for _ in self._iter_items())

    def __contains__(self, value: object) -> bool:
        return any(item.value == value for item in self._iter_items())

    def __delitem__(self, value: T) -> None:
        if self._payload and self._payload.value == value:
            self._payload = self._payload.next
            return

        for item in self._iter_items():
            if item.next and item.next.value == value:
                item.next = item.next.next
                return

        raise MissingKeyError(value)

    @string_accumulator()
    def __repr__(self) -> Iterable[str]:
        yield 'SequentialSet(['

        for i, item in enumerate(self._iter_items()):
            if i > 0:
                yield ', '

            yield repr(item.value)

        yield '])'

    def add(self, value: T) -> None:
        if self._payload is None:
            self._payload = SequentialSetItem(value)
            return

        for item in self._iter_items():
            if item.value == value:
                return

            if item.next is None:
                item.next = SequentialSetItem(value)

    def discard(self, value: T) -> None:
        del self[value]
