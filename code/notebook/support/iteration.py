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


def list_accumulator[R, **P](fun: Callable[P, Iterable[R]]) -> Callable[P, Sequence[R]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Sequence[R]:
        return list(fun(*args, **kwargs))

    return wrapper


def frozen_set_accumulator[R, **P](fun: Callable[P, Iterable[R]]) -> Callable[P, frozenset[R]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> frozenset[R]:
        return frozenset(fun(*args, **kwargs))

    return wrapper


def string_accumulator[**P](joiner: str = '') -> Callable[[Callable[P, Iterable[str]]], Callable[P, str]]:
    def decorator(fun: Callable[P, Iterable[str]]) -> Callable[P, str]:
        @functools.wraps(fun)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return joiner.join(str(value) for value in fun(*args, **kwargs))

        return wrapper

    return decorator


def get_strip_slice[T](seq: Sequence[T], predicate: Callable[[T], bool]) -> slice:
    leading = 0
    trailing = 0

    for item in seq:
        if predicate(item):
            leading += 1
        else:
            break

    for item in reversed(seq):
        if predicate(item):
            trailing += 1
        else:
            break

    return slice(leading, len(seq) - trailing)
