from typing import Generic, TypeVar

from .placeholders import (
    AtomicFormulaPlaceholder,
    ConnectiveFormulaPlaceholder,
    ConstantFormulaPlaceholder,
    FormulaPlaceholder,
    NegationFormulaPlaceholder,
    QuantifierFormulaPlaceholder,
)


T = TypeVar('T')


class FormulaPlaceholderVisitor(Generic[T]):
    def visit(self, placeholder: FormulaPlaceholder) -> T:
        match placeholder:
            case ConstantFormulaPlaceholder():
                return self.visit_constant(placeholder)

            case AtomicFormulaPlaceholder():
                return self.visit_atomic(placeholder)

            case NegationFormulaPlaceholder():
                return self.visit_negation(placeholder)

            case ConnectiveFormulaPlaceholder():
                return self.visit_connective(placeholder)

            case QuantifierFormulaPlaceholder():
                return self.visit_quantifier(placeholder)

    def visit_constant(self, placeholder: ConstantFormulaPlaceholder) -> T:
        return self.generic_visit(placeholder)

    def visit_atomic(self, placeholder: AtomicFormulaPlaceholder) -> T:
        return self.generic_visit(placeholder)

    def visit_negation(self, placeholder: NegationFormulaPlaceholder) -> T:
        return self.generic_visit(placeholder)

    def visit_connective(self, placeholder: ConnectiveFormulaPlaceholder) -> T:
        return self.generic_visit(placeholder)

    def visit_quantifier(self, placeholder: QuantifierFormulaPlaceholder) -> T:
        return self.generic_visit(placeholder)

    def generic_visit(self, placeholder: FormulaPlaceholder) -> T:
        raise NotImplementedError


class FormulaPlaceholderTransformationVisitor(FormulaPlaceholderVisitor[FormulaPlaceholder]):
    def visit_constant(self, placeholder: ConstantFormulaPlaceholder) -> FormulaPlaceholder:
        return placeholder

    def visit_atomic(self, placeholder: AtomicFormulaPlaceholder) -> FormulaPlaceholder:
        return placeholder

    def visit_negation(self, placeholder: NegationFormulaPlaceholder) -> FormulaPlaceholder:
        return NegationFormulaPlaceholder(self.visit(placeholder.sub))

    def visit_connective(self, placeholder: ConnectiveFormulaPlaceholder) -> FormulaPlaceholder:
        return ConnectiveFormulaPlaceholder(
            placeholder.conn,
            self.visit(placeholder.a),
            self.visit(placeholder.b)
        )

    def visit_quantifier(self, placeholder: QuantifierFormulaPlaceholder) -> FormulaPlaceholder:
        return QuantifierFormulaPlaceholder(
            placeholder.quantifier,
            placeholder.variable,
            self.visit(placeholder.sub)
        )
