from ...signature import FormalLogicSignature, FunctionSymbol


GROUP_SIGNATURE = FormalLogicSignature(
    FunctionSymbol('𝕖', arity=0),
    FunctionSymbol('~', arity=1),
    FunctionSymbol('⋅', arity=2),
)
