from typing import Iterable

from ...support.parsing.parser import Parser
from ..alphabet import Terminal, NonTerminal
from ..grammar import GrammarRule, GrammarSchema
from .tokens import MiscToken, GrammarToken
from .tokenizer import GrammarTokenizer


class GrammarParser(Parser[GrammarToken]):
    def skip_whitespace(self):
        while not self.is_at_end() and self.peek() == MiscToken.space:
            self.advance()

    def skip_empty_lines(self):
        while not self.is_at_end() and self.peek() == MiscToken.new_line:
            self.advance()
            self.skip_whitespace()

    def advance_and_with_whitespace(self):
        self.advance()
        self.skip_whitespace()

    def parse_rule_src(self) -> Iterable[Terminal | NonTerminal]:
        assert isinstance(self.peek(), Terminal | NonTerminal)
        contains_nonterminal = False

        while isinstance(head := self.peek(), Terminal | NonTerminal):
            yield head
            self.advance_and_with_whitespace()

            contains_nonterminal |= isinstance(head, NonTerminal)

        if not contains_nonterminal:
            raise self.error('The left side of a rule must contain at least one nonterminal')

    def parse_rule_dest(self) -> Iterable[Terminal | NonTerminal]:
        assert isinstance(self.peek(), Terminal | NonTerminal) or self.peek() == MiscToken.epsilon
        is_epsilon_rule = self.peek() == MiscToken.epsilon

        if is_epsilon_rule:
            self.advance_and_with_whitespace()

        while isinstance(head := self.peek(), Terminal | NonTerminal) or head == MiscToken.epsilon:
            if is_epsilon_rule:
                raise self.error('ε is only allowed on its own on the right side of a rule')
            else:
                assert isinstance(head, Terminal | NonTerminal)
                yield head
                self.advance_and_with_whitespace()

    def parse_rule_line(self) -> Iterable[GrammarRule]:
        self.skip_whitespace()

        if not isinstance(self.peek(), Terminal | NonTerminal):
            raise self.error('The left side of a rule must consist of only terminals and nonterminals')

        src = list(self.parse_rule_src())

        if self.peek() == MiscToken.right_arrow:
            self.advance_and_with_whitespace()
        else:
            raise self.error('Expected an arrow after the rule source')

        while not self.is_at_end():
            if not isinstance(self.peek(), Terminal | NonTerminal) and self.peek() != MiscToken.epsilon:
                raise self.error('The right side of a rule must consist of terminals and nonterminals or of a single ε')

            dest = list(self.parse_rule_dest())
            yield GrammarRule(src, dest)

            if self.peek() == MiscToken.new_line:
                self.advance_and_with_whitespace()
                return

            if self.peek() == MiscToken.pipe:
                self.advance_and_with_whitespace()
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
