from .formula_visitor import (
    apply_substitution_to_formula,
    evaluate_substitution_spec,
    substitute_in_formula,
    unwrap_substitution_spec,
)
from .substitution import AtomicLogicSubstitution, infer_substitution
from .term_visitor import apply_substitution_to_term, substitute_in_term
