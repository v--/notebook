from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from textwrap import dedent

import pytest

from ...support.pytest import pytest_parametrize_lists
from ...support.unicode import Capitalization, is_latin_string
from ..exceptions import ParsingError
from ..identifiers import LatinIdentifier
from ..old_tokens import TokenEnum
from ..whitespace import Space, Whitespace
from .old_identifiers import IdentifierTokenizerMixin
from .old_inference_rules import InferenceRuleParserMixin
from .whitespace import WhitespaceParserMixin


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    comma = ','
    sequent = '⫢'


SimpleToken = LatinIdentifier | MiscToken | Space


class SimpleTokenizer(IdentifierTokenizerMixin[SimpleToken]):
    def parse_step(self, head: str) -> SimpleToken:
        if sym := MiscToken.try_match(head):
            self.advance()
            return sym

        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        if is_latin_string(head, Capitalization.mixed):
            return self.parse_latin_identifier(Capitalization.mixed)

        raise self.error('Unexpected symbol')


@dataclass(frozen=True)
class SimpleSentence:
    id: LatinIdentifier

    def __str__(self) -> str:
        return str(self.id)


@dataclass(frozen=True)
class SimpleRule:
    name: str
    premises: Sequence[SimpleSentence]
    conclusion: SimpleSentence

    def __str__(self) -> str:
        if len(self.premises) > 0:
            premise_str = ', '.join(map(str, self.premises))
            return f'({self.name}) {premise_str} {MiscToken.sequent} {self.conclusion}'

        return f'({self.name}) {MiscToken.sequent} {self.conclusion}'

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(tuple(self.premises)) ^ hash(self.conclusion)


class SimpleRuleParser(WhitespaceParserMixin[SimpleToken], InferenceRuleParserMixin[SimpleToken]):
    def parse_sentence(self) -> SimpleSentence:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()
        return SimpleSentence(head)

    def iter_premises(self) -> Iterable[SimpleSentence]:
        for _ in self.iter_parse_premise_positions(MiscToken.sequent, MiscToken.comma):
            self.skip_spaces()
            yield self.parse_sentence()
            self.skip_spaces()

    def parse_rule(self) -> SimpleRule:
        name = self.parse_rule_name(MiscToken.left_parenthesis, MiscToken.right_parenthesis)
        self.advance_and_skip_spaces()
        premises = list(self.iter_premises())
        self.advance_and_skip_spaces()
        return SimpleRule(name, premises, self.parse_sentence())


def parse_rule(string: str) -> SimpleRule:
    with SimpleTokenizer(string) as tokenizer:
        tokens = list(tokenizer.parse())

    with SimpleRuleParser(tokens) as parser:
        return parser.parse_rule()


@pytest_parametrize_lists(
    rule=[
        '(R) ⫢ y',
        '(R) x ⫢ y',
        '(R) x₁, x₂ ⫢ y'
    ]
)
def test_rebuilding_rules(rule: str) -> None:
    assert str(parse_rule(rule)) == rule


def test_parsing_without_rule_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('x ⫢ y')

    assert str(excinfo.value) == 'A rule must start with a parenthesized name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x ⫢ y
          │ ^
        '''
    )


def test_parsing_with_empty_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('() x ⫢ y')

    assert str(excinfo.value) == 'The name of a rule cannot be empty'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ () x ⫢ y
          │ ^^
        '''
    )


def test_parsing_rule_with_unclosed_parens() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R x ⫢ y')

    assert str(excinfo.value) == 'Unclosed parenthesis after rule name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R x ⫢ y
          │ ^^^^^^^^
        '''
    )


def test_parsing_rule_with_no_comma() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) x₁ x₂ ⫢ y')

    assert str(excinfo.value) == 'Expected either a separator or a sequent symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) x₁ x₂ ⫢ y
          │        ^^
        '''
    )


def test_parsing_rule_with_no_conclusion() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) x')

    assert str(excinfo.value) == 'Expected a sequent symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) x
          │     ^
        '''
    )
