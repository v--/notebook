from .signature import FOLSignature


propositional_signature = FOLSignature()


# We shadow all FOL variables with the corresponding predicates
for ind in range(ord('a'), ord('z') + 1):
    propositional_signature.add_predicate_symbol(chr(ind), arity=0)
