from .signature import FOLSignature


# We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
# This deviates from the monograph, but implementing support for propositional variables will be of no use for us.
propositional_signature = FOLSignature()


# We shadow all FOL variables with the corresponding predicates
for ind in range(ord('a'), ord('z') + 1):
    propositional_signature.add_predicate_symbol(chr(ind), arity=0)
