from collections.abc import Iterable
from typing import override

from .exceptions import FormalLogicSignatureError
from .signature import FormalLogicSignature, SignatureSymbol, SignatureSymbolKind


class PropositionalLogicSignature(FormalLogicSignature):
    """A hackish class designed to treat individual variables without indices as nullary propositions."""
    def __init__(self, variable_names: Iterable[str]) -> None:
        super().__init__()

        for name in variable_names:
            self.trie[name] = SignatureSymbol('PREDICATE', name=name, arity=0)

    @override
    def add_symbol(self, symbol_kind: SignatureSymbolKind, name: str, arity: int) -> None:
        raise FormalLogicSignatureError('Adding proper symbols to a propositional signature is disallowed')


# We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
# This deviates from the monograph, but implementing support for propositional variables will be of no use for us.
PROPOSITIONAL_SIGNATURE = PropositionalLogicSignature(chr(ind) for ind in range(ord('a'), ord('z') + 1))
