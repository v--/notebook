from collections.abc import Sequence

from ....parsing.mixins.identifiers import IdentifierTokenizerMixin
from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ....support.unicode import Capitalization, is_greek_string, is_latin_string
from ...fol.alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from .tokens import CapitalLatinString, MiscToken, RuleToken, SuperscriptToken


class NaturalDeductionTokenizer(IdentifierTokenizerMixin[RuleToken], Tokenizer[RuleToken]):
    def _eagerly_parse_latin_string(self) -> CapitalLatinString:
        assert is_latin_string(self.peek(), Capitalization.capital)
        string = ''

        while is_latin_string(self.peek(), Capitalization.capital):
            string += self.peek()
            self.advance()

        return CapitalLatinString(string)

    def parse_step(self, head: str) -> RuleToken:
        sym = PropConstant.try_match(head) or \
            BinaryConnective.try_match(head) or \
            Quantifier.try_match(head) or \
            UnaryConnective.try_match(head) or \
            MiscToken.try_match(head) or \
            SuperscriptToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        if is_greek_string(head, Capitalization.small):
            return self.parse_greek_identifier()

        if is_latin_string(head, Capitalization.small):
            return self.parse_latin_identifier()

        if is_latin_string(head, Capitalization.capital):
            return self._eagerly_parse_latin_string()

        raise self.error('Unexpected symbol')


def tokenize_nd_string(string: str) -> Sequence[RuleToken]:
    with NaturalDeductionTokenizer(string) as tokenizer:
        return list(tokenizer.parse())
