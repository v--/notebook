from collections.abc import Iterable

from ..old_parser import Parser
from ..old_tokens import AbstractToken


class InferenceRuleParserMixin[T: AbstractToken](Parser[T]):
    def parse_rule_name(self, opening_delimiter: str, closing_delimiter: str) -> str:
        start = self.index

        if self.peek() == opening_delimiter:
            self.advance()
        else:
            raise self.error('A rule must start with a parenthesized name')

        name = self.gobble_string(lambda sym: sym != closing_delimiter)

        if name == '':
            raise self.error('The name of a rule cannot be empty', i_first_token=start)

        if self.is_at_end():
            raise self.error('Unclosed parenthesis after rule name', i_first_token=start)

        self.advance()
        return name

    def iter_parse_premise_positions(self, sequent: str, separator: str) -> Iterable[None]:
        while not self.is_at_end() and self.peek() != sequent:
            yield

            if self.is_at_end() or self.peek() == sequent:
                continue

            if self.peek() == separator:
                self.advance()
            else:
                raise self.error('Expected either a separator or a sequent symbol')

        if self.is_at_end():
            raise self.error('Expected a sequent symbol')
