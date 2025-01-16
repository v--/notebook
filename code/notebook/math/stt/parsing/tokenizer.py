from collections.abc import Sequence
from dataclasses import dataclass

from ....parsing.mixins.identifiers import IdentifierTokenizerMixin
from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ....support.unicode import Capitalization, is_greek_string, is_latin_string
from ..alphabet import LambdaTermConnective, RuleConnective, SimpleTypeConnective, TypeAssertionConnective
from ..signature import STTSignature
from .tokens import BaseTypeToken, ConstantTermToken, MiscToken, STTToken


@dataclass
class STTTokenizer(IdentifierTokenizerMixin[STTToken], Tokenizer[STTToken]):
    signature: STTSignature

    def parse_step(self, head: str) -> STTToken:
        if sym := LambdaTermConnective.try_match(head) or \
            SimpleTypeConnective.try_match(head) or \
            TypeAssertionConnective.try_match(head) or \
            RuleConnective.try_match(head) or \
            MiscToken.try_match(head):
            self.advance()
            return sym

        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        for bt in self.signature.base_types:
            if self.peek_multiple(len(bt)) == bt:
                self.advance(len(bt))
                return BaseTypeToken(bt)

        for ct in self.signature.constant_terms:
            if self.peek_multiple(len(ct)) == ct:
                self.advance(len(ct))
                return ConstantTermToken(ct)

        if is_latin_string(head, Capitalization.lower):
            return self.parse_latin_identifier(Capitalization.lower)

        if is_latin_string(head, Capitalization.upper):
            return self.parse_latin_identifier(Capitalization.upper)

        if is_greek_string(head, Capitalization.lower):
            return self.parse_greek_identifier(Capitalization.lower)

        raise self.error('Unexpected symbol')


def tokenize_stt_string(signature: STTSignature, string: str) -> Sequence[STTToken]:
    with STTTokenizer(string, signature) as tokenizer:
        return list(tokenizer.parse())
