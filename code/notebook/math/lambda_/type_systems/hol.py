from ..signature import LambdaSignature
from ..typing_rules import GradualTypingSystem
from .base import BASE_SYSTEM


HOL_SIGNATURE = LambdaSignature(base_types={'o', 'ι'}, constant_terms={'Q', 'I'})
HOL = GradualTypingSystem(
    rules=[
        BASE_SYSTEM['App'],
        BASE_SYSTEM['Abs']
    ]
)
