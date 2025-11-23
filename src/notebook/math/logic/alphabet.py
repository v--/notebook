from enum import StrEnum


class PropConstant(StrEnum):
    VERUM = '⊤'
    FALSUM = '⊥'


class UnaryPrefix(StrEnum):
    NEGATION = '¬'


class BinaryConnective(StrEnum):
    DISJUNCTION = '∨'
    CONJUNCTION = '∧'
    CONDITIONAL = '→'
    BICONDITIONAL = '↔'


class Quantifier(StrEnum):
    UNIVERSAL = '∀'
    EXISTENTIAL = '∃'


class EqualitySymbol(StrEnum):
    EQUALITY = '='


class AuxImproperSymbol(StrEnum):
    DOT = '.'
    COMMA = ','
    ASTERISK = '*'
    LEFT_PARENTHESIS = '('
    RIGHT_PARENTHESIS = ')'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
