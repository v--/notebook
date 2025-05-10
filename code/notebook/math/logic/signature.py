from collections.abc import Iterable
from typing import Literal, NamedTuple

from ...support.collections import TrieMapping


SignatureSymbolKind = Literal['FUNCTION', 'PREDICATE']


class SignatureSymbol(NamedTuple):
    kind: SignatureSymbolKind
    name: str
    arity: int


class FormalLogicSignature:
    '''What we call here function and predicate symbols can have multiple Unicode graphemes,
    yet they are guaranteed to correspond to one lexeme ("token").
    This makes it more convenient to use at the cost of possibly confusing terminology.
    Calling them "symbols" corresponds to their usage in the literature, where Unicode is not involved.'''
    trie: TrieMapping[SignatureSymbol]

    def __init__(self) -> None:
        self.trie = TrieMapping()

    def add_symbol(self, symbol_kind: SignatureSymbolKind, name: str, arity: int) -> None:
        self.trie[name] = SignatureSymbol(symbol_kind, name, arity)

    def get_symbol(self, name: str) -> SignatureSymbol:
        return self.trie[name]

    def iter_symbols(self) -> Iterable[SignatureSymbol]:
        return self.trie.values()


EMPTY_SIGNATURE = FormalLogicSignature()
