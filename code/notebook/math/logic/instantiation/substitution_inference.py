from ..formulas import FormulaSchemaSubstitutionSpec, FormulaSubstitutionSpec
from ..terms import EigenvariableSchemaSubstitutionSpec, TermSchemaSubstitutionSpec, TermSubstitutionSpec
from .base import FormalLogicSchemaInstantiation, merge_instantiations
from .exceptions import InsufficientInferenceDataError
from .formula_inference import infer_instantiation_from_formula
from .term_inference import infer_instantiation_from_term


def infer_instantiation_from_formula_substitution_spec(
    schema_spec: FormulaSchemaSubstitutionSpec,
    spec: FormulaSubstitutionSpec,
) -> FormalLogicSchemaInstantiation:
    instantiation = infer_instantiation_from_formula(schema_spec.formula, spec.formula)

    match (schema_spec.sub, spec.sub):
        case (None, None):
            return instantiation

        case (None, _):
            raise InsufficientInferenceDataError('Cannot infer substitution schema without the schema substitution')

        case (_, None):
            raise InsufficientInferenceDataError('Cannot infer substitution schema without the formula substitution')

        case _:
            assert schema_spec.sub is not None
            assert spec.sub is not None

            instantiation = merge_instantiations(
                instantiation,
                infer_instantiation_from_term(schema_spec.sub.dest, spec.sub.dest)
            )

            variable_mapping = dict(instantiation.variable_mapping)
            variable_mapping[schema_spec.sub.src] = spec.sub.src

            return FormalLogicSchemaInstantiation(
                variable_mapping=variable_mapping,
                term_mapping=instantiation.term_mapping,
                formula_mapping=instantiation.formula_mapping
            )


def infer_instantiation_from_term_substitution_spec(
    schema_spec: EigenvariableSchemaSubstitutionSpec | TermSchemaSubstitutionSpec,
    spec: TermSubstitutionSpec
) -> FormalLogicSchemaInstantiation:
    return merge_instantiations(
        infer_instantiation_from_term(schema_spec.src, spec.src),
        infer_instantiation_from_term(schema_spec.dest, spec.dest)
    )
