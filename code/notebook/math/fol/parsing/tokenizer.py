from dataclasses import dataclass

from ....parsing.identifiers import (
    Capitalization,
    GreekIdentifier,
)
from ....parsing.mixins.identifiers import IdentifierTokenizerMixin
from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from ..signature import FOLSignature
from .tokens import FOLToken, FunctionSymbolToken, MiscToken, PredicateSymbolToken


@dataclass
class FOLTokenizer(IdentifierTokenizerMixin[FOLToken], Tokenizer[FOLToken]):
    signature: FOLSignature

    def parse_step(self, head: str) -> FOLToken:
        sym = PropConstant.try_match(head) or \
            BinaryConnective.try_match(head) or \
            Quantifier.try_match(head) or \
            UnaryConnective.try_match(head) or \
            MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        for fs in self.signature.iter_function_symbols():
            if self.peek_multiple(len(fs)) == fs:
                self.advance(len(fs))
                return FunctionSymbolToken(fs)

        for ps in self.signature.iter_predicate_symbols():
            if self.peek_multiple(len(ps)) == ps:
                self.advance(len(ps))
                return PredicateSymbolToken(ps)

        if self.is_at_alphabetic_string(GreekIdentifier, Capitalization.mixed):
            return self.parse_identifier(GreekIdentifier, Capitalization.mixed, short=False)

        raise self.error('Unexpected symbol')


def tokenize_fol_string(signature: FOLSignature, string: str) -> list[FOLToken]:
    with FOLTokenizer(string, signature) as tokenizer:
        return list(tokenizer.parse())
