"""We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
This deviates from the monograph, but implementing support for propositional variables will be of no use for us."""

from .evaluation import evaluate_prop_formula
from .exceptions import (
    MissingInterpretationError,
    NonPropositionalFormulaError,
    PropositionalLogicError,
)
from .formula_conversion import convert_to_prop_formula
from .formula_to_function import prop_formula_to_function
from .formula_visitor import PropFormulaTransformationVisitor, PropFormulaVisitor
from .formulas import PropConnectiveFormula, PropFormula, PropNegationFormula, PropVariable
from .interpretation import PropInterpretation
from .parsing import parse_prop_formula, parse_prop_variable
from .sat import (
    are_equisatisfiable,
    are_semantically_equivalent,
    brute_force_satisfy,
    is_contradiction,
    is_tautology,
    iter_interpretations,
    iter_interpretations_for_variables,
)
from .schema_conversion import convert_to_prop_schema
from .schemas import PropConnectiveFormulaSchema, PropFormulaSchema, PropNegationFormulaSchema, PropPlaceholder
from .signature import DEFAULT_PROP_SIGNATURE, DEFAULT_PROP_VARIABLE, PropLogicSignature
from .substitute_subformula import substitute_subformula
from .symbols import PropVariableSymbol
from .translation import (
    PropFormulaTranslation,
    UnspecifiedReplacementError,
    apply_prop_formula_translation,
    translate_prop_formula,
)
from .variables import get_prop_variables
