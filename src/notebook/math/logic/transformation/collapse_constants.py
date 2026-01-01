from ..alphabet import BinaryConnective, PropConstantSymbol, get_dual_prop_constant
from ..formulas import (
    ConnectiveFormula,
    Formula,
    FormulaTransformationVisitor,
    NegationFormula,
    PropConstant,
    QuantifierFormula,
)
from ..propositional import PropFormula, convert_to_prop_formula


class CollapseConstantsVisitor(FormulaTransformationVisitor):
    def visit_negation(self, formula: NegationFormula) -> Formula:
        body = self.visit(formula.body)

        if isinstance(body, PropConstant):
            return PropConstant(get_dual_prop_constant(body.value))

        return NegationFormula(body)

    def visit_conjunction(self, formula: ConnectiveFormula) -> Formula:
        left = self.visit(formula.left)
        right = self.visit(formula.right)

        if isinstance(left, PropConstant):
            match left.value:
                case PropConstantSymbol.VERUM:
                    return right

                case PropConstantSymbol.FALSUM:
                    return left

        if isinstance(right, PropConstant):
            match right.value:
                case PropConstantSymbol.VERUM:
                    return left

                case PropConstantSymbol.FALSUM:
                    return right

        return ConnectiveFormula(BinaryConnective.CONJUNCTION, left, right)

    def visit_disjunction(self, formula: ConnectiveFormula) -> Formula:
        left = self.visit(formula.left)
        right = self.visit(formula.right)

        if isinstance(left, PropConstant):
            match left.value:
                case PropConstantSymbol.VERUM:
                    return left

                case PropConstantSymbol.FALSUM:
                    return right

        if isinstance(right, PropConstant):
            match right.value:
                case PropConstantSymbol.VERUM:
                    return right

                case PropConstantSymbol.FALSUM:
                    return left

        return ConnectiveFormula(BinaryConnective.DISJUNCTION, left, right)

    def visit_conditional(self, formula: ConnectiveFormula) -> Formula:
        left = self.visit(formula.left)
        right = self.visit(formula.right)

        if isinstance(left, PropConstant):
            match left.value:
                case PropConstantSymbol.VERUM:
                    return right

                case PropConstantSymbol.FALSUM:
                    return PropConstant(PropConstantSymbol.VERUM)

        if isinstance(right, PropConstant):
            match right.value:
                case PropConstantSymbol.VERUM:
                    return PropConstant(PropConstantSymbol.VERUM)

                case PropConstantSymbol.FALSUM:
                    return NegationFormula(left)

        return ConnectiveFormula(BinaryConnective.CONDITIONAL, left, right)

    def visit_biconditional(self, formula: ConnectiveFormula) -> Formula:
        left = self.visit(formula.left)
        right = self.visit(formula.right)

        if isinstance(left, PropConstant) and isinstance(right, PropConstant):
            if left == right:
                return PropConstant(PropConstantSymbol.VERUM)

            return PropConstant(PropConstantSymbol.FALSUM)

        return ConnectiveFormula(BinaryConnective.BICONDITIONAL, left, right)

    def visit_quantifier(self, formula: QuantifierFormula) -> Formula:
        body = self.visit(formula.body)

        if isinstance(body, QuantifierFormula):
            return body

        return QuantifierFormula(formula.quant, formula.var, body)


def collapse_constants(formula: Formula) -> Formula:
    return CollapseConstantsVisitor().visit(formula)


# This is alg:propositional_constant_collapse in the monograph
def collapse_constants_prop(formula: PropFormula) -> PropFormula:
    return convert_to_prop_formula(collapse_constants(formula))
