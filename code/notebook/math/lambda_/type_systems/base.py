from ..parsing import parse_pure_typing_rule
from ..typing_rules import TypingSystem


BASE_SYSTEM = TypingSystem(
    rules=[
        parse_pure_typing_rule('(App) M: (α → β), N: α ⫢ (MN): β'),
        parse_pure_typing_rule('(Abs) [x: α] M: β ⫢ (λx.M): (α → β)')
    ]
)
