from dataclasses import dataclass

import pytest

from ..identifiers import Capitalization, GreekIdentifier, LatinIdentifier
from ..parser import ParsingError
from ..tokenizer import Tokenizer
from ..tokens import TokenEnum
from .identifiers import IdentifierTokenizerMixin


class MiscToken(TokenEnum):
    colon = ':'
    space = ' '


TestToken = LatinIdentifier | GreekIdentifier | MiscToken


@dataclass
class TestTokenizer(IdentifierTokenizerMixin[TestToken], Tokenizer[TestToken]):
    capitalization: Capitalization
    short: bool

    def parse_step(self, head: str) -> TestToken:
        sym = MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if self.is_at_alphabetic_string(LatinIdentifier, self.capitalization):
            return self.parse_identifier(LatinIdentifier, self.capitalization, short=self.short)

        if self.is_at_alphabetic_string(GreekIdentifier, self.capitalization):
            return self.parse_identifier(GreekIdentifier, self.capitalization, short=self.short)

        raise self.error('Unexpected symbol')


def tokenize(string: str, capitalization: Capitalization = Capitalization.mixed, *, short: bool = False) -> list[TestToken]:
    with TestTokenizer(string, capitalization, short) as tokenizer:
        return list(tokenizer.parse())


def test_valid_latin_identifiers() -> None:
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


def test_invalid_latin_identifiers() -> None:
    # Fails to parse Cyrillic
    with pytest.raises(ParsingError):
        tokenize('Тест')

    # Fails to parse capitalized identifiers when uncapitalized ones are expected
    with pytest.raises(ParsingError):
        tokenize('TEST', Capitalization.small)


def test_type_assignments() -> None:
    assert tokenize('x: τ') == [
        LatinIdentifier('x'),
        MiscToken.colon,
        MiscToken.space,
        GreekIdentifier('τ')
    ]
