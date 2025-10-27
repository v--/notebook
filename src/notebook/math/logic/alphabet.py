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
