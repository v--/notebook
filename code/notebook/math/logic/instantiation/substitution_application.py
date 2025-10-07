from ..formulas import Formula, FormulaSchemaSubstitutionSpec
from ..substitution import substitute_in_formula
from .base import FormalLogicSchemaInstantiation
from .formula_application import instantiate_formula_schema
from .term_application import instantiate_term_schema


def instantiate_substitution_spec(schema: FormulaSchemaSubstitutionSpec, instantiation: FormalLogicSchemaInstantiation) -> Formula:
    formula = instantiate_formula_schema(schema.formula, instantiation)

    if schema.sub:
        src = instantiate_term_schema(schema.sub.src, instantiation)
        dest = instantiate_term_schema(schema.sub.dest, instantiation)
        return substitute_in_formula(formula, src, dest)

    return formula
