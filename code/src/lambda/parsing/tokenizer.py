from ...support.parsing.identifiers import Capitalization, LatinIdentifier
from ...support.parsing.tokenizer import BaseTokenizer
from .tokens import LambdaToken, MiscToken


class LambdaTokenizer(BaseTokenizer[LambdaToken]):
    def parse_step(self, head: str) -> LambdaToken:
        sym = MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if self.accept_alphabetic_string(LatinIdentifier, Capitalization.mixed):
            return self.parse_identifier(LatinIdentifier, Capitalization.mixed, short=True)

        raise self.error('Unexpected symbol')
