from ..signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol


ARITHMETIC_SIGNATURE = FormalLogicSignature(
    FunctionSymbol('0', arity=0),
    FunctionSymbol('S', arity=1, notation='CONDENSED'),
    FunctionSymbol('~', arity=1, notation='CONDENSED'),
    FunctionSymbol('+', arity=2, notation='INFIX'),
    FunctionSymbol('×', arity=2, notation='INFIX'),
    PredicateSymbol('≤', arity=2, notation='INFIX')
)

