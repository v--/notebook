from ..arrow_types import ARROW_ONLY_TYPE_SYSTEM
from ..assertions import TypeAssertionSchema
from ..parsing import parse_typing_rule
from ..terms import Constant
from ..type_system import ExplicitTypeSystem, TypingRule, TypingRuleEntry
from ..types import translate_type_to_schema
from .signature import EMPTY_HOL_SIGNATURE, HolSignature


BASE_HOL_TYPE_SYSTEM = ExplicitTypeSystem([
    *ARROW_ONLY_TYPE_SYSTEM.rules,

    parse_typing_rule('H⊤', '⊩ H⊤: ο', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H⊥', '⊩ H⊥: ο', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H∧', '⊩ H∧: (ο → (ο → ο))', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H∨', '⊩ H∨: (ο → (ο → ο))', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H→', '⊩ H→: (ο → (ο → ο))', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H↔', '⊩ H↔: (ο → (ο → ο))', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H=', 'M: τ, N: τ ⊩ ((H=M)N): ο', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H∀', 'x: τ, M: ο ⊩ (H∀(λx:τ.M)): ο', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H∃', 'x: τ, M: ο ⊩ (H∃(λx:τ.M)): ο', EMPTY_HOL_SIGNATURE),
    parse_typing_rule('H℩', 'x: τ, M: ο ⊩ (H℩(λx:τ.M)): τ', EMPTY_HOL_SIGNATURE),
])


def generate_type_system(signature: HolSignature) -> ExplicitTypeSystem:
    return ExplicitTypeSystem([
        *BASE_HOL_TYPE_SYSTEM.rules,
        *(
            TypingRule(
                name='Ax',
                premises=[],
                conclusion=TypingRuleEntry(
                    main=TypeAssertionSchema(Constant(sym), translate_type_to_schema(signature.get_type(sym)))
                )
            )
            for sym in signature.iter_nonlogical()
        )
    ])
