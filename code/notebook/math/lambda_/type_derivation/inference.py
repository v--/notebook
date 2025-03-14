from collections.abc import Mapping
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
from ..type_system import BASE_EXPLICIT_TYPE_SYSTEM
from ..types import SimpleType, is_arrow_type
from .exceptions import TypeInferenceError
from .tree import TypeDerivationTree, apply, assume, premise


# This is alg:simply_typed_term_type_derivation in the monograph
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
        subtree_a = self.visit(term.a)
        subtree_b = self.visit(term.b)

        if not is_arrow_type(subtree_a.conclusion.type) or subtree_a.conclusion.type.a != subtree_b.conclusion.type:
            raise TypeInferenceError(f'Incompatible types in application term {term}')

        return apply(
            BASE_EXPLICIT_TYPE_SYSTEM, '→⁻',
            premise(tree=subtree_a),
            premise(tree=subtree_b)
        )

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> TypeDerivationTree:
        subtree = TypeInferenceVisitor({**self.context, term.var: term.var_type}).visit(term.sub)

        return apply(
            BASE_EXPLICIT_TYPE_SYSTEM, '→⁺',
            premise(tree=subtree, discharge=VariableTypeAssertion(term.var, term.var_type))
        )


def derive_type(term: TypedTerm, context: Mapping[Variable, SimpleType] = {}) -> TypeDerivationTree:
    return TypeInferenceVisitor(context=context).visit(term)


def infer_type(term: TypedTerm, context: Mapping[Variable, SimpleType]) -> SimpleType:
    return derive_type(term, context).conclusion.type
