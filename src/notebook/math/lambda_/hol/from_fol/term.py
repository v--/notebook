from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from .....support.coderefs import collector
from ....logic.terms import FunctionApplication, Term, TermVisitor
from ....logic.terms import Variable as FolVariable
from ...terms import Constant, TypedApplication, TypedTerm
from ...terms import Variable as LambdaVariable
from ...type_context import TypeContext
from ...variables import get_free_variables
from .. import common
from ..expression import HolExpression
from .signature import fol_signature_to_hol_signature


if TYPE_CHECKING:
    from ....logic.signature.signature import FormalLogicSignature
    from ..signature import HolSignature


@dataclass(frozen=True)
class TermTranslationVisitor(TermVisitor):
    fol_signature: FormalLogicSignature
    hol_signature: HolSignature

    @override
    def visit_variable(self, term: FolVariable) -> LambdaVariable:
        return LambdaVariable(term.identifier)

    @override
    def visit_function(self, term: FunctionApplication) -> TypedTerm:
        result: TypedTerm = Constant(self.hol_signature.get_nonlogical_constant_symbol(term.symbol.name))

        for arg in term.arguments:
            result = TypedApplication(result, self.visit(arg))

        return result


@collector.ref('alg:fol_to_hol/term')
def fol_term_to_hol_expression(fol_signature: FormalLogicSignature, fol_term: Term) -> HolExpression:
    hol_signature = fol_signature_to_hol_signature(fol_signature)
    hol_term = TermTranslationVisitor(fol_signature, hol_signature).visit(fol_term)
    context = TypeContext(dict.fromkeys(get_free_variables(hol_term), common.individual))
    return HolExpression(hol_term, common.individual, context)
