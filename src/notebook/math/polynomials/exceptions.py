from ..exceptions import NotebookMathError


class PolynomialError(NotebookMathError):
    pass


class IndeterminateError(PolynomialError):
    pass


class PolynomialDegreeError(PolynomialError):
    pass


class PolynomialDivisionError(PolynomialError):
    pass


class ZeroPolynomialError(PolynomialDivisionError, ZeroDivisionError):
    pass


class PolynomialEvaluationError(PolynomialError):
    pass
