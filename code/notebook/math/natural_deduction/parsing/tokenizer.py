from ....parsing.identifiers import (
    Capitalization,
    GreekIdentifier,
    LatinIdentifier,
)
from ....parsing.mixins.identifiers import IdentifierTokenizerMixin
from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ...fol.alphabet import BinaryConnective, PropConstant, Quantifier
from .tokens import MiscToken, RuleToken


class NaturalDeductionTokenizer(IdentifierTokenizerMixin[RuleToken], Tokenizer[RuleToken]):
    def parse_step(self, head: str) -> RuleToken:
        sym = PropConstant.try_match(head) or \
            BinaryConnective.try_match(head) or \
            Quantifier.try_match(head) or \
            MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        if self.is_at_alphabetic_string(LatinIdentifier, Capitalization.mixed):
            return self.parse_identifier(LatinIdentifier, Capitalization.mixed, short=False)

        if self.is_at_alphabetic_string(GreekIdentifier, Capitalization.mixed):
            return self.parse_identifier(GreekIdentifier, Capitalization.mixed, short=False)

        raise self.error('Unexpected symbol')
