from ..parsing import parse_formula, parse_formula_schema
from .exceptions import PropositionalLogicError
from .formula_conversion import convert_to_prop_formula
from .formulas import PropFormula, PropVariable
from .schema_conversion import convert_to_prop_schema
from .schemas import PropFormulaSchema
from .signature import DEFAULT_PROP_SIGNATURE


def parse_prop_formula(source: str) -> PropFormula:
    return convert_to_prop_formula(parse_formula(source, DEFAULT_PROP_SIGNATURE))


def parse_prop_variable(source: str) -> PropVariable:
    formula = parse_prop_formula(source)

    if not isinstance(formula, PropVariable):
        raise PropositionalLogicError(f'Encountered a propositional variable, but got {source}')

    return formula


def parse_prop_schema(source: str) -> PropFormulaSchema:
    return convert_to_prop_schema(parse_formula_schema(source, DEFAULT_PROP_SIGNATURE))
