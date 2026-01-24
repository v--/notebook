from dataclasses import dataclass
from typing import override

from ..formulas import (
    ConnectiveFormulaSchema,
    FormulaSchema,
    FormulaSchemaVisitor,
    NegationFormulaSchema,
    QuantifierFormulaSchema,
)


@dataclass(frozen=True)
class IsSubschemaVisitor(FormulaSchemaVisitor[bool]):
    subschema: FormulaSchema

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> bool:
        return schema == self.subschema or self.visit(schema.body)

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> bool:
        return schema == self.subschema or self.visit(schema.left) or self.visit(schema.right)

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> bool:
        return schema == self.subschema or self.visit(schema.body)

    @override
    def generic_visit(self, schema: FormulaSchema) -> bool:
        return schema == self.subschema


def is_subschema(schema: FormulaSchema, subschema: FormulaSchema) -> bool:
    return IsSubschemaVisitor(subschema).visit(schema)
