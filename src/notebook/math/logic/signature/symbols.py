import abc
from dataclasses import dataclass
from typing import Literal, override

from ....parsing import is_greek_identifier, is_latin_identifier
from ....support.inference import ImproperInferenceRuleSymbol
from ....support.substitution import ImproperSubstitutionSymbol
from ....support.unicode import Capitalization
from ..alphabet import AuxImproperSymbol, BinaryConnective, EqualitySymbol, PropConstantSymbol, Quantifier, UnaryPrefix
from .exceptions import FormalLogicSignatureError


SignatureSymbolNotation = Literal['PREFIX', 'INFIX', 'CONDENSED']


@dataclass(unsafe_hash=True)
class BaseSignatureSymbol(abc.ABC):
    name: str
    arity: int
    notation: SignatureSymbolNotation = 'PREFIX'

    def __init__(self, name: str, arity: int, notation: SignatureSymbolNotation | None = None) -> None:
        if notation is None:
            notation = 'CONDENSED' if arity == 0 else 'PREFIX'

        self.validate(name, arity, notation)
        self.name = name
        self.arity = arity
        self.notation = notation

    def validate(self, name: str, arity: int, notation: SignatureSymbolNotation) -> None:
        self.name = name
        self.arity = arity

        if name == '(' or name == ')':
            raise FormalLogicSignatureError('Cannot use a parenthesis as a proper signature symbol')

        if (
            name in PropConstantSymbol or
            name in UnaryPrefix or
            name in BinaryConnective or
            name in Quantifier or
            name in EqualitySymbol or
            name in AuxImproperSymbol or
            name in ImproperInferenceRuleSymbol or
            name in ImproperSubstitutionSymbol
        ):
            raise FormalLogicSignatureError(f'Cannot use the improper symbol {name} as a proper signature symbol')

        if is_latin_identifier(name, Capitalization.LOWER):
            raise FormalLogicSignatureError(f'Cannot use {name} as a proper signature symbol because that conflicts with the grammar of variables')

        if is_greek_identifier(name, Capitalization.LOWER):
            raise FormalLogicSignatureError(f'Cannot use {name} as a proper signature symbol because that conflicts with the grammar of placeholders')

        if notation == 'INFIX' and arity != 2:
            raise FormalLogicSignatureError(f'Cannot use infix notation for the {self.get_kind_string()} {name} with arity {arity}')

        if arity == 0 and notation != 'CONDENSED':
            raise FormalLogicSignatureError(f'Only condensed prefix notation is allowed for the nullary {self.get_kind_string()} {name}')

    @abc.abstractmethod
    def get_kind_string(self) -> str:
        ...

    def __str__(self) -> str:
        return self.name


class FunctionSymbol(BaseSignatureSymbol):
    @override
    def get_kind_string(self) -> str:
        return 'function'


class PredicateSymbol(BaseSignatureSymbol):
    @override
    def get_kind_string(self) -> str:
        return 'predicate'


SignatureSymbol = FunctionSymbol | PredicateSymbol
