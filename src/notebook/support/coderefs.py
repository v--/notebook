import inspect
from collections.abc import Callable, Iterator, Mapping, MutableMapping
from dataclasses import dataclass


def determine_calling_function() -> Callable | None:
    call_stack = inspect.stack()

    for frame_info in call_stack[1:]:
        if mod := inspect.getmodule(frame_info.frame):
            try:
                value = getattr(mod, frame_info.function)
            except AttributeError:
                continue

            if inspect.getmodule(value) == mod and mod.__name__.startswith('notebook.math'):
                return value

    return None


@dataclass
class DictMetadataProxy[K, V](Mapping[K, V]):
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

    def ref_inline[T](self, doc_ref: str) -> None:
        if calling := determine_calling_function():
            self.mapping[doc_ref] = calling

    def ref_proxy[T](self, doc_ref: str, **kwargs: T) -> Mapping[str, T]:
        return DictMetadataProxy(self, doc_ref, dict(**kwargs))


collector = CodeRefCollector()
