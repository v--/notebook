from dataclasses import dataclass

import pytest

from ...support.unicode import Capitalization, is_greek_string, is_latin_string
from ..identifiers import GreekIdentifier, LatinIdentifier
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
    def parse_step(self, head: str) -> TestToken:
        sym = MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if is_latin_string(head, Capitalization.small):
            return self.parse_latin_identifier()

        if is_greek_string(head, Capitalization.small):
            return self.parse_greek_identifier()

        raise self.error('Unexpected symbol')


def tokenize(string: str) -> list[TestToken]:
    with TestTokenizer(string) as tokenizer:
        return list(tokenizer.parse())


def test_valid_latin_identifiers() -> None:
    assert tokenize('t') == [LatinIdentifier('t')]
    assert tokenize('t₀e₁s₂t₃') == [
        LatinIdentifier('t', index=0),
        LatinIdentifier('e', index=1),
        LatinIdentifier('s', index=2),
        LatinIdentifier('t', index=3)
    ]


def test_invalid_latin_identifiers() -> None:
    # Fails to parse Cyrillic
    with pytest.raises(ParsingError):
        tokenize('Т')

    # Fails to parse capitalized identifiers
    with pytest.raises(ParsingError):
        tokenize('T')


def test_type_assignments() -> None:
    assert tokenize('x: τ') == [
        LatinIdentifier('x'),
        MiscToken.colon,
        MiscToken.space,
        GreekIdentifier('τ')
    ]
