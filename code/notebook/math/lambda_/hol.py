from .parsing import parse_typing_rule
from .signature import LambdaSignature
from .typing_rules import TypingSystem


ANDREWS_HOL_SIGNATURE = LambdaSignature(base_types={'o', 'ι'}, constant_terms={'Q', 'I'})
ANDREWS_HOL = TypingSystem(
    rules=[
        parse_typing_rule(ANDREWS_HOL_SIGNATURE, '(App) M: (α → β), N: α ⫢ (MN): β'),
        parse_typing_rule(ANDREWS_HOL_SIGNATURE, '(Abs) [x: α] M: β ⫢ (λx.M): (α → β)')
    ]
)
