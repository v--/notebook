from .....parsing import LatinIdentifier
from ...alphabet import BinaryConnective, PropConstantSymbol, Quantifier
from ...common import variables as var
from ...formulas import ConnectiveFormula, EqualityFormula, Formula, NegationFormula, PropConstant, QuantifierFormula
from ...terms import Variable
from ...transformation import dualize_formula, universal_closure


VAR_LETTER = 'x'


# ex:cardinality_control_formulas
def cardinality_formula_geq(n: int) -> Formula:
    body: Formula | None = None

    for i in range(1, n):
        addendum = NegationFormula(
            EqualityFormula(
                Variable(LatinIdentifier(VAR_LETTER, i)),
                var.y
            )
        )

        if body is None:
            body = addendum
        else:
            body = ConnectiveFormula(BinaryConnective.CONJUNCTION, body, addendum)

    if body is None:
        return PropConstant(PropConstantSymbol.VERUM)

    return universal_closure(
        QuantifierFormula(Quantifier.EXISTENTIAL, var.y, body)
    )


def cardinality_formula_less(n: int) -> Formula:
    return dualize_formula(cardinality_formula_geq(n))


def cardinality_formula_equal(n: int) -> Formula:
    if n == 1:
        return cardinality_formula_less(2)

    return ConnectiveFormula(
        BinaryConnective.CONJUNCTION,
        cardinality_formula_geq(n),
        dualize_formula(cardinality_formula_geq(n + 1))
    )
