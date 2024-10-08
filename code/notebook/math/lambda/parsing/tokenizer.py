from collections.abc import Sequence

from ....parsing.mixins.identifiers import IdentifierTokenizerMixin
from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ....support.unicode import Capitalization, is_latin_string
from .tokens import LambdaToken, MiscToken


class LambdaTokenizer(IdentifierTokenizerMixin[LambdaToken], Tokenizer[LambdaToken]):
    def parse_step(self, head: str) -> LambdaToken:
        if sym := MiscToken.try_match(head):
            self.advance()
            return sym

        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        if is_latin_string(head, Capitalization.lower):
            return self.parse_latin_identifier()

        raise self.error('Unexpected symbol')


def tokenize_lambda_term(string: str) -> Sequence[LambdaToken]:
    with LambdaTokenizer(string) as tokenizer:
        return list(tokenizer.parse())
