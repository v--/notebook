from collections.abc import Iterator

from ....support.collections import MissingKeyError, TrieMapping
from .exceptions import FormalLogicSignatureError
from .symbols import FunctionSymbol, PredicateSymbol, SignatureSymbol


class FormalLogicSignature:
    '''What we call here function and predicate symbols can have multiple Unicode graphemes,
    yet they are guaranteed to correspond to one lexeme ("token").
    This makes it more convenient to use at the cost of possibly confusing terminology.
    Calling them "symbols" corresponds to their usage in the literature, where Unicode is not involved.'''
    trie: TrieMapping[SignatureSymbol]

    def __init__(self, *symbols: SignatureSymbol) -> None:
        self.trie = TrieMapping()

        for symbol in symbols:
            self.add_symbol(symbol)

    def add_symbol(self, symbol: SignatureSymbol) -> None:
        try:
            existing = self.trie[symbol.name]
        except MissingKeyError:
            self.trie[symbol.name] = symbol
        else:
            raise FormalLogicSignatureError(f'The signature already contains a {existing.get_kind_string()} symbol {symbol.name}')

    def __getitem__(self, name: str) -> SignatureSymbol:
        return self.trie[name]

    def get_function_symbol(self, name: str) -> FunctionSymbol:
        sym = self[name]

        if not isinstance(sym, FunctionSymbol):
            raise FormalLogicSignatureError(f'Expected {name} to be a function symbol, but got a {sym.get_kind_string()}')

        return sym

    def get_predicate_symbol(self, name: str) -> PredicateSymbol:
        sym = self[name]

        if not isinstance(sym, PredicateSymbol):
            raise FormalLogicSignatureError(f'Expected {name} to be a predicate symbol, but got a {sym.get_kind_string()}')

        return sym

    def __contains__(self, symbol: SignatureSymbol) -> bool:
        try:
            existing = self.trie[symbol.name]
        except MissingKeyError:
            return False

        return existing == symbol

    def __iter__(self) -> Iterator[SignatureSymbol]:
        return iter(self.trie.values())


EMPTY_SIGNATURE = FormalLogicSignature()
