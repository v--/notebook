from ..signature import LambdaSignature
from .base import ARROW_ELIM_RULE_EXPLICIT, ARROW_INTRO_RULE_EXPLICIT
from .systems import ExplicitTypingSystem


HOL_SIGNATURE = LambdaSignature(base_types={'o', 'ι'}, constant_terms={'Q', 'I'})
HOL = ExplicitTypingSystem(
    rules=[
        ARROW_ELIM_RULE_EXPLICIT,
        ARROW_INTRO_RULE_EXPLICIT
    ]
)
