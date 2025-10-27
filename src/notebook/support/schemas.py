from collections.abc import Iterable, Mapping

from .exceptions import NotebookSupportError


class SchemaError(NotebookSupportError):
    pass


class SchemaInstantiationError(SchemaError):
    pass


class SchemaInferenceError(SchemaError):
    pass


def iter_mapping_discrepancy[S, T](a: Mapping[S, T], b: Mapping[S, T]) -> Iterable[tuple[S, tuple[T, T]]]:
    for key, value in a.items():
        if key in b and b[key] != value:
            yield key, (value, b[key])
