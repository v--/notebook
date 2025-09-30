from enum import StrEnum


class ImproperTermSymbol(StrEnum):
    LAMBDA = 'λ'


class BinaryTypeConnective(StrEnum):
    ARROW = '→'
    SUM = '+'
    PROD = '×'
