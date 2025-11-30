from ..exceptions import NotebookMathError


class PolynomialError(NotebookMathError):
    pass


class PolynomialDivisionError(NotebookMathError):
    pass


class ZeroPolynomialError(PolynomialDivisionError, ZeroDivisionError):
    pass


class PolynomialEvaluationError(PolynomialError):
    pass
