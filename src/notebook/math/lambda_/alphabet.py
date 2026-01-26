from enum import StrEnum


class BinderSymbol(StrEnum):
    LAMBDA = 'λ'


class AuxImproperSymbol(StrEnum):
    DOT = '.'
    COLON = ':'
    LEFT_PARENTHESIS = '('
    RIGHT_PARENTHESIS = ')'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    PLACEHOLDER = '•'


class BinaryTypeConnective(StrEnum):
    ARROW = '→'
    SUM = '+'
    PRODUCT = '×'
