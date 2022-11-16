from ..support.parsing import TokenMixin, TokenEnum


class NaturalNumber(TokenMixin):
    pass


class LatinName(TokenMixin):
    pass


class GreekName(TokenMixin):
    pass


class PropConstant(TokenEnum):
    verum = '⊤'
    falsum = '⊥'


class BinaryConnective(TokenEnum):
    join_ = '∨'
    meet = '∧'
    conditional = '→'
    biconditional = '↔'


class Quantifier(TokenEnum):
    universal = '∀'
    existential = '∃'


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    comma = ','
    dot = '.'
    space = ' '

    equality = '='
    negation = '¬'


FOLToken = NaturalNumber | LatinName | GreekName | PropConstant | BinaryConnective | Quantifier | MiscToken
