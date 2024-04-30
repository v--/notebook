from typing import Generic, TypeVar

from .schemas import (
    ConnectiveFormulaSchema,
    ConstantFormulaSchema,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormulaSchema,
    QuantifierFormulaSchema,
)


T = TypeVar('T')


class FormulaSchemaVisitor(Generic[T]):
    def visit(self, schema: FormulaSchema) -> T:
        match schema:
            case ConstantFormulaSchema():
                return self.visit_constant(schema)

            case FormulaPlaceholder():
                return self.visit_atomic(schema)

            case NegationFormulaSchema():
                return self.visit_negation(schema)

            case ConnectiveFormulaSchema():
                return self.visit_connective(schema)

            case QuantifierFormulaSchema():
                return self.visit_quantifier(schema)

    def visit_constant(self, schema: ConstantFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_atomic(self, schema: FormulaPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_negation(self, schema: NegationFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_connective(self, schema: ConnectiveFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: FormulaSchema) -> T:
        raise NotImplementedError


class FormulaSchemaTransformationVisitor(FormulaSchemaVisitor[FormulaSchema]):
    def visit_constant(self, schema: ConstantFormulaSchema) -> FormulaSchema:
        return schema

    def visit_atomic(self, schema: FormulaPlaceholder) -> FormulaSchema:
        return schema

    def visit_negation(self, schema: NegationFormulaSchema) -> FormulaSchema:
        return NegationFormulaSchema(self.visit(schema.sub))

    def visit_connective(self, schema: ConnectiveFormulaSchema) -> FormulaSchema:
        return ConnectiveFormulaSchema(
            schema.conn,
            self.visit(schema.a),
            self.visit(schema.b)
        )

    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> FormulaSchema:
        return QuantifierFormulaSchema(
            schema.quantifier,
            schema.variable,
            self.visit(schema.sub)
        )
