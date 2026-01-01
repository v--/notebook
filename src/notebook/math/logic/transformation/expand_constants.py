from dataclasses import dataclass

from ..alphabet import BinaryConnective, PropConstantSymbol
from ..formulas import (
    ConnectiveFormula,
    Formula,
    FormulaTransformationVisitor,
    NegationFormula,
    PropConstant,
)
from ..propositional import (
    DEFAULT_PROP_VARIABLE,
    PropFormula,
    convert_to_prop_formula,
    get_prop_variables,
)


@dataclass(frozen=True)
class ExpandConstantsVisitor(FormulaTransformationVisitor):
    default_formula: Formula

    def visit_prop_constant(self, formula: PropConstant) -> ConnectiveFormula:
        default = self.default_formula

        match formula.value:
            case PropConstantSymbol.VERUM:
                return ConnectiveFormula(BinaryConnective.CONDITIONAL, default, default)

            case PropConstantSymbol.FALSUM:
                return ConnectiveFormula(BinaryConnective.CONJUNCTION, default, NegationFormula(default))


def expand_constants(formula: Formula, default: Formula) -> Formula:
    return ExpandConstantsVisitor(default).visit(formula)


# This is alg:propositional_constant_expansion in the monograph
def expand_constants_prop(formula: PropFormula) -> PropFormula:
    variables = get_prop_variables(formula)

    if len(variables) > 0:
        p = min(variables)
    else:
        p = DEFAULT_PROP_VARIABLE

    return convert_to_prop_formula(expand_constants(formula, default=p))
