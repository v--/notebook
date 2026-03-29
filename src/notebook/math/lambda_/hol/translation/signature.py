from .....support.coderefs import collector
from ....logic.signature import FormalLogicSignature, PredicateSymbol, SignatureSymbol
from ...alphabet import BinaryTypeConnective
from ...types import BaseType, SimpleConnectiveType, SimpleType
from ..signature import HolSignature, NonLogicalConstantSymbol, common_types


def fol_symbol_to_hol_type(sym: SignatureSymbol) -> SimpleType:
    type_: SimpleType = BaseType(common_types.prop if isinstance(sym, PredicateSymbol) else common_types.individual)

    for _ in range(sym.arity):
        type_ = SimpleConnectiveType(
            BinaryTypeConnective.ARROW,
            BaseType(common_types.individual),
            type_,
        )

    return type_


@collector.ref('alg:fol_signature_to_hol_signature')
def fol_signature_to_hol_signature(fol_signature: FormalLogicSignature) -> HolSignature:
    hol_signature = HolSignature(common_types.individual)

    for sym in fol_signature:
        hol_signature.add_symbol(NonLogicalConstantSymbol(sym.name), fol_symbol_to_hol_type(sym))

    return hol_signature
