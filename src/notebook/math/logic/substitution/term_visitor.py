from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from ..terms import FunctionApplication, Term, TermTransformationVisitor, Variable
from .substitution import LogicSubstitution


@dataclass(frozen=True)
class TermSubstitutionVisitor(TermTransformationVisitor):
    substitution: LogicSubstitution

    @override
    def visit_variable(self, term: Variable) -> Term:
        return self.substitution.substitute_variable(term)

    @override
    def visit_function(self, term: FunctionApplication) -> Term:
        return FunctionApplication(term.name, [self.visit(arg) for arg in term.arguments])


def apply_term_substitution(term: Term, substitution: LogicSubstitution) -> Term:
    return TermSubstitutionVisitor(substitution).visit(term)


def substitute_in_term(term: Term, variable_mapping: Mapping[Variable, Term]) -> Term:
    return apply_term_substitution(term, LogicSubstitution(variable_mapping=variable_mapping))
