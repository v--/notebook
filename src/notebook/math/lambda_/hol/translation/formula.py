from dataclasses import dataclass, field
from typing import TYPE_CHECKING, override

from ....logic.alphabet import BinaryConnective, PropConstantSymbol, Quantifier
from ....logic.formulas import (
    ConnectiveFormula,
    Formula,
    FormulaVisitor,
    NegationFormula,
    PredicateApplication,
    PropConstant,
    QuantifierFormula,
)
from ...assertions import VariableTypeAssertion
from ...terms import Constant, TypedAbstraction, TypedApplication, TypedTerm
from ...types import BaseType
from ...variables import get_free_variables
from ..expressions import HolExpression
from ..symbols import LogicalConstantSymbol, common_constants, common_types
from .signature import fol_signature_to_hol_signature
from .term import TermTranslationVisitor


if TYPE_CHECKING:
    from ....logic.signature.signature import FormalLogicSignature
    from ..signature import HolSignature


def connective_to_logical_constant(conn: BinaryConnective) -> LogicalConstantSymbol:
    match conn:
        case BinaryConnective.CONJUNCTION:
            return common_constants.conjunction

        case BinaryConnective.DISJUNCTION:
            return common_constants.disjunction

        case BinaryConnective.CONDITIONAL:
            return common_constants.conditional

        case BinaryConnective.BICONDITIONAL:
            return common_constants.biconditional


def quantifier_to_logical_constant(quant: Quantifier) -> LogicalConstantSymbol:
    match quant:
        case Quantifier.UNIVERSAL:
            return common_constants.forall

        case Quantifier.EXISTENTIAL:
            return common_constants.exists


@dataclass
class FormulaTranslationVisitor(FormulaVisitor):
    fol_signature: FormalLogicSignature
    hol_signature: HolSignature
    term_visitor: TermTranslationVisitor = field(init=False)

    def __post_init__(self) -> None:
        self.term_visitor = TermTranslationVisitor(self.fol_signature, self.hol_signature)

    @override
    def visit_prop_constant(self, formula: PropConstant) -> Constant:
        match formula.value:
            case PropConstantSymbol.VERUM:
                return Constant(common_constants.verum)

            case PropConstantSymbol.FALSUM:
                return Constant(common_constants.falsum)

    @override
    def visit_predicate(self, formula: PredicateApplication) -> TypedTerm:
        result: TypedTerm = Constant(self.hol_signature.get_nonlogical_constant_symbol(formula.symbol.name))

        for arg in formula.arguments:
            result = TypedApplication(result, self.term_visitor.visit(arg))

        return result

    @override
    def visit_negation(self, formula: NegationFormula) -> TypedApplication:
        return TypedApplication(
            Constant(common_constants.negation),
            self.visit(formula.body),
        )

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> TypedApplication:
        return TypedApplication(
            TypedApplication(
                Constant(connective_to_logical_constant(formula.conn)),
                self.visit(formula.left),
            ),
            self.visit(formula.right),
        )

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> TypedApplication:
        return TypedApplication(
            Constant(quantifier_to_logical_constant(formula.quant)),
            TypedAbstraction(
                self.term_visitor.visit(formula.var),
                BaseType(common_types.individual),
                self.visit(formula.body),
            ),
        )


# alg:fol_formula_to_hol_expression
def fol_formula_to_hol_expression(fol_signature: FormalLogicSignature, fol_formula: Formula) -> HolExpression:
    hol_signature = fol_signature_to_hol_signature(fol_signature)
    hol_term = FormulaTranslationVisitor(fol_signature, hol_signature).visit(fol_formula)
    context = [VariableTypeAssertion(var, BaseType(common_types.individual)) for var in get_free_variables(hol_term)]
    return HolExpression(hol_term, BaseType(common_types.individual), context)
