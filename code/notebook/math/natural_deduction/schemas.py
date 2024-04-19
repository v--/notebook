from dataclasses import dataclass
from typing import override

from ..fol.formulas import ConnectiveFormula, ConstantFormula, Formula, NegationFormula, QuantifierFormula
from .rules import (
    AtomicFormulaPlaceholder,
    ConnectiveFormulaPlaceholder,
    ConstantFormulaPlaceholder,
    FormulaPlaceholder,
    NegationFormulaPlaceholder,
    QuantifierFormulaPlaceholder,
)
from .visitors import FormulaPlaceholderVisitor


FormulaSubstitution = dict[AtomicFormulaPlaceholder, Formula]


@dataclass
class BuildSubstitutionVisitor(FormulaPlaceholderVisitor[FormulaSubstitution | None]):
    formula: Formula

    @override
    def visit_constant(self, placeholder: ConstantFormulaPlaceholder) -> FormulaSubstitution | None:
        if isinstance(self.formula, ConstantFormula) and self.formula.value == placeholder.value:
            return {}

        return None

    @override
    def visit_atomic(self, placeholder: AtomicFormulaPlaceholder) -> FormulaSubstitution:
        return {placeholder: self.formula}

    @override
    def visit_negation(self, placeholder: NegationFormulaPlaceholder) -> FormulaSubstitution | None:
        if isinstance(self.formula, NegationFormula):
            return BuildSubstitutionVisitor(self.formula.sub).visit(placeholder.sub)

        return None

    @override
    def visit_connective(self, placeholder: ConnectiveFormulaPlaceholder) -> FormulaSubstitution | None:
        if isinstance(self.formula, ConnectiveFormula) and self.formula.conn == placeholder.conn:
            a = BuildSubstitutionVisitor(self.formula.a).visit(placeholder.a)
            b = BuildSubstitutionVisitor(self.formula.b).visit(placeholder.b)

            if a is None or b is None:
                return None

            common_placeholders = set(set(a.keys()) & set(b.keys()))

            if all(a[pl] == b[pl] for pl in common_placeholders):
                return {**a, **b}

        return None

    @override
    def visit_quantifier(self, placeholder: QuantifierFormulaPlaceholder) -> FormulaSubstitution | None:
        if isinstance(self.formula, QuantifierFormula) and self.formula.quantifier == placeholder.quantifier:
            return BuildSubstitutionVisitor(self.formula.sub).visit(placeholder.sub)

        return None


def is_schema_instance(placeholder: FormulaPlaceholder, formula: Formula) -> bool:
    return BuildSubstitutionVisitor(formula).visit(placeholder) is not None
