from ..parsing import parse_typing_rule
from ..signature import EMPTY_SIGNATURE
from ..typing import TypingStyle


APP_RULE_IMPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(App) M: (α → β), N: α ⫢ (MN): β', TypingStyle.implicit)
APP_RULE_EXPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(App) M: (α → β), N: α ⫢ (MN): β', TypingStyle.explicit)
ABS_RULE_IMPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(Abs) [x: α] M: β ⫢ (λx.M): (α → β)', TypingStyle.implicit)
ABS_RULE_EXPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(Abs) [x: α] M: β ⫢ (λx:α.M): (α → β)', TypingStyle.explicit)
