from notebook.math.lambda_.hol import common
from notebook.math.lambda_.hol.expression import HolExpression
from notebook.math.lambda_.parsing import parse_typed_term

from .signature import ARITHMETIC_SIGNATURE


PEANO_INDUCTION_AXIOM = HolExpression(
    parse_typed_term(
        '(L∀(λp:(ι → ο).((L→((L∧(p0))(L∀(λn:ι.((L→(pn))(p(S⁺n)))))))(L∀(λn:ι.(pn))))))',
        ARITHMETIC_SIGNATURE,
    ),
    common.prop,
)
