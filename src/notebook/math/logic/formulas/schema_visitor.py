from ..alphabet import BinaryConnective, PropConstantSymbol, Quantifier
from .schemas import (
    AtomicFormulaSchema,
    ConnectiveFormulaSchema,
    EqualityFormulaSchema,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormulaSchema,
    PredicateApplicationSchema,
    PropConstant,
    QuantifierFormulaSchema,
)


class FormulaSchemaVisitor[T]:
    def visit(self, schema: FormulaSchema) -> T:  # noqa: PLR0911,C901
        match schema:
            case PropConstant():
                match schema.value:
                    case PropConstantSymbol.VERUM:
                        return self.visit_verum(schema)

                    case PropConstantSymbol.FALSUM:
                        return self.visit_falsum(schema)

            case EqualityFormulaSchema():
                return self.visit_equality(schema)

            case PredicateApplicationSchema():
                return self.visit_predicate(schema)

            case FormulaPlaceholder():
                return self.visit_formula_placeholder(schema)

            case NegationFormulaSchema():
                return self.visit_negation(schema)

            case ConnectiveFormulaSchema():
                match schema.conn:
                    case BinaryConnective.CONJUNCTION:
                        return self.visit_conjunction(schema)

                    case BinaryConnective.DISJUNCTION:
                        return self.visit_disjunction(schema)

                    case BinaryConnective.CONDITIONAL:
                        return self.visit_conditional(schema)

                    case BinaryConnective.BICONDITIONAL:
                        return self.visit_biconditional(schema)

            case QuantifierFormulaSchema():
                match schema.quant:
                    case Quantifier.UNIVERSAL:
                        return self.visit_universal(schema)

                    case Quantifier.EXISTENTIAL:
                        return self.visit_existential(schema)

    def visit_atomic(self, schema: AtomicFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_prop_constant(self, schema: PropConstant) -> T:
        return self.visit_atomic(schema)

    def visit_verum(self, schema: PropConstant) -> T:
        return self.visit_prop_constant(schema)

    def visit_falsum(self, schema: PropConstant) -> T:
        return self.visit_prop_constant(schema)

    def visit_equality(self, schema: EqualityFormulaSchema) -> T:
        return self.visit_atomic(schema)

    def visit_predicate(self, schema: PredicateApplicationSchema) -> T:
        return self.visit_atomic(schema)

    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_negation(self, schema: NegationFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_connective(self, schema: ConnectiveFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_conjunction(self, schema: ConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def visit_disjunction(self, schema: ConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def visit_conditional(self, schema: ConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def visit_biconditional(self, schema: ConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_universal(self, schema: QuantifierFormulaSchema) -> T:
        return self.visit_quantifier(schema)

    def visit_existential(self, schema: QuantifierFormulaSchema) -> T:
        return self.visit_quantifier(schema)

    def generic_visit(self, schema: FormulaSchema) -> T:
        raise NotImplementedError

