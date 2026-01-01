from ...formulas import Formula
from ...transformation import pull_quantifiers


# This is alg:prenex_normal_form_conversion in the monograph
def formula_to_pnf(formula: Formula) -> Formula:
    return pull_quantifiers(formula)
