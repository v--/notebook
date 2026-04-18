from ....parsing import parse_typed_term
from ... import common
from ...expression import HolExpression
from .signature import ARITHMETIC_SIGNATURE


PEANO_INDUCTION_AXIOM = HolExpression(
    parse_typed_term(
        '(L∀(λp:(ι → ο).((L→((L∧(p0))(L∀(λn:ι.((L→(pn))(p(S⁺n)))))))(L∀(λn:ι.(pn))))))',
        ARITHMETIC_SIGNATURE,
    ),
    common.prop,
)
