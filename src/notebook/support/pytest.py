from typing import TYPE_CHECKING, Any

import pytest

from .coderefs import DictMetadataProxy
from .iteration import repeat


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Mapping


def pytest_parametrize_lists[**P](**kwargs: Iterable[Any]) -> Callable[[Callable[P, None]], Callable[[], None]]:
    return pytest.mark.parametrize(
        tuple(kwargs.keys()),
        zip(*kwargs.values(), strict=True),
    )


def pytest_parametrize_kwargs[**P](*args: Mapping[str, Any]) -> Callable[[Callable[P, None]], Callable[[], None]]:
    pytest_decorator = pytest.mark.parametrize(
        tuple(args[0].keys()),
        [tuple(kwargs.values()) for kwargs in args],
    )

    def decorator(fun: Callable[P, None]) -> Callable[[], None]:
        for arg in args:
            if isinstance(arg, DictMetadataProxy):
                arg.collector.mapping[arg.doc_ref] = fun

        return pytest_decorator(fun)

    return decorator


def repeat5[**P, R](fun: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> Iterable[R]:
    return repeat(5, fun, *args, **kwargs)
