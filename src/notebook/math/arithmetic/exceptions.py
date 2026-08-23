from notebook.math.exceptions import NotebookMathError


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


class NotCoprimeError(InvalidArgumentError):
    def __init__(self, a: int, b: int) -> None:
        super().__init__(f'Expected {a} and {b} to be coprime')


class RadixError(NotebookArithmeticError):
    pass
