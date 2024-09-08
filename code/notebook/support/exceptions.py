import functools
from collections.abc import Callable

from notebook.exceptions import NotebookCodeException


def exit_gracefully_on_error[R, **P](fun: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fun(*args, **kwargs)
        except NotebookCodeException as err:
            raise SystemExit(str(err)) from err

    return wrapper
