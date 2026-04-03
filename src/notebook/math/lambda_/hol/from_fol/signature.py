from .....support.coderefs import collector
from ....logic.signature import FormalLogicSignature, PredicateSymbol, SignatureSymbol
from ...alphabet import BinaryTypeConnective
from ...types import SimpleConnectiveType, SimpleType
from .. import common
from ..alphabet import SortName
from ..signature import HolSignature, NonLogicalConstantSymbol, SortSymbol


def fol_symbol_to_hol_type(sym: SignatureSymbol) -> SimpleType:
    type_: SimpleType = common.prop if isinstance(sym, PredicateSymbol) else common.individual

    for _ in range(sym.arity):
        type_ = SimpleConnectiveType(
            BinaryTypeConnective.ARROW,
            common.individual,
            type_,
        )

    return type_


@collector.ref('alg:fol_to_hol/signature')
def fol_signature_to_hol_signature(fol_signature: FormalLogicSignature) -> HolSignature:
    hol_signature = HolSignature(SortSymbol(SortName.INDIVIDUAL))

    for sym in fol_signature:
        hol_signature.add_symbol(
            NonLogicalConstantSymbol(sym.name, fol_symbol_to_hol_type(sym)),
        )

    return hol_signature
