from ..signature import LambdaSignature
from .base import ABS_RULE_EXPLICIT, APP_RULE_EXPLICIT
from .systems import ExplicitTypingSystem


HOL_SIGNATURE = LambdaSignature(base_types={'o', 'ι'}, constant_terms={'Q', 'I'})
HOL = ExplicitTypingSystem(
    rules=[
        APP_RULE_EXPLICIT,
        ABS_RULE_EXPLICIT
    ]
)
