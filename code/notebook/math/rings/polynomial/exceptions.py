from ..exceptions import RingDivisionError, RingError


class PolynomialError(RingError):
    pass


class PolynomialDivisionError(RingDivisionError):
    pass


class PolynomialEvaluationError(PolynomialError):
    pass
