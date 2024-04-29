from dataclasses import dataclass
from typing import override

from ..fol.formulas import ConnectiveFormula, ConstantFormula, Formula, NegationFormula, QuantifierFormula
from .exceptions import NaturalDeductionError
from .placeholders import (
    AtomicFormulaPlaceholder,
    ConnectiveFormulaPlaceholder,
    ConstantFormulaPlaceholder,
    FormulaPlaceholder,
    NegationFormulaPlaceholder,
    QuantifierFormulaPlaceholder,
)
from .visitors import FormulaPlaceholderVisitor


class SubstitutionError(NaturalDeductionError):
    pass


@dataclass
class UniformSubstitutionApplicationVisitor(FormulaPlaceholderVisitor[Formula]):
    atomic_mapping: dict[AtomicFormulaPlaceholder, Formula]

    @override
    def visit_constant(self, placeholder: ConstantFormulaPlaceholder) -> ConstantFormula:
        return ConstantFormula(placeholder.value)

    @override
    def visit_atomic(self, placeholder: AtomicFormulaPlaceholder) -> Formula:
        if placeholder not in self.atomic_mapping:
            raise SubstitutionError(f'No specification how to substitute {placeholder}')

        return self.atomic_mapping[placeholder]

    @override
    def visit_negation(self, placeholder: NegationFormulaPlaceholder) -> NegationFormula:
        return NegationFormula(self.visit(placeholder.sub))

    @override
    def visit_connective(self, placeholder: ConnectiveFormulaPlaceholder) -> ConnectiveFormula:
        return ConnectiveFormula(
            placeholder.conn,
            self.visit(placeholder.a),
            self.visit(placeholder.b)
        )

    @override
    def visit_quantifier(self, placeholder: QuantifierFormulaPlaceholder) -> QuantifierFormula:
        return QuantifierFormula(
            placeholder.quantifier,
            placeholder.variable,
            self.visit(placeholder.sub)
        )


@dataclass
class UniformSubstitution:
    atomic_mapping: dict[AtomicFormulaPlaceholder, Formula]

    def apply_to(self, placeholder: FormulaPlaceholder) -> Formula:
        return UniformSubstitutionApplicationVisitor(self.atomic_mapping).visit(placeholder)

    def __and__(self, other: object) -> 'UniformSubstitution | None':
        if not isinstance(other, UniformSubstitution):
            return NotImplemented

        a = self.atomic_mapping
        b = other.atomic_mapping
        common_keys = set(set(a.keys()) & set(b.keys()))

        if all(a[pl] == b[pl] for pl in common_keys):
            return UniformSubstitution({**a, **b})

        return None


EMPTY_SUBSTITUTION = UniformSubstitution({})


@dataclass
class BuildUniformSubstitutionVisitor(FormulaPlaceholderVisitor[UniformSubstitution | None]):
    formula: Formula

    @override
    def visit_constant(self, placeholder: ConstantFormulaPlaceholder) -> UniformSubstitution | None:
        if isinstance(self.formula, ConstantFormula) and self.formula.value == placeholder.value:
            return UniformSubstitution({})

        return None

    @override
    def visit_atomic(self, placeholder: AtomicFormulaPlaceholder) -> UniformSubstitution:
        return UniformSubstitution({placeholder: self.formula})

    @override
    def visit_negation(self, placeholder: NegationFormulaPlaceholder) -> UniformSubstitution | None:
        if isinstance(self.formula, NegationFormula):
            return BuildUniformSubstitutionVisitor(self.formula.sub).visit(placeholder.sub)

        return None

    @override
    def visit_connective(self, placeholder: ConnectiveFormulaPlaceholder) -> UniformSubstitution | None:
        if isinstance(self.formula, ConnectiveFormula) and self.formula.conn == placeholder.conn:
            a = BuildUniformSubstitutionVisitor(self.formula.a).visit(placeholder.a)
            b = BuildUniformSubstitutionVisitor(self.formula.b).visit(placeholder.b)

            if a is None or b is None:
                return None

            return a & b

        return None

    @override
    def visit_quantifier(self, placeholder: QuantifierFormulaPlaceholder) -> UniformSubstitution | None:
        if isinstance(self.formula, QuantifierFormula) and self.formula.quantifier == placeholder.quantifier:
            return BuildUniformSubstitutionVisitor(self.formula.sub).visit(placeholder.sub)

        return None


def build_substitution(placeholder: FormulaPlaceholder, formula: Formula) -> UniformSubstitution | None:
    return BuildUniformSubstitutionVisitor(formula).visit(placeholder)


def is_schema_instance(placeholder: FormulaPlaceholder, formula: Formula) -> bool:
    return build_substitution(placeholder, formula) is not None
