from ...parsing.old_tokens import TokenEnum


class TermConnective(TokenEnum):
    l = 'λ'


class BinaryTypeConnective(TokenEnum):
    arrow = '→'
    plus = '+'
    times = '×'


class TypeAssertionConnective(TokenEnum):
    colon = ':'
