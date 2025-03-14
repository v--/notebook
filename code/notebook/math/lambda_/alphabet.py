from enum import StrEnum


class TermConnective(StrEnum):
    LAMBDA = 'λ'


class BinaryTypeConnective(StrEnum):
    ARROW = '→'
    SUM = '+'
    PROD = '×'
