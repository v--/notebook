from collections.abc import Sequence
from dataclasses import dataclass

from ....parsing.mixins.identifiers import IdentifierTokenizerMixin
from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ....support.inference.rules import InferenceRuleConnective
from ....support.unicode import Capitalization, is_greek_string, is_latin_string
from ..alphabet import BinaryConnective, PropConstant, Quantifier, SchemaConnective, UnaryConnective
from ..signature import FormalLogicSignature
from .tokens import (
    CapitalizedLatinString,
    FunctionSymbolToken,
    LogicToken,
    MiscToken,
    PredicateSymbolToken,
    SuperscriptToken,
)


@dataclass
class FormalLogicTokenizer(IdentifierTokenizerMixin[LogicToken], Tokenizer[LogicToken]):
    signature: FormalLogicSignature

    def parse_step(self, head: str) -> LogicToken:
        sym = PropConstant.try_match(head) or \
            BinaryConnective.try_match(head) or \
            Quantifier.try_match(head) or \
            UnaryConnective.try_match(head) or \
            InferenceRuleConnective.try_match(head) or \
            SchemaConnective.try_match(head) or \
            MiscToken.try_match(head) or \
            SuperscriptToken.try_match(head)

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

        if is_latin_string(head, Capitalization.lower):
            return self.parse_latin_identifier()

        if is_latin_string(head, Capitalization.upper):
            return CapitalizedLatinString(
                self.gobble_string(lambda sym: is_latin_string(sym, Capitalization.mixed))
            )

        if is_greek_string(head, Capitalization.lower):
            return self.parse_greek_identifier(Capitalization.lower)

        raise self.error('Unexpected symbol')


def tokenize_formal_logic_string(signature: FormalLogicSignature, string: str) -> Sequence[LogicToken]:
    with FormalLogicTokenizer(string, signature) as tokenizer:
        return list(tokenizer.parse())
