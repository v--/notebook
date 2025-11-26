from ..signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol


ARITHMETIC_SIGNATURE = FormalLogicSignature(
    FunctionSymbol(name='0', arity=0, infix=False),
    FunctionSymbol(name='S', arity=1, infix=False),
    FunctionSymbol(name='~', arity=1, infix=False),
    FunctionSymbol(name='+', arity=2, infix=True),
    FunctionSymbol(name='×', arity=2, infix=True),
    PredicateSymbol(name='≤', arity=2, infix=True)
)

