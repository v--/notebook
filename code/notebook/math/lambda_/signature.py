from collections.abc import Collection, Iterable
from typing import Literal, NamedTuple

from ...support.collections import TrieMapping


LambdaSymbolKind = Literal['CONSTANT_TERM', 'BASE_TYPE']


class LambdaSymbol(NamedTuple):
    kind: LambdaSymbolKind
    name: str


class LambdaSignature:
    trie: TrieMapping[LambdaSymbol]

    def __init__(self, base_types: Collection[str] | None = None, constant_terms: Collection[str] | None = None) -> None:
        self.trie = TrieMapping()

        if base_types:
            for name in base_types:
                self.trie[name] = LambdaSymbol('BASE_TYPE', name)

        if constant_terms:
            for name in constant_terms:
                self.trie[name] = LambdaSymbol('CONSTANT_TERM', name)

    def add_symbol(self, symbol_kind: LambdaSymbolKind, name: str) -> None:
        self.trie[name] = LambdaSymbol(symbol_kind, name)

    def get_symbol(self, name: str) -> LambdaSymbol:
        return self.trie[name]

    def iter_symbols(self) -> Iterable[LambdaSymbol]:
        return self.trie.values()


EMPTY_SIGNATURE = LambdaSignature()
