from collections.abc import ItemsView, Iterable, Iterator, KeysView, Mapping, MutableMapping, ValuesView

from ..iteration import string_accumulator
from .exceptions import MissingKeyError


class SequentialMappingItem[K, V]:
    key: K
    value: V
    next: 'SequentialMappingItem[K, V] | None'

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.next = None


class SequentialMapping[K, V](MutableMapping[K, V]):
    _payload: SequentialMappingItem[K, V] | None

    def __init__(self, items: Mapping[K, V] | Iterable[tuple[K, V]] | None = None) -> None:
        self._payload = None

        if items is None:
            return

        items_iter = items.items() if isinstance(items, Mapping) else items

        for key, value in items_iter:
            self[key] = value

    def _iter_items(self) -> Iterator[SequentialMappingItem[K, V]]:
        current = self._payload

        while current:
            yield current
            current = current.next

    def __iter__(self) -> Iterator[K]:
        for item in self._iter_items():
            yield item.key

    def __len__(self) -> int:
        return sum(1 for _ in self._iter_items())

    def __getitem__(self, key: K) -> V:
        for item in self._iter_items():
            if item.key == key:
                return item.value

        raise MissingKeyError(key)

    def __contains__(self, key: object) -> bool:
        return any(item.key == key for item in self._iter_items())

    def __setitem__(self, key: K, value: V) -> None:
        for item in self._iter_items():
            if item.next and item.next.key == key:
                item.value = value
                return

            if item.next is None:
                item.next = SequentialMappingItem(key, value)
                return

        self._payload = SequentialMappingItem(key, value)

    def __delitem__(self, key: K) -> None:
        if self._payload and self._payload.key == key:
            self._payload = self._payload.next
            return

        for item in self._iter_items():
            if item.next and item.next.key == key:
                item.next = item.next.next
                return

        raise MissingKeyError(key)

    @string_accumulator()
    def __repr__(self) -> Iterable[str]:
        yield 'SequentialMapping(['

        for i, item in enumerate(self._iter_items()):
            if i > 0:
                yield ', '

            yield '('
            yield repr(item.key)
            yield ', '
            yield repr(item.value)
            yield ')'

        yield '])'

    def keys(self) -> KeysView[K]:
        return KeysView(self)

    def values(self) -> ValuesView[V]:
        return ValuesView(self)

    def items(self) -> ItemsView[K, V]:
        return ItemsView(self)
