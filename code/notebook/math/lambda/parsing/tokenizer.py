from ....parsing.identifiers import Capitalization, LatinIdentifier
from ....parsing.mixins.identifiers import IdentifierTokenizerMixin
from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from .tokens import LambdaToken, MiscToken


class LambdaTokenizer(IdentifierTokenizerMixin[LambdaToken], Tokenizer[LambdaToken]):
    def parse_step(self, head: str) -> LambdaToken:
        sym = MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        if self.accept_alphabetic_string(LatinIdentifier, Capitalization.mixed):
            return self.parse_identifier(LatinIdentifier, Capitalization.mixed, short=True)

        raise self.error('Unexpected symbol')
