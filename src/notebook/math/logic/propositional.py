from collections.abc import Iterable
from typing import override

from .formulas import PredicateApplication
from .signature import FormalLogicSignature, FormalLogicSignatureError, PredicateSymbol, SignatureSymbol


class PropositionalLogicSignature(FormalLogicSignature):
    """A hackish class designed to treat individual variables without indices as nullary propositions."""
    def __init__(self, variable_names: Iterable[str]) -> None:
        super().__init__()

        for name in variable_names:
            self.trie[name] = PredicateSymbol(name=name, arity=0, infix=False)

    @override
    def add_symbol(self, symbol: SignatureSymbol) -> None:
        raise FormalLogicSignatureError('Adding proper symbols to a propositional signature is disallowed')


# We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
# This deviates from the monograph, but implementing support for propositional variables will be of no use for us.
PROPOSITIONAL_SIGNATURE = PropositionalLogicSignature(chr(ind) for ind in range(ord('a'), ord('z') + 1))
DEFAULT_PROPOSITIONAL_VARIABLE = PROPOSITIONAL_SIGNATURE['p']


def get_propositional_variable(source: str, signature: PropositionalLogicSignature = PROPOSITIONAL_SIGNATURE) -> PredicateApplication:
    return PredicateApplication(signature[source], [])
