from typing import NamedTuple

from .alphabet import TypeAssertionConnective
from .terms import LambdaTerm, LambdaTermSchema
from .types import SimpleType, SimpleTypeSchema


class TypeAssertion(NamedTuple):
    term: LambdaTerm
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'


class TypeAssertionSchema(NamedTuple):
    term: LambdaTermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'
