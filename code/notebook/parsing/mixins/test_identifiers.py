from collections.abc import Sequence

import pytest

from ...support.pytest import pytest_parametrize_kwargs
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


class SimpleTokenizer(IdentifierTokenizerMixin[TestToken], Tokenizer[TestToken]):
    def parse_step(self, head: str) -> TestToken:
        if sym := MiscToken.try_match(head):
            self.advance()
            return sym

        if is_latin_string(head, Capitalization.lower):
            return self.parse_latin_identifier()

        if is_greek_string(head, Capitalization.lower):
            return self.parse_greek_identifier()

        raise self.error('Unexpected symbol')


def tokenize(string: str) -> Sequence[TestToken]:
    with SimpleTokenizer(string) as tokenizer:
        return list(tokenizer.parse())


@pytest_parametrize_kwargs(
    dict(string='t',   expected=[LatinIdentifier('t')]),
    dict(
        string='t₀e₁s₂t₃',
        expected=[
            LatinIdentifier('t', index=0),
            LatinIdentifier('e', index=1),
            LatinIdentifier('s', index=2),
            LatinIdentifier('t', index=3)
        ]
    ),
)
def test_valid_latin_identifiers(string: str, expected: Sequence[str]) -> None:
    assert tokenize(string) == expected


def test_cyrillic_identifier() -> None:
    with pytest.raises(ParsingError) as excinfo:
        tokenize('Т')

    assert str(excinfo.value) == 'Unexpected symbol'


def test_capitalized_identifiers() -> None:
    with pytest.raises(ParsingError) as excinfo:
        tokenize('T')

    assert str(excinfo.value) == 'Unexpected symbol'


def test_type_assignments() -> None:
    assert tokenize('x: τ') == [
        LatinIdentifier('x'),
        MiscToken.colon,
        MiscToken.space,
        GreekIdentifier('τ')
    ]
