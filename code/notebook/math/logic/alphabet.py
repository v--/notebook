from ...parsing.old_tokens import TokenEnum


class PropConstant(TokenEnum):
    verum = '⊤'
    falsum = '⊥'


class UnaryConnective(TokenEnum):
    negation = '¬'


class BinaryConnective(TokenEnum):
    disjunction = '∨'
    conjunction = '∧'
    conditional = '→'
    biconditional = '↔'


class Quantifier(TokenEnum):
    universal = '∀'
    existential = '∃'


class SchemaConnective(TokenEnum):
    substitution = '↦'
