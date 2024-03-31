from ...parsing.tokens import TokenEnum


class PropConstant(TokenEnum):
    verum = '⊤'
    falsum = '⊥'



class BinaryConnective(TokenEnum):
    disjunction = '∨'
    conjunction = '∧'
    conditional = '→'
    biconditional = '↔'


class Quantifier(TokenEnum):
    universal = '∀'
    existential = '∃'
