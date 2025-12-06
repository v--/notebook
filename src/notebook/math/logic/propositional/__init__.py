"""We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
This deviates from the monograph, but implementing support for propositional variables will be of no use for us."""

from .formula_visitor import PropositionalFormulaTransformationVisitor, PropositionalFormulaVisitor
from .formulas import PropositionalVariable, PropositionalVariableFormula, extract_variable
from .interpretation import PropositionalInterpretation
from .parsing import parse_propositional_formula, parse_propositional_variable
from .sat import are_equisatisfiable, are_semantically_equivalent, brute_force_satisfy, is_contradiction, is_tautology
from .signature import DEFAULT_PROPOSITIONAL_VARIABLE, PROPOSITIONAL_SIGNATURE, PropositionalLogicSignature
from .variables import get_propositional_variables
