from ..parsing import parse_typing_rule
from ..signature import EMPTY_SIGNATURE
from ..typing import TypingStyle


# These rules are distinct
ARROW_INT_RULE_IMPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁺) [x: α] M: β ⫢ (λx.M): (α → β)', TypingStyle.implicit)
ARROW_INT_RULE_EXPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁺) [x: α] M: β ⫢ (λx:α.M): (α → β)', TypingStyle.explicit)

# These rules are identical, but belong to different classes
ARROW_ELIM_RULE_IMPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁻) M: (α → β), N: α ⫢ (MN): β', TypingStyle.implicit)
ARROW_ELIM_RULE_EXPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁻) M: (α → β), N: α ⫢ (MN): β', TypingStyle.explicit)
