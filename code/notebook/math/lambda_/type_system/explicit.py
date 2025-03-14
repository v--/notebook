from collections.abc import Mapping

from ..parsing import parse_typing_rule
from ..signature import EMPTY_SIGNATURE
from ..typing import ExplicitTypingRule, TypingStyle
from .gradual import GradualTypeSystem


class ExplicitTypeSystem(GradualTypeSystem[ExplicitTypingRule]):
    rules: Mapping[str, ExplicitTypingRule]


BASE_EXPLICIT_TYPE_SYSTEM = ExplicitTypeSystem({
    '→⁺': parse_typing_rule(EMPTY_SIGNATURE, '[x: τ] M: σ ⫢ (λx:τ.M): (τ → σ)', TypingStyle.EXPLICIT),
    '→⁻': parse_typing_rule(EMPTY_SIGNATURE, 'M: (τ → σ), N: τ ⫢ (MN): σ', TypingStyle.EXPLICIT)
})

