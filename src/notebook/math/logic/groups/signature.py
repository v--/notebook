from ..signature import FormalLogicSignature, FunctionSymbol


GROUP_SIGNATURE = FormalLogicSignature(
    FunctionSymbol(name='1', arity=0, infix=False),
    FunctionSymbol(name='~', arity=1, infix=False),
    FunctionSymbol(name='⋅', arity=2, infix=True)
)
