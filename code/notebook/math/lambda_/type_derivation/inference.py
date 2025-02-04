from collections.abc import Collection
from dataclasses import dataclass
from typing import Never, override

from ..assertions import VariableTypeAssertion
from ..terms import (
    Constant,
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
    TypedTermVisitor,
    Variable,
)
from ..type_systems import ARROW_ELIM_RULE_EXPLICIT, ARROW_INTRO_RULE_EXPLICIT
from ..types import SimpleType, is_arrow_type
from .exceptions import TypeInferenceError
from .tree import RuleApplicationPremise, TypeDerivationTree, apply, assume


# This is alg:typed_term_type_derivation in the monograph
@dataclass(frozen=True)
class TypeInferenceVisitor(TypedTermVisitor[TypeDerivationTree]):
    context: Collection[VariableTypeAssertion]

    @override
    def visit_constant(self, term: Constant) -> Never:
        raise TypeInferenceError('Cannot infer a type for constants')

    @override
    def visit_variable(self, term: Variable) -> TypeDerivationTree:
        for assertion in self.context:
            if assertion.term == term:
                return assume(assertion)

        raise TypeInferenceError(f'No type specified for variable {term}')

    @override
    def visit_application(self, term: TypedApplication) -> TypeDerivationTree:
        subtree_a = self.visit(term.a)
        subtree_b = self.visit(term.b)

        if not is_arrow_type(subtree_a.conclusion.type) or subtree_a.conclusion.type.a != subtree_b.conclusion.type:
            raise TypeInferenceError(f'Incompatible types in application term {term}')

        return apply(
            ARROW_ELIM_RULE_EXPLICIT,
            RuleApplicationPremise(tree=subtree_a),
            RuleApplicationPremise(tree=subtree_b)
        )

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> TypeDerivationTree:
        assertion = VariableTypeAssertion(term.var, term.var_type)
        subtree = TypeInferenceVisitor({*self.context, assertion}).visit(term.sub)

        return apply(
            ARROW_INTRO_RULE_EXPLICIT,
            RuleApplicationPremise(tree=subtree, discharge=assertion)
        )


def derive_type(term: TypedTerm) -> TypeDerivationTree:
    return TypeInferenceVisitor(context=set()).visit(term)


def infer_type(term: TypedTerm) -> SimpleType:
    return derive_type(term).conclusion.type
