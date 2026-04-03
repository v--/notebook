from ..arrow_types import ARROW_ONLY_TYPE_SYSTEM
from ..assertions import TypeAssertionSchema
from ..parsing import parse_typing_rule
from ..terms import Constant
from ..type_system import ExplicitTypeSystem, TypingRule, TypingRuleEntry
from ..types import translate_type_to_schema
from .signature import PLAIN_HOL_SIGNATURE, HolSignature


BASE_HOL_TYPE_SYSTEM = ExplicitTypeSystem([
    *ARROW_ONLY_TYPE_SYSTEM.rules,

    parse_typing_rule('L⊤', '⊩ L⊤: ο', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L⊥', '⊩ L⊥: ο', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L∧', '⊩ L∧: (ο → (ο → ο))', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L∨', '⊩ L∨: (ο → (ο → ο))', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L→', '⊩ L→: (ο → (ο → ο))', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L↔', '⊩ L↔: (ο → (ο → ο))', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L=', 'M: τ, N: τ ⊩ ((L=M)N): ο', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L∀', 'x: τ, M: ο ⊩ (L∀(λx:τ.M)): ο', PLAIN_HOL_SIGNATURE),
    parse_typing_rule('L∃', 'x: τ, M: ο ⊩ (L∃(λx:τ.M)): ο', PLAIN_HOL_SIGNATURE),
])


def generate_type_system(signature: HolSignature) -> ExplicitTypeSystem:
    return ExplicitTypeSystem([
        *BASE_HOL_TYPE_SYSTEM.rules,
        *(
            TypingRule(
                name='Ax',
                premises=[],
                conclusion=TypingRuleEntry(
                    main=TypeAssertionSchema(Constant(sym), translate_type_to_schema(sym.type)),
                ),
            )
            for sym in signature.iter_nonlogical()
        ),
    ])
