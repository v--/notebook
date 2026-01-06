from ...signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol


ARITHMETIC_SIGNATURE = FormalLogicSignature(
    FunctionSymbol('0', arity=0),
    FunctionSymbol('S', arity=1),
    FunctionSymbol('~', arity=1),
    FunctionSymbol('+', arity=2),
    FunctionSymbol('×', arity=2),
    PredicateSymbol('≤', arity=2)
)

