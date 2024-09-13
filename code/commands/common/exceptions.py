import functools
from collections.abc import Callable

from notebook.exceptions import NotebookCodeError


class NotebookCommandError(NotebookCodeError):
    pass


def exit_gracefully_on_exception[R, **P](*exceptions: type[BaseException]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(fun: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fun)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return fun(*args, **kwargs)
            except exceptions as err:
                raise SystemExit(str(err)) from err

        return wrapper

    return decorator
