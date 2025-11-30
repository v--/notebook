import functools

from ..exceptions import PolynomialDegreeError


@functools.total_ordering
class PolynomialDegree:
    value: int | None

    @property
    def is_undefined(self) -> bool:
        return self.value is None

    def __init__(self, value: int | None = None) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        match other:
            case int():
                return self.value == other

            case PolynomialDegree():
                return self.value == other.value

            case _:
                return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __add__(self, other: PolynomialDegree | int) -> PolynomialDegree:
        other_value = other.value if isinstance(other, PolynomialDegree) else other

        if self.value is None or other_value is None:
            return UNDEFINED_POLYNOMIAL_DEGREE

        return PolynomialDegree(self.value + other_value)

    def __sub__(self, other: PolynomialDegree | int) -> PolynomialDegree:
        other_value = other.value if isinstance(other, PolynomialDegree) else other

        if self.value is None or other_value is None:
            return UNDEFINED_POLYNOMIAL_DEGREE

        return PolynomialDegree(self.value - other_value)

    def __mul__(self, other: PolynomialDegree | int) -> PolynomialDegree:
        other_value = other.value if isinstance(other, PolynomialDegree) else other

        if self.value is None or other_value is None:
            return UNDEFINED_POLYNOMIAL_DEGREE

        return PolynomialDegree(self.value * other_value)

    def __floordiv__(self, other: PolynomialDegree | int) -> PolynomialDegree:
        other_value = other.value if isinstance(other, PolynomialDegree) else other

        if self.value is None or other_value is None:
            return UNDEFINED_POLYNOMIAL_DEGREE

        return PolynomialDegree(self.value // other_value)

    def __pow__(self, power: int) -> PolynomialDegree:
        if self.value is None:
            return UNDEFINED_POLYNOMIAL_DEGREE

        return PolynomialDegree(self.value ** power)

    def __le__(self, other: PolynomialDegree | int) -> bool:
        other_value = other.value if isinstance(other, PolynomialDegree) else other

        if self.value is None and other_value is None:
            return True

        if self.value is None:
            return True

        if other_value is None:
            return False

        return self.value <= other_value


    def __int__(self) -> int:
        if self.value is None:
            raise PolynomialDegreeError('Undefined degree')

        return self.value

    def __str__(self) -> str:
        if self.value is None:
            return 'UNDEFINED'

        return str(self.value)


UNDEFINED_POLYNOMIAL_DEGREE = PolynomialDegree()
