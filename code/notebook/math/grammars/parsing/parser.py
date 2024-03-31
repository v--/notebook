from typing import Iterable

from ....parsing.mixins.whitespace import WhitespaceTokenizerMixin
from ....parsing.parser import Parser
from ....parsing.whitespace import Whitespace
from ..alphabet import NonTerminal, Terminal
from ..grammar import GrammarRule, GrammarSchema
from .tokenizer import GrammarTokenizer
from .tokens import GrammarToken, MiscToken


class GrammarParser(WhitespaceTokenizerMixin[GrammarToken], Parser[GrammarToken]):
    def parse_rule_src(self) -> Iterable[Terminal | NonTerminal]:
        assert isinstance(self.peek(), Terminal | NonTerminal)
        contains_nonterminal = False

        while isinstance(head := self.peek(), Terminal | NonTerminal):
            yield head
            self.advance_and_skip_spaces()

            contains_nonterminal |= isinstance(head, NonTerminal)

        if not contains_nonterminal:
            raise self.error('The left side of a rule must contain at least one nonterminal')

    def parse_rule_dest(self) -> Iterable[Terminal | NonTerminal]:
        assert isinstance(self.peek(), Terminal | NonTerminal) or self.peek() == MiscToken.epsilon
        is_epsilon_rule = self.peek() == MiscToken.epsilon

        if is_epsilon_rule:
            self.advance_and_skip_spaces()

        while isinstance(head := self.peek(), Terminal | NonTerminal) or head == MiscToken.epsilon:
            if is_epsilon_rule:
                raise self.error('ε is only allowed on its own on the right side of a rule')
            else:
                assert isinstance(head, Terminal | NonTerminal)
                yield head
                self.advance_and_skip_spaces()

    def parse_rule_line(self) -> Iterable[GrammarRule]:
        self.skip_spaces()

        if not isinstance(self.peek(), Terminal | NonTerminal):
            raise self.error('The left side of a rule must consist of only terminals and nonterminals')

        src = list(self.parse_rule_src())

        if self.peek() == MiscToken.right_arrow:
            self.advance_and_skip_spaces()
        else:
            raise self.error('Expected an arrow after the rule source')

        while not self.is_at_end():
            if not isinstance(self.peek(), Terminal | NonTerminal) and self.peek() != MiscToken.epsilon:
                raise self.error('The right side of a rule must consist of terminals and nonterminals or of a single ε')

            dest = list(self.parse_rule_dest())
            yield GrammarRule(src, dest)

            if self.peek() == Whitespace.line_break:
                self.advance_and_skip_spaces()
                return

            if self.peek() == MiscToken.pipe:
                self.advance_and_skip_spaces()
            else:
                raise self.error('The right side of a rule must contain a pipe between runs of terminals, nonterminals and ε')

    def parse_all_rules(self):
        while not self.is_at_end():
            yield from self.parse_rule_line()
            self.skip_empty_lines()

    def parse_schema(self):
        self.skip_empty_lines()
        rules = list(self.parse_all_rules())

        if len(rules) == 0:
            raise self.error('Expected at least one grammar rule')

        return GrammarSchema(rules)

    parse = parse_schema


def parse_grammar_schema(string: str) -> GrammarSchema:
    tokens = list(GrammarTokenizer(string).parse())
    parser = GrammarParser(tokens)
    schema = parser.parse_schema()
    parser.assert_exhausted()
    return schema
