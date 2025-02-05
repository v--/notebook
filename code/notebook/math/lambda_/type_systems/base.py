from ..parsing import parse_typing_rule
from ..signature import EMPTY_SIGNATURE
from ..typing import TypingStyle


# These rules are distinct
ARROW_INTRO_RULE_IMPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁺) [x: τ] M: σ ⫢ (λx.M): (τ → σ)', TypingStyle.implicit)
ARROW_INTRO_RULE_EXPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁺) [x: τ] M: σ ⫢ (λx:τ.M): (τ → σ)', TypingStyle.explicit)

# These rules are identical, but belong to different classes
ARROW_ELIM_RULE_IMPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁻) M: (τ → σ), N: τ ⫢ (MN): σ', TypingStyle.implicit)
ARROW_ELIM_RULE_EXPLICIT = parse_typing_rule(EMPTY_SIGNATURE, '(→⁻) M: (τ → σ), N: τ ⫢ (MN): σ', TypingStyle.explicit)
