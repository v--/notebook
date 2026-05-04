from notebook.math.lambda_.alphabet import BinaryTypeConnective
from notebook.math.lambda_.hol import common
from notebook.math.lambda_.hol.alphabet import SortName
from notebook.math.lambda_.hol.signature import HolSignature, NonLogicalConstantSymbol, SortSymbol
from notebook.math.lambda_.types import SimpleConnectiveType, SimpleType
from notebook.math.logic.signature import FormalLogicSignature, PredicateSymbol, SignatureSymbol
from notebook.support.coderefs import collector


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
