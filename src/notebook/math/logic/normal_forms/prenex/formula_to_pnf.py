from ...formulas import Formula
from ...transformation import pull_quantifiers


# This is alg:fol_formula_to_prenex_normal_form in the monograph
def formula_to_pnf(formula: Formula) -> Formula:
    return pull_quantifiers(formula)
