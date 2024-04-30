from .signature import FOLSignature


propositional_signature = FOLSignature()


for l in 'abcdefghijklmnopqrstuvwxyz':
    propositional_signature.add_predicate_symbol(l, arity=0)
    propositional_signature.add_predicate_symbol(l.upper(), arity=0)
