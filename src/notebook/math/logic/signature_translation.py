from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import override

from .exceptions import SignatureTranslationError
from .formulas import (
    EqualityFormula,
    Formula,
    FormulaTransformationVisitor,
    PredicateApplication,
)
from .signature import SignatureSymbol
from .terms import FunctionApplication, Term, TermTransformationVisitor


@dataclass
class SignatureMorphism:
    mapping: Mapping[SignatureSymbol, SignatureSymbol]

    def __post_init__(self) -> None:
        for a, b in self.mapping.items():
            if a.kind != b.kind:
                raise SignatureTranslationError(f'Mismatch between the {a.get_readable_kind()} symbol {a.name!r} and the {b.get_readable_kind()} symbol {b.name!r}')

            if a.arity != b.arity:
                raise SignatureTranslationError(f'Mismatch between {a.name!r} of arity {a.arity} and {b.name!r} of arity {b.arity}')


@dataclass
class TermTranslationVisitor(TermTransformationVisitor):
    translation: SignatureMorphism

    @override
    def visit_function(self, term: FunctionApplication) -> Term:
        return FunctionApplication(
            self.translation.mapping[term.symbol],
            [self.visit(arg) for arg in term.arguments]
        )


# This is alg:fol_term_signature_translation in the monograph
def translate_term(translation: SignatureMorphism, term: Term) -> Term:
    return TermTranslationVisitor(translation).visit(term)


@dataclass
class FormulaTranslationVisitor(FormulaTransformationVisitor):
    translation: SignatureMorphism
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
            self.translation.mapping[formula.symbol],
            [self.term_visitor.visit(arg) for arg in formula.arguments]
        )


# This is alg:fol_formula_signature_translation in the monograph
def translate_formula(translation: SignatureMorphism, formula: Formula) -> Formula:
    return FormulaTranslationVisitor(translation).visit(formula)
