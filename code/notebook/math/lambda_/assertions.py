from typing import NamedTuple

from .alphabet import TypeAssertionConnective
from .terms import Term, TermSchema
from .types import SimpleType, SimpleTypeSchema


class TypeAssertion(NamedTuple):
    term: Term
    type: SimpleType

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'


class TypeAssertionSchema(NamedTuple):
    term: TermSchema
    type: SimpleTypeSchema

    def __str__(self) -> str:
        return f'{self.term}{TypeAssertionConnective.colon} {self.type}'
