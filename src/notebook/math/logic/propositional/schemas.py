from ..formulas import ConnectiveFormulaSchema, FormulaPlaceholder, NegationFormulaSchema, PropConstant


class PropPlaceholder(FormulaPlaceholder):
    def __repr__(self) -> str:
        return f"parse_prop_formula_schema('{self}')"


class PropNegationFormulaSchema(NegationFormulaSchema):
    body: PropFormulaSchema

    def __repr__(self) -> str:
        return f"parse_prop_formula_schema('{self}')"


class PropConnectiveFormulaSchema(ConnectiveFormulaSchema):
    left: PropFormulaSchema
    right: PropFormulaSchema

    def __repr__(self) -> str:
        return f"parse_prop_formula_schema('{self}')"


PropFormulaSchema = PropConstant | PropPlaceholder | PropNegationFormulaSchema | PropConnectiveFormulaSchema
