from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from .....support.substitution.exceptions import UnspecifiedReplacementError
from ...assertions import VariableTypeAssertion
from ...terms import Constant, TypedAbstraction, TypedApplication, TypedTerm, TypedTermVisitor, Variable
from ..tree import TypeDerivationTree, assume
from .substitution import TypeDerivationSubstitution


@dataclass(frozen=True)
class TypedSubstitutionApplicationVisitor(TypedTermVisitor[TypedTerm]):
    substitution: TypeDerivationSubstitution

    @override
    def visit_constant(self, term: Constant) -> Constant:
        return term

    @override
    def visit_variable(self, term: Variable) -> TypedTerm:
        try:
            result = self.substitution.substitute_variable(term)
        except UnspecifiedReplacementError:
            return term

        return result.conclusion.term

    @override
    def visit_application(self, term: TypedApplication) -> TypedApplication:
        return TypedApplication(self.visit(term.left), self.visit(term.right))

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> TypedAbstraction:
        new_var = self.substitution.get_modified_abstractor_variable(term)
        new_subst = self.substitution.modify_at(term.var, assume(VariableTypeAssertion(new_var, term.var_type)))
        new_subterm = apply_tree_substitution_to_term(term.body, new_subst)
        return TypedAbstraction(new_var, term.var_type, new_subterm)


# This is alg:simply_typed_substitution in the monograph
def apply_tree_substitution_to_term(term: TypedTerm, substitution: TypeDerivationSubstitution) -> TypedTerm:
    return TypedSubstitutionApplicationVisitor(substitution).visit(term)


def substitute_term(term: TypedTerm, variable_mapping: Mapping[Variable, TypeDerivationTree]) -> TypedTerm:
    return apply_tree_substitution_to_term(term, TypeDerivationSubstitution(variable_mapping=variable_mapping))
