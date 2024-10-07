import functools
import operator
from dataclasses import dataclass


@dataclass
class ZhegalkinPolynomial:
    payload: frozenset[frozenset[str]]
    free: bool

    def __call__(self, **kwargs: bool) -> bool:
        result = self.free

        for monomial in self.payload:
            result ^= functools.reduce(operator.and_, (kwargs[var] for var in monomial))

        return result

    def __str__(self) -> str:
        if len(self.payload) == 0:
            return 'T' if self.free else 'F'

        return ' + '.join(''.join(variables) for variables in self.payload) + (' + T' if self.free else '')

    def __add__(self, other: 'ZhegalkinPolynomial') -> 'ZhegalkinPolynomial':
        return ZhegalkinPolynomial(
            payload=frozenset(self.payload.symmetric_difference(other.payload)),
            free=self.free ^ other.free
        )

    def __mul__(self, other: 'ZhegalkinPolynomial') -> 'ZhegalkinPolynomial':
        if len(self.payload) == 0:
            return other if self.free else ZhegalkinPolynomial(frozenset(), free=False)

        if len(other.payload) == 0:
            return self if other.free else ZhegalkinPolynomial(frozenset(), free=False)

        payload = set[frozenset[str]]()

        for a_monomial in self.payload:
            for b_monomial in other.payload:
                monomial = a_monomial.symmetric_difference(b_monomial)

                if len(monomial) > 0:
                    payload.add(monomial)

                if self.free:
                    payload.add(b_monomial)

            if other.free:
                payload.add(a_monomial)

        return ZhegalkinPolynomial(payload=frozenset(payload), free=self.free and other.free)
