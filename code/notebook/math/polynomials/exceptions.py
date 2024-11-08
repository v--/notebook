from ...exceptions import NotebookCodeError


class PolynomialError(NotebookCodeError):
    pass


class PolynomialDivisionError(NotebookCodeError):
    pass


class PolynomialZeroDivisionError(PolynomialDivisionError, ZeroDivisionError):
    pass


class PolynomialEvaluationError(PolynomialError):
    pass
