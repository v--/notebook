from typing import override

from .exceptions import FormalLogicSignatureError
from .signature import FormalLogicSignature, SignatureSymbol, SignatureSymbolKind


class PropositionalLogicSignature(FormalLogicSignature):
    """A hackish class designed to treat all individual variables as nullary propositions."""
    def __init__(self) -> None:
        super().__init__()

        for ind in range(ord('a'), ord('z') + 1):
            self.trie[chr(ind)] = SignatureSymbol('PREDICATE', name=chr(ind), arity=0)

    @override
    def add_symbol(self, symbol_kind: SignatureSymbolKind, name: str, arity: int) -> None:
        raise FormalLogicSignatureError('Adding proper symbols to a propositional signature is disallowed')


# We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
# This deviates from the monograph, but implementing support for propositional variables will be of no use for us.
PROPOSITIONAL_SIGNATURE = PropositionalLogicSignature()
