from dataclasses import dataclass


@dataclass
class LaTeXToken:
    value: str

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object):
        return isinstance(other, type(self)) and self.value == other.value


class WordToken(LaTeXToken):
    pass


class EscapedWordToken(LaTeXToken):
    def __str__(self):
        return '\\' + self.value


class SpecialToken(LaTeXToken):
    pass


ampersand_token = SpecialToken('&')
underscore_token = SpecialToken('_')
caret_token = SpecialToken('^')
opening_brace = SpecialToken('{')
closing_brace = SpecialToken('}')
opening_bracket = SpecialToken('[')
closing_bracket = SpecialToken(']')

special_symbol_map = {
    '&': ampersand_token,
    '_': underscore_token,
    '^': caret_token,
    '{': opening_brace,
    '}': closing_brace,
    '[': opening_bracket,
    ']': closing_bracket
}


@dataclass
class WhitespaceToken(LaTeXToken):
    pass
