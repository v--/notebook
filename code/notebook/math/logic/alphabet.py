from enum import StrEnum


class PropConstant(StrEnum):
    VERUM = '⊤'
    FALSUM = '⊥'


class UnaryConnective(StrEnum):
    NEGATION = '¬'


class BinaryConnective(StrEnum):
    DISJUNCTION = '∨'
    CONJUNCTION = '∧'
    CONDITIONAL = '→'
    BICONDITIONAL = '↔'


class Quantifier(StrEnum):
    UNIVERSAL = '∀'
    EXISTENTIAL = '∃'


class SchemaConnective(StrEnum):
    SUBSTITUTION = '↦'
