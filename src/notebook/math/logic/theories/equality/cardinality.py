from notebook.math.logic.alphabet import BinaryConnective, PropConstantSymbol, Quantifier
from notebook.math.logic.common import variables as var
from notebook.math.logic.formulas import (
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PropConstant,
    QuantifierFormula,
)
from notebook.math.logic.terms import Variable
from notebook.math.logic.transformation import dualize_formula, universal_closure
from notebook.parsing import LatinIdentifier
from notebook.support.coderefs import collector


VAR_LETTER = 'x'


@collector.ref('ex:cardinality_control_formulas')
def cardinality_formula_geq(n: int) -> Formula:
    body: Formula | None = None

    for i in range(1, n):
        addendum = NegationFormula(
            EqualityFormula(
                Variable(LatinIdentifier(VAR_LETTER, i)),
                var.y,
            ),
        )

        body = addendum if body is None else ConnectiveFormula(BinaryConnective.CONJUNCTION, body, addendum)

    if body is None:
        return PropConstant(PropConstantSymbol.VERUM)

    return universal_closure(
        QuantifierFormula(Quantifier.EXISTENTIAL, var.y, body),
    )


def cardinality_formula_less(n: int) -> Formula:
    return dualize_formula(cardinality_formula_geq(n))


def cardinality_formula_equal(n: int) -> Formula:
    if n == 1:
        return cardinality_formula_less(2)

    return ConnectiveFormula(
        BinaryConnective.CONJUNCTION,
        cardinality_formula_geq(n),
        dualize_formula(cardinality_formula_geq(n + 1)),
    )
