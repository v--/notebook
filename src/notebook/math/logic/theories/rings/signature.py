from ...signature import FormalLogicSignature, FunctionSymbol


RING_SIGNATURE = FormalLogicSignature(
    FunctionSymbol('0', arity=0),
    FunctionSymbol('1', arity=0),
    FunctionSymbol('-', arity=1, notation='CONDENSED'),
    FunctionSymbol('+', arity=2, notation='INFIX'),
    FunctionSymbol('⋅', arity=2, notation='INFIX'),
)
