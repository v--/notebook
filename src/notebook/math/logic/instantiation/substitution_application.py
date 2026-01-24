from ..formulas import (
    FormulaSchemaWithSubstitution,
    FormulaWithSubstitution,
)
from ..terms import TermSubstitutionSpec
from .base import AtomicLogicSchemaInstantiation
from .formula_application import instantiate_formula_schema
from .term_application import instantiate_term_schema


def instantiate_substitution(schema: FormulaSchemaWithSubstitution, instantiation: AtomicLogicSchemaInstantiation) -> FormulaWithSubstitution:
    formula = instantiate_formula_schema(schema.formula, instantiation)

    if not schema.sub:
        return FormulaWithSubstitution(formula)

    src = instantiate_term_schema(schema.sub.src, instantiation)
    dest_ = instantiate_term_schema(schema.sub.dest, instantiation)
    return FormulaWithSubstitution(
        formula,
        TermSubstitutionSpec(src, dest_)
    )
