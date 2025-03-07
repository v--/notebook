from collections.abc import Sequence
from dataclasses import dataclass

from ....parsing.mixins.old_identifiers import IdentifierTokenizerMixin
from ....parsing.old_tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ....support.inference.rules import InferenceRuleConnective
from ....support.unicode import Capitalization, is_greek_string, is_latin_string
from ..alphabet import BinaryTypeConnective, TermConnective, TypeAssertionConnective
from ..signature import LambdaSignature
from .tokens import BaseTypeToken, ConstantTermToken, LambdaToken, MiscToken, SuperscriptToken


@dataclass
class LambdaTokenizer(IdentifierTokenizerMixin[LambdaToken], Tokenizer[LambdaToken]):
    signature: LambdaSignature

    def parse_step(self, head: str) -> LambdaToken:
        if sym := TermConnective.try_match(head) or \
            BinaryTypeConnective.try_match(head) or \
            TypeAssertionConnective.try_match(head) or \
            InferenceRuleConnective.try_match(head) or \
            SuperscriptToken.try_match(head) or \
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


def tokenize_lambda_string(signature: LambdaSignature, string: str) -> Sequence[LambdaToken]:
    with LambdaTokenizer(string, signature) as tokenizer:
        return list(tokenizer.parse())
