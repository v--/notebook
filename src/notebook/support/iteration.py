import functools
from collections.abc import Callable, Collection, Hashable, Iterable, Mapping, Sequence


def power_set[T](base_set: Collection[T]) -> Collection[Collection[T]]:
    if len(base_set) == 0:
        return frozenset([frozenset()])

    head, *tail = base_set
    subset_power = power_set(tail)
    return frozenset((*subset_power, *(frozenset((*subset, head)) for subset in subset_power)))


def groupby_custom[K: Hashable, V](values: Iterable[V], by: Callable[[V], K]) -> Iterable[tuple[K, Sequence[V]]]:
    result: dict[K, list[V]] = {}

    for value in values:
        key = by(value)
        result.setdefault(key, [])
        result[key].append(value)

    return result.items()


def list_accumulator[T, **P](fun: Callable[P, Iterable[T]]) -> Callable[P, Sequence[T]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Sequence[T]:
        return list(fun(*args, **kwargs))

    return wrapper


def dict_accumulator[K: Hashable, V, **P](fun: Callable[P, Iterable[tuple[K, V]]]) -> Callable[P, Mapping[K, V]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Mapping[K, V]:
        return dict(fun(*args, **kwargs))

    return wrapper


def set_accumulator[T, **P](fun: Callable[P, Iterable[T]]) -> Callable[P, Collection[T]]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Collection[T]:
        return set(fun(*args, **kwargs))

    return wrapper


def string_accumulator[**P](joiner: str = '') -> Callable[[Callable[P, Iterable[str]]], Callable[P, str]]:
    def decorator(fun: Callable[P, Iterable[str]]) -> Callable[P, str]:
        @functools.wraps(fun)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return joiner.join(fun(*args, **kwargs))

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


def repeat[**P, R](n: int, fun: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> Iterable[R]:
    for _ in range(n):
        yield fun(*args, **kwargs)
