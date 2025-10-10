from ..formulas import FormulaSchemaSubstitutionSpec, FormulaWithSubstitution
from ..terms import EigenvariableSchemaSubstitutionSpec, TermSchemaSubstitutionSpec, TermSubstitutionSpec
from .base import FormalLogicSchemaInstantiation
from .exceptions import InsufficientInferenceDataError
from .formula_inference import infer_instantiation_from_formula
from .term_inference import infer_instantiation_from_term


def infer_instantiation_from_term_substitution_spec(
    schema_spec: EigenvariableSchemaSubstitutionSpec | TermSchemaSubstitutionSpec,
    spec: TermSubstitutionSpec
) -> FormalLogicSchemaInstantiation:
    return infer_instantiation_from_term(schema_spec.src, spec.src) | \
        infer_instantiation_from_term(schema_spec.dest, spec.dest)


def infer_instantiation_from_formula_substitution_spec(
    schema_spec: FormulaSchemaSubstitutionSpec,
    spec: FormulaWithSubstitution,
) -> FormalLogicSchemaInstantiation:
    instantiation = infer_instantiation_from_formula(schema_spec.formula, spec.formula)
    schema_sub = schema_spec.sub
    formula_sub = spec.sub

    if formula_sub and schema_sub:
        return instantiation | infer_instantiation_from_term_substitution_spec(schema_sub, formula_sub)

    if formula_sub and schema_sub is None:
        raise InsufficientInferenceDataError('Cannot infer a substitution schema instantiation without the schema substitution')

    return instantiation
