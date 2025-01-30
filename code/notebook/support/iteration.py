import functools
from collections.abc import Callable, Hashable, Iterable, Sequence


def groupby_custom[K: Hashable, V](values: Iterable[V], by: Callable[[V], K]) -> Iterable[tuple[K, Sequence[V]]]:
    result: dict[K, list[V]] = {}

    for value in values:
        key = by(value)
        result.setdefault(key, [])
        result[key].append(value)

    return result.items()


def iter_accumulator[T, R, **P](collector: Callable[[Iterable[T]], R]) -> Callable[[Callable[P, Iterable[T]]], Callable[P, R]]:
    def decorator(fun: Callable[P, Iterable[T]]) -> Callable[P, R]:
        @functools.wraps(fun)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return collector(fun(*args, **kwargs))

        return wrapper

    return decorator


list_accumulator = iter_accumulator(list)


def string_accumulator[**P](joiner: str = '') -> Callable[[Callable[P, Iterable[str]]], Callable[P, str]]:
    return iter_accumulator(lambda values: joiner.join(values))


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


def repeat[**P, R](n: int, fun: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> Iterable[R]:
    for _ in range(n):
        yield fun(*args, **kwargs)
