from ..support.parsing.tokens import TokenEnum
from ..support.parsing.identifiers import LatinIdentifier, GreekIdentifier


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


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    comma = ','
    dot = '.'
    space = ' '

    equality = '='
    negation = '¬'


FOLToken = LatinIdentifier | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | MiscToken
