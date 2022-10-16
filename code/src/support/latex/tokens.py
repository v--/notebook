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


class Word(LaTeXToken):
    pass


class EscapedWord(LaTeXToken):
    def __str__(self):
        return '\\' + self.value


class Special(LaTeXToken):
    pass


ampersand = Special('&')
underscore = Special('_')
caret = Special('^')
opening_brace = Special('{')
closing_brace = Special('}')
opening_bracket = Special('[')
closing_bracket = Special(']')

special_symbol_map = {
    '&':  ampersand,
    '_': underscore,
    '^': caret,
    '{': opening_brace,
    '}': closing_brace,
    '[': opening_bracket,
    ']': closing_bracket
}


@dataclass
class Whitespace(LaTeXToken):
    value: str


single_space = Whitespace(' ')
tab = Whitespace(' ')
newline = Whitespace('\n')

single_whitespace_map = {
    ' ':  single_space,
    '\t': tab,
    '\n': newline
}
