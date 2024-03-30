from ...support.parsing.identifiers import Capitalization, LatinIdentifier
from ...support.parsing.tokenizer import Tokenizer
from ...support.parsing.mixins.identifiers import IdentifierTokenizerMixin
from .tokens import LambdaToken, MiscToken


class LambdaTokenizer(IdentifierTokenizerMixin[LambdaToken], Tokenizer[LambdaToken]):
    def parse_step(self, head: str) -> LambdaToken:
        sym = MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if self.accept_alphabetic_string(LatinIdentifier, Capitalization.mixed):
            return self.parse_identifier(LatinIdentifier, Capitalization.mixed, short=True)

        raise self.error('Unexpected symbol')
