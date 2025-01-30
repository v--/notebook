from .signature import FormalLogicSignature


# We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
# This deviates from the monograph, but implementing support for propositional variables will be of no use for us.
PROPOSITIONAL_SIGNATURE = FormalLogicSignature()


# We shadow all variables with the corresponding predicates
for ind in range(ord('a'), ord('z') + 1):
    PROPOSITIONAL_SIGNATURE.add_predicate_symbol(chr(ind), arity=0)
