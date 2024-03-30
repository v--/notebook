from ...support.parsing.identifiers import Capitalization, LatinIdentifier, GreekIdentifier
from ...support.parsing.tokenizer import Tokenizer
from ...support.parsing.mixins.identifiers import IdentifierTokenizerMixin
from ..alphabet import BinaryConnective, PropConstant, Quantifier
from .tokens import FOLToken, MiscToken


class FOLTokenizer(IdentifierTokenizerMixin[FOLToken], Tokenizer[FOLToken]):
    def parse_step(self, head: str) -> FOLToken:
        sym = PropConstant.try_match(head) or \
            BinaryConnective.try_match(head) or \
            Quantifier.try_match(head) or \
            MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if self.accept_alphabetic_string(LatinIdentifier, Capitalization.mixed):
            return self.parse_identifier(LatinIdentifier, Capitalization.mixed, short=False)

        if self.accept_alphabetic_string(GreekIdentifier, Capitalization.mixed):
            return self.parse_identifier(GreekIdentifier, Capitalization.mixed, short=False)

        raise self.error('Unexpected symbol')
