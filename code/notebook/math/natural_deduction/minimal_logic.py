from .parsing.parser import parse_rule
from .system import NaturalDeductionSystem


minimal_nd_system = NaturalDeductionSystem(
    frozenset([
        parse_rule('(→⁺) [φ] φ, ψ ⫢ (φ → ψ)')
    ])
)
