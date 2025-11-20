from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import override

from .exceptions import FormalLogicError
from .formulas import (
    EqualityFormula,
    Formula,
    FormulaTransformationVisitor,
    PredicateApplication,
)
from .signature import FormalLogicSignature
from .terms import FunctionApplication, Term, TermTransformationVisitor


class SignatureTranslationError(FormalLogicError):
    pass


@dataclass
class SignatureTranslation:
    src: FormalLogicSignature
    dest: FormalLogicSignature
    mapping: Mapping[str, str]

    def __post_init__(self) -> None:
        for a, b in self.mapping.items():
            try:
                sym_a = self.src.get_symbol(a)
            except LookupError:
                raise SignatureTranslationError(f'Symbol {a!r} is not present in signature') from None

            try:
                sym_b = self.dest.get_symbol(b)
            except LookupError:
                raise SignatureTranslationError(f'Symbol {a!r} is not present in signature') from None

            if sym_a.kind != sym_b.kind:
                raise SignatureTranslationError(f'Mismatch between the {sym_a.kind.lower()} symbol {a!r} and the {sym_b.kind.lower()} symbol {b!r}')

            if sym_a.arity != sym_b.arity:
                raise SignatureTranslationError(f'Mismatch between {a!r} of arity {sym_a.arity} and {b!r} of arity {sym_b.arity}')


@dataclass
class TermTranslationVisitor(TermTransformationVisitor):
    translation: SignatureTranslation

    @override
    def visit_function(self, term: FunctionApplication) -> Term:
        return FunctionApplication(
            self.translation.mapping[term.name],
            [self.visit(arg) for arg in term.arguments]
        )


# This is alg:fol_term_signature_translation in the monograph
def translate_term(translation: SignatureTranslation, term: Term) -> Term:
    return TermTranslationVisitor(translation).visit(term)


@dataclass
class FormulaTranslationVisitor(FormulaTransformationVisitor):
    translation: SignatureTranslation
    term_visitor: TermTranslationVisitor = field(init=False)

    def __post_init__(self) -> None:
        self.term_visitor = TermTranslationVisitor(self.translation)

    @override
    def visit_equality(self, formula: EqualityFormula) -> EqualityFormula:
        return EqualityFormula(
            self.term_visitor.visit(formula.left),
            self.term_visitor.visit(formula.right)
        )

    @override
    def visit_predicate(self, formula: PredicateApplication) -> PredicateApplication:
        return PredicateApplication(
            self.translation.mapping[formula.name],
            [self.term_visitor.visit(arg) for arg in formula.arguments]
        )


# This is alg:fol_signature_translation in the monograph
def translate_formula(translation: SignatureTranslation, formula: Formula) -> Formula:
    return FormulaTranslationVisitor(translation).visit(formula)
