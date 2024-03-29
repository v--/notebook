from dataclasses import dataclass

import pytest

from .parser import ParserError
from .tokens import TokenEnum
from .tokenizer import BaseTokenizer
from .identifiers import Capitalization, LatinIdentifier, GreekIdentifier


class MiscToken(TokenEnum):
    colon = ':'
    space = ' '


TestToken = LatinIdentifier | GreekIdentifier | MiscToken


@dataclass
class TestTokenizer(BaseTokenizer[TestToken]):
    capitalization: Capitalization
    short: bool

    def parse_step(self, head: str) -> TestToken:
        sym = MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if self.accept_alphabetic_string(LatinIdentifier, self.capitalization):
            return self.parse_identifier(LatinIdentifier, self.capitalization, self.short)

        if self.accept_alphabetic_string(GreekIdentifier, self.capitalization):
            return self.parse_identifier(GreekIdentifier, self.capitalization, self.short)

        raise self.error('Unexpected symbol')


def tokenize(string: str, capitalization: Capitalization = Capitalization.mixed, short: bool = False):
    tokenizer = TestTokenizer(string, capitalization, short)
    result = list(tokenizer.parse())
    tokenizer.assert_exhausted()
    return result


def test_valid_latin_identifiers():
    assert tokenize('Test') == [LatinIdentifier('Test')]
    assert tokenize('Test', short=True) == [
        LatinIdentifier('T', short=True),
        LatinIdentifier('e', short=True),
        LatinIdentifier('s', short=True),
        LatinIdentifier('t', short=True)
    ]

    assert tokenize('T₀e₁s₂t₃') == [
        LatinIdentifier('T₀'),
        LatinIdentifier('e₁'),
        LatinIdentifier('s₂'),
        LatinIdentifier('t₃')
    ]


def test_invalid_latin_identifiers():
    # Fails to parse Cyrillic
    with pytest.raises(ParserError):
        tokenize('Тест')

    # Fails to parse capitalized identifiers when uncapitalized ones are expected
    with pytest.raises(ParserError):
        tokenize('TEST', Capitalization.small)


def test_type_assignments():
    assert tokenize('x: τ') == [
        LatinIdentifier('x'),
        MiscToken.colon,
        MiscToken.space,
        GreekIdentifier('τ')
    ]
