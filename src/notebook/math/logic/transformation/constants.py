from dataclasses import dataclass

from ..alphabet import BinaryConnective, PropConstant
from ..formulas import (
    ConnectiveFormula,
    ConstantFormula,
    Formula,
    FormulaTransformationVisitor,
    NegationFormula,
    PredicateApplication,
    is_logical_constant,
)
from ..propositional import (
    DEFAULT_PROPOSITIONAL_VARIABLE,
    PropositionalFormulaTransformationVisitor,
    PropositionalVariable,
    get_propositional_variables,
)


@dataclass(frozen=True)
class ExpandConstantsVisitor(PropositionalFormulaTransformationVisitor):
    default_variable: PropositionalVariable

    def visit_logical_constant(self, formula: ConstantFormula) -> ConnectiveFormula:
        p_formula = PredicateApplication(self.default_variable, [])

        match formula.value:
            case PropConstant.VERUM:
                return ConnectiveFormula(BinaryConnective.CONDITIONAL, p_formula, p_formula)

            case PropConstant.FALSUM:
                return ConnectiveFormula(BinaryConnective.CONJUNCTION, p_formula, NegationFormula(p_formula))


# This is alg:propositional_constant_expansion in the monograph
def expand_constants(formula: Formula) -> Formula:
    variables = get_propositional_variables(formula)

    if len(variables) > 0:
        p = min(variables)
    else:
        p = DEFAULT_PROPOSITIONAL_VARIABLE

    return ExpandConstantsVisitor(p).visit(formula)


class CollapseConstantsVisitor(FormulaTransformationVisitor):
    def visit_negation(self, formula: NegationFormula) -> Formula:
        body = self.visit(formula.body)

        if is_logical_constant(body):
            match body.value:
                case PropConstant.VERUM:
                    return ConstantFormula(PropConstant.FALSUM)

                case PropConstant.FALSUM:
                    return ConstantFormula(PropConstant.VERUM)

        return NegationFormula(body)

    def visit_connective(self, formula: ConnectiveFormula) -> Formula:  # noqa: PLR0911, C901
        left = self.visit(formula.left)
        right = self.visit(formula.right)

        match formula.conn:
            case BinaryConnective.CONJUNCTION:
                if is_logical_constant(left):
                    match left.value:
                        case PropConstant.VERUM:
                            return right

                        case PropConstant.FALSUM:
                            return left

                if is_logical_constant(right):
                    match right.value:
                        case PropConstant.VERUM:
                            return left

                        case PropConstant.FALSUM:
                            return right

                return ConnectiveFormula(BinaryConnective.CONJUNCTION, left, right)

            case BinaryConnective.DISJUNCTION:
                if is_logical_constant(left):
                    match left.value:
                        case PropConstant.VERUM:
                            return left

                        case PropConstant.FALSUM:
                            return right

                if is_logical_constant(right):
                    match right.value:
                        case PropConstant.VERUM:
                            return right

                        case PropConstant.FALSUM:
                            return left

                return ConnectiveFormula(BinaryConnective.DISJUNCTION, left, right)

            case BinaryConnective.CONDITIONAL:
                if is_logical_constant(left):
                    match left.value:
                        case PropConstant.VERUM:
                            return right

                        case PropConstant.FALSUM:
                            return ConstantFormula(PropConstant.VERUM)

                if is_logical_constant(right):
                    match right.value:
                        case PropConstant.VERUM:
                            return ConstantFormula(PropConstant.VERUM)

                        case PropConstant.FALSUM:
                            return NegationFormula(left)

                return ConnectiveFormula(BinaryConnective.CONDITIONAL, left, right)

            case BinaryConnective.BICONDITIONAL:
                if is_logical_constant(left) and is_logical_constant(right):
                    if left == right:
                        return ConstantFormula(PropConstant.VERUM)

                    return ConstantFormula(PropConstant.FALSUM)

                return ConnectiveFormula(BinaryConnective.BICONDITIONAL, left, right)


# This is alg:propositional_constant_collapse in the monograph
def collapse_constants(formula: Formula) -> Formula:
    return CollapseConstantsVisitor().visit(formula)
