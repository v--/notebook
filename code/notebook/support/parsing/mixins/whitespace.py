from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from ..tokens import AbstractToken
from ..tokenizer import Parser
from ..whitespace import Whitespace


T_co = TypeVar('T_co', bound=AbstractToken)


class WhitespaceTokenizerMixin(Parser[T_co]):
    def skip_spaces(self):
        while not self.is_at_end() and self.peek() == Whitespace.space:
            self.advance()

    def skip_empty_lines(self):
        while not self.is_at_end() and self.peek() == Whitespace.line_break:
            self.advance()
            self.skip_spaces()

    def advance_and_skip_spaces(self):
        self.advance()
        self.skip_spaces()
