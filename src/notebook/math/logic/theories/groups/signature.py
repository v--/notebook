from ...signature import FormalLogicSignature, FunctionSymbol


GROUP_SIGNATURE = FormalLogicSignature(
    FunctionSymbol('1', arity=0),
    FunctionSymbol('~', arity=1, notation='CONDENSED'),
    FunctionSymbol('⋅', arity=2, notation='INFIX')
)
