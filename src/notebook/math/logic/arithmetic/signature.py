from ..signature import FormalLogicSignature


ARITHMETIC_SIGNATURE = FormalLogicSignature()
ARITHMETIC_SIGNATURE.add_symbol('FUNCTION', name='0', arity=0, infix=False)
ARITHMETIC_SIGNATURE.add_symbol('FUNCTION', name='S', arity=1, infix=False)
ARITHMETIC_SIGNATURE.add_symbol('FUNCTION', name='+', arity=2, infix=True)
ARITHMETIC_SIGNATURE.add_symbol('FUNCTION', name='×', arity=2, infix=True)
ARITHMETIC_SIGNATURE.add_symbol('PREDICATE', name='≤', arity=2, infix=True)
