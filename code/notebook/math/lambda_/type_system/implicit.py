from collections.abc import Mapping

from ..parsing import parse_typing_rule
from ..signature import EMPTY_SIGNATURE
from ..typing import ImplicitTypingRule, TypingStyle
from .gradual import GradualTypeSystem


class ImplicitTypeSystem(GradualTypeSystem[ImplicitTypingRule]):
    rules: Mapping[str, ImplicitTypingRule]


BASE_IMPLICIT_TYPE_SYSTEM = ImplicitTypeSystem({
    '→₊': parse_typing_rule(EMPTY_SIGNATURE, '[x: τ] M: σ ⫢ (λx.M): (τ → σ)', TypingStyle.IMPLICIT),
    '→₋': parse_typing_rule(EMPTY_SIGNATURE, 'M: (τ → σ), N: τ ⫢ (MN): σ', TypingStyle.IMPLICIT)
})

