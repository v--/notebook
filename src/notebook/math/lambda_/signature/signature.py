from collections.abc import Iterator

from ....parsing import is_greek_identifier, is_latin_identifier
from ....support.collections import MissingKeyError, TrieMapping
from ....support.inference import ImproperInferenceRuleSymbol
from ....support.unicode import Capitalization
from ..alphabet import AuxImproperSymbol, BinaryTypeConnective, BinderSymbol
from .exceptions import LambdaSignatureError
from .symbols import BaseTypeSymbol, ConstantTermSymbol, SignatureSymbol


class LambdaSignature:
    trie: TrieMapping[SignatureSymbol]

    def __init__(self, *symbols: SignatureSymbol) -> None:
        self.trie = TrieMapping()

        for symbol in symbols:
            self.add_symbol(symbol)

    def add_symbol(self, symbol: SignatureSymbol) -> None:
        name = symbol.name

        match symbol:
            case BaseTypeSymbol():
                if name in BinaryTypeConnective or name in AuxImproperSymbol or name in ImproperInferenceRuleSymbol:
                    raise LambdaSignatureError(f'Cannot use the improper symbol {name!r} as a base type')

                if is_greek_identifier(name, Capitalization.LOWER):
                    raise LambdaSignatureError(f'Cannot use {name!r} as a base type because that conflicts with the grammar of type variables')

            case ConstantTermSymbol():
                if name in BinderSymbol or name in AuxImproperSymbol or name in ImproperInferenceRuleSymbol:
                    raise LambdaSignatureError(f'Cannot use the improper symbol {name!r} as a λ-term constant')

                if is_latin_identifier(name, Capitalization.LOWER):
                    raise LambdaSignatureError(f'Cannot use {name!r} as a λ-term constant because that conflicts with the grammar of variables')

                if is_latin_identifier(name, Capitalization.UPPER):
                    raise LambdaSignatureError(f'Cannot use {name!r} as a λ-term constant because that conflicts with the grammar of placeholders')

        self.trie[name] = symbol

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
