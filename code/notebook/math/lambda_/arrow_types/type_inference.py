from collections.abc import Mapping
from dataclasses import dataclass
from typing import Never, override

from ..arrow_types import ARROW_ONLY_TYPE_SYSTEM
from ..assertions import VariableTypeAssertion
from ..terms import (
    Constant,
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
    TypedTermVisitor,
    Variable,
)
from ..type_derivation import TypeDerivationTree, TypeInferenceError, apply, assume, premise
from ..types import SimpleType, is_arrow_type


# This is alg:simply_typed_term_type_inference in the monograph
@dataclass(frozen=True)
class TypeInferenceVisitor(TypedTermVisitor[TypeDerivationTree]):
    context: Mapping[Variable, SimpleType]

    @override
    def visit_constant(self, term: Constant) -> Never:
        raise TypeInferenceError('Cannot infer a type for constants')

    @override
    def visit_variable(self, term: Variable) -> TypeDerivationTree:
        if term in self.context:
            return assume(VariableTypeAssertion(term, self.context[term]))

        raise TypeInferenceError(f'No type specified for variable {term}')

    @override
    def visit_application(self, term: TypedApplication) -> TypeDerivationTree:
        left_subtree = self.visit(term.left)
        right_subtree = self.visit(term.right)

        if not is_arrow_type(left_subtree.conclusion.type) or left_subtree.conclusion.type.left != right_subtree.conclusion.type:
            raise TypeInferenceError(f'Incompatible types in application term {term}')

        return apply(
            ARROW_ONLY_TYPE_SYSTEM['→₋'],
            premise(tree=left_subtree),
            premise(tree=right_subtree)
        )

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> TypeDerivationTree:
        subtree = TypeInferenceVisitor({**self.context, term.var: term.var_type}).visit(term.body)

        return apply(
            ARROW_ONLY_TYPE_SYSTEM['→₊'],
            premise(tree=subtree, discharge=VariableTypeAssertion(term.var, term.var_type))
        )


def derive_type(term: TypedTerm, context: Mapping[Variable, SimpleType] = {}) -> TypeDerivationTree:
    return TypeInferenceVisitor(context=context).visit(term)


def infer_type(term: TypedTerm, context: Mapping[Variable, SimpleType]) -> SimpleType:
    return derive_type(term, context).conclusion.type
