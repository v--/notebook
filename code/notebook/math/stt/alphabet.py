from ...parsing.tokens import TokenEnum


class LambdaTermConnective(TokenEnum):
    l = 'λ'


class SimpleTypeConnective(TokenEnum):
    arrow = '→'


class TypeAssertionConnective(TokenEnum):
    colon = ':'


class RuleConnective(TokenEnum):
    sequent = '⫢'
