from collections.abc import ItemsView, Iterator, KeysView, MutableMapping, ValuesView

from ..exceptions import NotebookCodeError


class SequentialMappingError(NotebookCodeError):
    pass


class MissingKeyError(SequentialMappingError, KeyError):
    pass


class KeyExistsError(SequentialMappingError, KeyError):
    pass


class SequentialMappingItem[K, V]:
    key: K
    value: V
    next: 'SequentialMappingItem[K, V] | None'

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.next = None


class SequentialMapping[K, V](MutableMapping[K, V]):
    payload: SequentialMappingItem[K, V] | None

    def __init__(self) -> None:
        self.payload = None

    def _iter_items(self) -> Iterator[SequentialMappingItem[K, V]]:
        current = self.payload

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

    def set(self, key: K, value: V, *, exists_ok: bool = True) -> None:
        if not exists_ok and self.payload and self.payload.key == key:
            raise KeyExistsError(key)

        for item in self._iter_items():
            if item.next and item.next.key == key:
                if exists_ok:
                    item.value = value
                    return

                raise KeyExistsError(key)

            if item.next is None:
                item.next = SequentialMappingItem(key, value)
                return

        self.payload = SequentialMappingItem(key, value)

    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value, exists_ok=True)

    def __delitem__(self, key: K) -> None:
        if self.payload and self.payload.key == key:
            self.payload = self.payload.next
            return

        for item in self._iter_items():
            if item.next and item.next.key == key:
                item.next = item.next.next
                return

        raise MissingKeyError(key)

    def keys(self) -> KeysView[K]:
        return KeysView(self)

    def values(self) -> ValuesView[V]:
        return ValuesView(self)

    def items(self) -> ItemsView[K, V]:
        return ItemsView(self)
