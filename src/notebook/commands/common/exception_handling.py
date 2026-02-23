import functools
from collections.abc import Callable


def exit_gracefully_on_exception[R, **P](*exceptions: type[BaseException]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    # The outer ParamSpec seems not to be sufficient for ty because it is only used in the return value.
    def decorator[S, **Q](fun: Callable[Q, S]) -> Callable[Q, S]:
        @functools.wraps(fun)
        def wrapper(*args: Q.args, **kwargs: Q.kwargs) -> S:
            try:
                return fun(*args, **kwargs)
            except exceptions as err:
                raise SystemExit(str(err)) from err

        return wrapper

    return decorator
