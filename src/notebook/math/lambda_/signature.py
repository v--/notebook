from collections.abc import Collection, Iterable
from typing import Literal, NamedTuple

from ...parsing import is_greek_identifier, is_latin_identifier
from ...support.collections import TrieMapping
from ...support.inference import ImproperInferenceRuleSymbol
from ...support.unicode import Capitalization
from .alphabet import AuxImproperSymbol, BinaryTypeConnective, BinderSymbol
from .exceptions import LambdaSignatureError


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
                if name in BinaryTypeConnective or name in AuxImproperSymbol or name in ImproperInferenceRuleSymbol:
                    raise LambdaSignatureError(f'Cannot use the improper symbol {name!r} as a base type')

                if is_greek_identifier(name, Capitalization.LOWER):
                    raise LambdaSignatureError(f'Cannot use {name!r} as a base type because that conflicts with the grammar of type variables')

                self.trie[name] = LambdaSymbol('BASE_TYPE', name)

        if constant_terms:
            for name in constant_terms:
                if name in BinderSymbol or name in AuxImproperSymbol or name in ImproperInferenceRuleSymbol:
                    raise LambdaSignatureError(f'Cannot use the improper symbol {name!r} as a λ-term constant')

                if is_latin_identifier(name, Capitalization.LOWER):
                    raise LambdaSignatureError(f'Cannot use {name!r} as a λ-term constant because that conflicts with the grammar of variables')

                if is_latin_identifier(name, Capitalization.UPPER):
                    raise LambdaSignatureError(f'Cannot use {name!r} as a λ-term constant because that conflicts with the grammar of placeholders')

                self.trie[name] = LambdaSymbol('CONSTANT_TERM', name)

    def add_symbol(self, symbol_kind: LambdaSymbolKind, name: str) -> None:
        self.trie[name] = LambdaSymbol(symbol_kind, name)

    def get_symbol(self, name: str) -> LambdaSymbol:
        return self.trie[name]

    def iter_symbols(self) -> Iterable[LambdaSymbol]:
        return self.trie.values()


EMPTY_SIGNATURE = LambdaSignature()
