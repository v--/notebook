from ....support.schemas import SchemaInferenceError
from ..formulas import FormulaSchemaWithSubstitution, FormulaWithSubstitution
from ..terms import TermSchemaSubstitutionSpec, TermSubstitutionSpec
from .base import AtomicLogicSchemaInstantiation
from .formula_inference import infer_instantiation_from_formula
from .term_inference import infer_instantiation_from_term


def infer_instantiation_from_term_substitution_spec(
    schema_spec: TermSchemaSubstitutionSpec,
    spec: TermSubstitutionSpec
) -> AtomicLogicSchemaInstantiation:
    return infer_instantiation_from_term(schema_spec.src, spec.src) | \
        infer_instantiation_from_term(schema_spec.dest, spec.dest)


def infer_instantiation_from_formula_substitution_spec(
    schema_spec: FormulaSchemaWithSubstitution,
    spec: FormulaWithSubstitution,
) -> AtomicLogicSchemaInstantiation:
    instantiation = infer_instantiation_from_formula(schema_spec.formula, spec.formula)
    schema_sub = schema_spec.sub
    formula_sub = spec.sub

    if formula_sub and schema_sub:
        return instantiation | infer_instantiation_from_term_substitution_spec(schema_sub, formula_sub)

    if formula_sub and schema_sub is None:
        raise SchemaInferenceError('Cannot infer a substitution schema instantiation without the schema substitution')

    return instantiation
