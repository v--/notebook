from ..signature import LambdaSignature
from ..typing_rules import TypingSystem
from .base import BASE_SYSTEM


ANDREWS_HOL_SIGNATURE = LambdaSignature(base_types={'o', 'ι'}, constant_terms={'Q', 'I'})
ANDREWS_HOL = TypingSystem(
    rules=[
        BASE_SYSTEM['App'],
        BASE_SYSTEM['Abs']
    ]
)
