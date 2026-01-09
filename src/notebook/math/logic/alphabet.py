from enum import StrEnum
from typing import Literal


class PropConstantSymbol(StrEnum):
    VERUM = '⊤'
    FALSUM = '⊥'


class UnaryPrefix(StrEnum):
    NEGATION = '¬'


class BinaryConnective(StrEnum):
    DISJUNCTION = '∨'
    CONJUNCTION = '∧'
    CONDITIONAL = '→'
    BICONDITIONAL = '↔'


LatticeConnective = Literal[BinaryConnective.DISJUNCTION, BinaryConnective.CONJUNCTION]


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
    SEQUENT = '⊢'



def get_dual_prop_constant(const: PropConstantSymbol) -> PropConstantSymbol:
    match const:
        case PropConstantSymbol.VERUM:
            return PropConstantSymbol.FALSUM

        case PropConstantSymbol.FALSUM:
            return PropConstantSymbol.VERUM


def get_dual_connective(conn: LatticeConnective) -> LatticeConnective:
    match conn:
        case BinaryConnective.CONJUNCTION:
            return BinaryConnective.DISJUNCTION

        case BinaryConnective.DISJUNCTION:
            return BinaryConnective.CONJUNCTION


def get_dual_quantifier(quant: Quantifier) -> Quantifier:
    match quant:
        case Quantifier.UNIVERSAL:
            return Quantifier.EXISTENTIAL

        case Quantifier.EXISTENTIAL:
            return Quantifier.UNIVERSAL
