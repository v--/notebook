from dataclasses import dataclass, field
from typing import TYPE_CHECKING, overload, override

from notebook.math.lambda_.alphabet import BinaryTypeConnective
from notebook.math.lambda_.arrow_types.type_inference import infer_type
from notebook.math.lambda_.terms import (
    Constant,
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
    TypedTermVisitor,
    Variable,
)
from notebook.math.lambda_.type_context import TypeContext
from notebook.math.lambda_.types import SimpleConnectiveType, SimpleType
from notebook.math.lambda_.variables import get_free_variables
from notebook.support.coderefs import collector
from notebook.support.name_collision import get_name_without_collision

from . import common
from .expression import HolExpression
from .signature import HolSignature, NonLogicalConstantSymbol
from .structure import HolStructure, HolStructureValue, HolVariableAssignment, evaluate_hol_expression


if TYPE_CHECKING:
    from collections.abc import Iterable, MutableMapping


@dataclass
class ExpressionTranslationVisitor[T](TypedTermVisitor[TypedTerm]):
    signature: HolSignature
    context: TypeContext
    structure: HolStructure[T] | None
    new_constants: MutableMapping[NonLogicalConstantSymbol, TypedAbstraction] = field(default_factory=dict)
    new_interpretation: MutableMapping[NonLogicalConstantSymbol, HolStructureValue[T]] = field(default_factory=dict)

    @override
    def visit_atomic(self, term: Constant | Variable) -> TypedTerm:
        return term

    @override
    def visit_application(self, term: TypedApplication) -> TypedApplication:
        if term.left == common.forall or term.left == common.exists:
            if TYPE_CHECKING:
                assert isinstance(term.right, TypedAbstraction)

            return TypedApplication(
                term.left,
                TypedAbstraction(
                    term.right.var,
                    term.right.var_type,
                    self.visit(term.right.body),
                ),
            )

        return TypedApplication(self.visit(term.left), self.visit(term.right))

    def _produce_new_nl_type(self, type_: SimpleType, variables: Iterable[Variable]) -> SimpleType:
        try:
            var, *rest = variables
        except ValueError:
            return type_
        else:
            return SimpleConnectiveType(
                BinaryTypeConnective.ARROW,
                self.context[var],
                self._produce_new_nl_type(type_, rest),
            )

    def _produce_new_nl_occurrence(self, sym: NonLogicalConstantSymbol, variables: Iterable[Variable]) -> TypedTerm:
        try:
            var, *rest = variables
        except ValueError:
            return Constant(sym)
        return TypedApplication(
            self._produce_new_nl_occurrence(sym, rest),
            var,
        )

    def _produce_new_nl_interpretation(
        self,
        expression: HolExpression,
        variables: Iterable[Variable],
        assignment: HolVariableAssignment[T],
    ) -> HolStructureValue[T]:
        if TYPE_CHECKING:
            assert self.structure

        try:
            var, *rest = variables
        except ValueError:
            return evaluate_hol_expression(expression, self.structure, assignment)
        else:
            return lambda a: self._produce_new_nl_interpretation(
                expression,
                rest,
                assignment.modify(var, self.context[var], a),
            )

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> TypedTerm:
        term_type = infer_type(term, self.context)
        nl_sym_name = get_name_without_collision(
            'Λ₁',
            {sym.name for sym in self.signature} | {sym.name for sym in self.new_constants},
        )

        variables = get_free_variables(term)
        nl_sym = NonLogicalConstantSymbol(nl_sym_name, self._produce_new_nl_type(term_type, variables))
        expression = HolExpression(term, term_type, TypeContext({var: self.context[var] for var in variables}))
        self.new_constants[nl_sym] = term

        if self.structure:
            self.new_interpretation[nl_sym] = self._produce_new_nl_interpretation(
                expression,
                variables,
                HolVariableAssignment(),
            )

        return self._produce_new_nl_occurrence(nl_sym, variables)


@dataclass
class EliminateAbstractionsResult[T]:
    signature: HolSignature
    expression: HolExpression
    structure: HolStructure[T] | None


@overload
def eliminate_abstractions(
    signature: HolSignature,
    expression: HolExpression,
) -> EliminateAbstractionsResult: ...
@overload
def eliminate_abstractions[T](
    signature: HolSignature,
    expression: HolExpression,
    structure: HolStructure[T],
) -> EliminateAbstractionsResult[T]: ...
@collector.ref('alg:hol_abstraction_elimination')
def eliminate_abstractions[T](
    signature: HolSignature,
    expression: HolExpression,
    structure: HolStructure[T] | None = None,
) -> EliminateAbstractionsResult[T]:
    visitor = ExpressionTranslationVisitor(signature, expression.context, structure)

    # It is essential that we build the new expression first,
    # because the new constants and new interpretation would not be populated otherwise
    translated_expression = HolExpression(
        visitor.visit(expression.term),
        expression.type,
        expression.context,
    )

    translated_signature = HolSignature(*signature, *visitor.new_constants.keys())

    if structure:
        translated_structure = HolStructure(
            translated_signature,
            structure.sort_universes,
            {**structure.interpretation, **visitor.new_interpretation},
        )
    else:
        translated_structure = None

    return EliminateAbstractionsResult(
        translated_signature,
        translated_expression,
        translated_structure,
    )
