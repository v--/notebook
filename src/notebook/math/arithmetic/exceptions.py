from ..exceptions import NotebookMathError


class NotebookArithmeticError(NotebookMathError):
    pass


class InvalidArgumentError(NotebookArithmeticError, ValueError):
    pass


class NotebookZeroDivisionError(InvalidArgumentError, ZeroDivisionError):
    def __init__(self, divisor: int) -> None:
        super().__init__(f'Expected a nonzero divisor, but got {divisor}')


class NotPositiveIntegerError(InvalidArgumentError):
    def __init__(self, n: int) -> None:
        super().__init__(f'Expected a positive integer, but got {n}')


class RadixError(NotebookArithmeticError):
    pass
