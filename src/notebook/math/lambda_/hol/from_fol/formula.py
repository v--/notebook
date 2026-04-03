from dataclasses import dataclass, field
from typing import TYPE_CHECKING, override

from .....support.coderefs import collector
from ....logic.alphabet import BinaryConnective, PropConstantSymbol, Quantifier
from ....logic.formulas import (
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    FormulaVisitor,
    NegationFormula,
    PredicateApplication,
    PropConstant,
    QuantifierFormula,
)
from ...terms import Constant, TypedAbstraction, TypedApplication, TypedTerm
from ...type_context import TypeContext
from ...variables import get_free_variables
from .. import common
from ..expression import HolExpression
from .signature import fol_signature_to_hol_signature
from .term import TermTranslationVisitor


if TYPE_CHECKING:
    from ....logic.signature.signature import FormalLogicSignature
    from ..signature import HolSignature


def connective_to_logical_constant(conn: BinaryConnective) -> Constant:
    match conn:
        case BinaryConnective.CONJUNCTION:
            return common.conjunction

        case BinaryConnective.DISJUNCTION:
            return common.disjunction

        case BinaryConnective.CONDITIONAL:
            return common.conditional

        case BinaryConnective.BICONDITIONAL:
            return common.biconditional


def quantifier_to_logical_constant(quant: Quantifier) -> Constant:
    match quant:
        case Quantifier.UNIVERSAL:
            return common.forall

        case Quantifier.EXISTENTIAL:
            return common.exists


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
                return common.verum

            case PropConstantSymbol.FALSUM:
                return common.falsum

    @override
    def visit_predicate(self, formula: PredicateApplication) -> TypedTerm:
        result: TypedTerm = Constant(self.hol_signature.get_nonlogical_constant_symbol(formula.symbol.name))

        for arg in formula.arguments:
            result = TypedApplication(result, self.term_visitor.visit(arg))

        return result

    @override
    def visit_equality(self, formula: EqualityFormula) -> TypedTerm:
        return TypedApplication(
            TypedApplication(
                common.equality,
                self.term_visitor.visit(formula.left),
            ),
            self.term_visitor.visit(formula.right),
        )

    @override
    def visit_negation(self, formula: NegationFormula) -> TypedApplication:
        return TypedApplication(
            common.negation,
            self.visit(formula.body),
        )

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> TypedApplication:
        return TypedApplication(
            TypedApplication(
                connective_to_logical_constant(formula.conn),
                self.visit(formula.left),
            ),
            self.visit(formula.right),
        )

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> TypedApplication:
        return TypedApplication(
            quantifier_to_logical_constant(formula.quant),
            TypedAbstraction(
                self.term_visitor.visit(formula.var),
                common.individual,
                self.visit(formula.body),
            ),
        )


@collector.ref('alg:fol_to_hol/formula')
def fol_formula_to_hol_expression(fol_signature: FormalLogicSignature, fol_formula: Formula) -> HolExpression:
    hol_signature = fol_signature_to_hol_signature(fol_signature)
    hol_term = FormulaTranslationVisitor(fol_signature, hol_signature).visit(fol_formula)
    context = TypeContext(dict.fromkeys(get_free_variables(hol_term), common.individual))
    return HolExpression(hol_term, common.individual, context)
