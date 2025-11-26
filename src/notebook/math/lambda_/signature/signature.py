from collections.abc import Iterator

from ....support.collections import MissingKeyError, TrieMapping
from .exceptions import LambdaSignatureError
from .symbols import SignatureSymbol


class LambdaSignature:
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
            raise LambdaSignatureError(f'The signature already contains a {existing.get_kind_string()} symbol {symbol.name}')

    def __getitem__(self, name: str) -> SignatureSymbol:
        return self.trie[name]

    def __contains__(self, symbol: SignatureSymbol) -> bool:
        try:
            existing = self.trie[symbol.name]
        except MissingKeyError:
            return False

        return existing == symbol

    def __iter__(self) -> Iterator[SignatureSymbol]:
        return iter(self.trie.values())


EMPTY_SIGNATURE = LambdaSignature()
