from ..alphabet import BinaryConnective, PropConstantSymbol
from ..formulas import PropConstant
from .schemas import (
    PropConnectiveFormulaSchema,
    PropFormulaSchema,
    PropNegationFormulaSchema,
    PropPlaceholder,
)


class PropFormulaSchemaVisitor[T]:
    def visit(self, schema: PropFormulaSchema) -> T:
        match schema:
            case PropConstant():
                match schema.value:
                    case PropConstantSymbol.VERUM:
                        return self.visit_verum(schema)

                    case PropConstantSymbol.FALSUM:
                        return self.visit_falsum(schema)

            case PropPlaceholder():
                return self.visit_formula_placeholder(schema)

            case PropNegationFormulaSchema():
                return self.visit_negation(schema)

            case PropConnectiveFormulaSchema():
                match schema.conn:
                    case BinaryConnective.CONJUNCTION:
                        return self.visit_conjunction(schema)

                    case BinaryConnective.DISJUNCTION:
                        return self.visit_disjunction(schema)

                    case BinaryConnective.CONDITIONAL:
                        return self.visit_conditional(schema)

                    case BinaryConnective.BICONDITIONAL:
                        return self.visit_biconditional(schema)

    def visit_prop_constant(self, schema: PropConstant) -> T:
        return self.generic_visit(schema)

    def visit_verum(self, schema: PropConstant) -> T:
        return self.visit_prop_constant(schema)

    def visit_falsum(self, schema: PropConstant) -> T:
        return self.visit_prop_constant(schema)

    def visit_formula_placeholder(self, schema: PropPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_negation(self, schema: PropNegationFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_connective(self, schema: PropConnectiveFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_conjunction(self, schema: PropConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def visit_disjunction(self, schema: PropConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def visit_conditional(self, schema: PropConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def visit_biconditional(self, schema: PropConnectiveFormulaSchema) -> T:
        return self.visit_connective(schema)

    def generic_visit(self, schema: PropFormulaSchema) -> T:
        raise NotImplementedError
