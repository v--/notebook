from collections.abc import Callable, Iterable, Mapping
from typing import Any

import pytest

from notebook.support.iteration import repeat


def pytest_parametrize_lists[**P](**kwargs: Iterable[Any]) -> Callable[[Callable[P, None]], Callable[[], None]]:
    return pytest.mark.parametrize(
        tuple(kwargs.keys()),
        zip(*kwargs.values(), strict=True)
    )


def pytest_parametrize_kwargs[**P](*args: Mapping[str, Any]) -> Callable[[Callable[P, None]], Callable[[], None]]:
    return pytest.mark.parametrize(
        tuple(args[0].keys()),
        [tuple(kwargs.values()) for kwargs in args]
    )


def repeat5[**P, R](fun: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> Iterable[R]:
    return repeat(5, fun, *args, **kwargs)
