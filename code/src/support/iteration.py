from typing import Iterable, TypeVar


T = TypeVar('T')


def iter_common_prefix(a: Iterable[T], b: Iterable[T]) -> Iterable[T]:
    for x, y in zip(a, b):
        if x == y:
            yield x
        else:
            return


def find_common_prefix(a: Iterable[T], b: Iterable[T]) -> list[T]:
    return list(iter_common_prefix(a, b))


def find_common_suffix(a: Iterable[T], b: Iterable[T]) -> list[T]:
    return list(
        reversed(
            list(
                find_common_prefix(
                    reversed(list(a)),
                    reversed(list(b))
                )
            )
        )
    )
