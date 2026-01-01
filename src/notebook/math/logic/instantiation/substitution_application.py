from ..formulas import FormulaSchemaSubstitutionSpec, FormulaWithSubstitution
from ..terms import TermSubstitutionSpec
from .base import AtomicLogicSchemaInstantiation
from .formula_application import instantiate_formula_schema
from .term_application import instantiate_term_schema


def instantiate_substitution_spec(schema: FormulaSchemaSubstitutionSpec, instantiation: AtomicLogicSchemaInstantiation) -> FormulaWithSubstitution:
    formula = instantiate_formula_schema(schema.formula, instantiation)

    if schema.sub:
        src = instantiate_term_schema(schema.sub.src, instantiation)
        dest = instantiate_term_schema(schema.sub.dest, instantiation)
        return FormulaWithSubstitution(
            formula,
            TermSubstitutionSpec(src, dest)
        )

    return FormulaWithSubstitution(formula)
