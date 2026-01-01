from dataclasses import dataclass
from typing import override

from .formula_visitor import PropFormulaTransformationVisitor
from .formulas import PropFormula


@dataclass(frozen=True)
class FormulaSubstitutionVisitor(PropFormulaTransformationVisitor):
    src: PropFormula
    dest: PropFormula

    @override
    def visit(self, formula: PropFormula) -> PropFormula:
        if formula == self.src:
            return self.dest

        return super().visit(formula)


# This is alg:propositional_subformula_substitution in the monograph
def substitute_subformula(formula: PropFormula, src: PropFormula, dest: PropFormula) -> PropFormula:
    return FormulaSubstitutionVisitor(src, dest).visit(formula)
