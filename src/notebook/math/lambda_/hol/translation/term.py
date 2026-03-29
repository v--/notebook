from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from ....logic.terms import FunctionApplication, Term, TermVisitor
from ....logic.terms import Variable as LogicVariable
from ...assertions import VariableTypeAssertion
from ...terms import Constant, TypedApplication, TypedTerm
from ...terms import Variable as LambdaVariable
from ...types import BaseType
from ...variables import get_free_variables
from ..expressions import HolExpression
from ..signature import common_types
from .signature import fol_signature_to_hol_signature


if TYPE_CHECKING:
    from ....logic.signature.signature import FormalLogicSignature
    from ..signature import HolSignature


@dataclass(frozen=True)
class TermTranslationVisitor(TermVisitor):
    fol_signature: FormalLogicSignature
    hol_signature: HolSignature

    @override
    def visit_variable(self, term: LogicVariable) -> LambdaVariable:
        return LambdaVariable(term.identifier)

    @override
    def visit_function(self, term: FunctionApplication) -> TypedTerm:
        result: TypedTerm = Constant(self.hol_signature.get_nonlogical_constant_symbol(term.symbol.name))

        for arg in term.arguments:
            result = TypedApplication(result, self.visit(arg))

        return result


# alg:fol_term_to_hol_expression
def fol_term_to_hol_expression(fol_signature: FormalLogicSignature, fol_term: Term) -> HolExpression:
    hol_signature = fol_signature_to_hol_signature(fol_signature)
    hol_term = TermTranslationVisitor(fol_signature, hol_signature).visit(fol_term)
    context = [VariableTypeAssertion(var, BaseType(common_types.individual)) for var in get_free_variables(hol_term)]
    return HolExpression(hol_term, BaseType(common_types.individual), context)
