import functools
from collections.abc import Callable, Iterable, Sequence


def iter_common_prefix[T](a: Iterable[T], b: Iterable[T]) -> Iterable[T]:
    for x, y in zip(a, b, strict=True):
        if x == y:
            yield x
        else:
            return


def find_common_prefix[T](a: Iterable[T], b: Iterable[T]) -> Sequence[T]:
    return list(iter_common_prefix(a, b))


def find_common_suffix[T](a: Iterable[T], b: Iterable[T]) -> Sequence[T]:
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


def list_accumulator[T, **P](fun: Callable[P, Iterable[T]]) -> Callable[P, Sequence[T]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Sequence[T]:
        return list(fun(*args, **kwargs))

    return wrapper


def frozen_set_accumulator[T, **P](fun: Callable[P, Iterable[T]]) -> Callable[P, frozenset[T]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> frozenset[T]:
        return frozenset(fun(*args, **kwargs))

    return wrapper


def string_accumulator[T, **P](joiner: str = '') -> Callable[[Callable[P, Iterable[T]]], Callable[P, str]]:
    def decorator(fun: Callable[P, Iterable[T]]) -> Callable[P, str]:
        @functools.wraps(fun)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return joiner.join(str(value) for value in fun(*args, **kwargs))

        return wrapper

    return decorator
