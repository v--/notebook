from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from ....support.coderefs import collector
from .formula_visitor import PropFormulaTransformationVisitor


if TYPE_CHECKING:
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


@collector.ref('alg:propositional_subformula_substitution')
def substitute_subformula(formula: PropFormula, src: PropFormula, dest: PropFormula) -> PropFormula:
    return FormulaSubstitutionVisitor(src, dest).visit(formula)
