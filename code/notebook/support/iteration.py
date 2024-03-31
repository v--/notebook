import functools
from collections.abc import Callable, Iterable
from typing import ParamSpec, TypeVar


T = TypeVar('T')
P = ParamSpec('P')


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


def list_accumulator(fun: Callable[P, Iterable[T]]) -> Callable[P, list[T]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> list[T]:
        return list(fun(*args, **kwargs))

    return wrapper


def string_accumulator(joiner: str = '') -> Callable[[Callable[P, Iterable[T]]], Callable[P, str]]:
    def decorator(fun: Callable[P, Iterable[T]]) -> Callable[P, str]:
        @functools.wraps(fun)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return ''.join(str(value) for value in fun(*args, **kwargs))

        return wrapper

    return decorator
