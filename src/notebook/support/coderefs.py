from collections.abc import Callable, Iterator, Mapping, MutableMapping
from dataclasses import dataclass


@dataclass
class DictMetadataProxy[K, V](Mapping[K, V]):
    """This proxy is used by `pytest_parametrize_kwargs` to put the appropriate function into the collector."""

    collector: CodeRefCollector
    doc_ref: str
    subject: Mapping[K, V]

    def __getitem__(self, key: K) -> V:
        return self.subject[key]

    def __contains__(self, key: object) -> bool:
        return key in self.subject

    def __len__(self) -> int:
        return len(self.subject)

    def __iter__(self) -> Iterator[K]:
        return iter(self.subject)


class CodeRefCollector:
    mapping: MutableMapping[str, Callable]

    def __init__(self) -> None:
        self.mapping = {}

    def ref[R, **P](self, doc_ref: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def decorator(fun: Callable[P, R]) -> Callable[P, R]:
            self.mapping[doc_ref] = fun
            return fun

        return decorator

    def ref_proxy[T](self, doc_ref: str, *args: Mapping[str, T]) -> Iterator[Mapping[str, T]]:
        for mapping in args:
            yield DictMetadataProxy(self, doc_ref, mapping)


collector = CodeRefCollector()
