from collections.abc import Iterable
from typing import Literal, NamedTuple

from ...parsing import is_greek_identifier, is_latin_identifier
from ...support.collections import TrieMapping
from ...support.inference import ImproperInferenceRuleSymbol
from ...support.substitution import ImproperSubstitutionSymbol
from ...support.unicode import Capitalization
from .alphabet import AuxImproperSymbol, BinaryConnective, EqualitySymbol, PropConstant, Quantifier, UnaryPrefix
from .exceptions import FormalLogicSignatureError


SignatureSymbolKind = Literal['FUNCTION', 'PREDICATE']


class SignatureSymbol(NamedTuple):
    kind: SignatureSymbolKind
    name: str
    arity: int
    infix: bool

    def get_readable_kind(self) -> str:
        return self.kind.lower()


class FormalLogicSignature:
    '''What we call here function and predicate symbols can have multiple Unicode graphemes,
    yet they are guaranteed to correspond to one lexeme ("token").
    This makes it more convenient to use at the cost of possibly confusing terminology.
    Calling them "symbols" corresponds to their usage in the literature, where Unicode is not involved.'''
    trie: TrieMapping[SignatureSymbol]

    def __init__(self) -> None:
        self.trie = TrieMapping()

    def add_symbol(self, symbol_kind: SignatureSymbolKind, name: str, arity: int, *, infix: bool) -> None:
        if name == '(' or name == ')':
            raise FormalLogicSignatureError('Cannot use a parenthesis as a proper signature symbol')

        if (
            name in PropConstant or
            name in UnaryPrefix or
            name in BinaryConnective or
            name in Quantifier or
            name in EqualitySymbol or
            name in AuxImproperSymbol or
            name in ImproperInferenceRuleSymbol or
            name in ImproperSubstitutionSymbol
        ):
            raise FormalLogicSignatureError(f'Cannot use the improper symbol {name!r} as a proper signature symbol')

        if is_latin_identifier(name, Capitalization.LOWER):
            raise FormalLogicSignatureError(f'Cannot use {name!r} as a proper signature symbol because that conflicts with the grammar of variables')

        if is_greek_identifier(name, Capitalization.LOWER):
            raise FormalLogicSignatureError(f'Cannot use {name!r} as a proper signature symbol because that conflicts with the grammar of placeholders')

        if infix and arity != 2:
            raise FormalLogicSignatureError(f'Cannot use {name!r} as an infix symbol since it has arity {arity}')

        self.trie[name] = SignatureSymbol(symbol_kind, name, arity, infix)

    def get_symbol(self, name: str) -> SignatureSymbol:
        return self.trie[name]

    def iter_symbols(self) -> Iterable[SignatureSymbol]:
        return self.trie.values()


EMPTY_SIGNATURE = FormalLogicSignature()
