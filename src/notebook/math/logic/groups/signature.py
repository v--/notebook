from ..signature import FormalLogicSignature


GROUP_SIGNATURE = FormalLogicSignature()
GROUP_SIGNATURE.add_symbol('FUNCTION', name='ⅇ', arity=0, infix=False)
GROUP_SIGNATURE.add_symbol('FUNCTION', name='~', arity=1, infix=False)
GROUP_SIGNATURE.add_symbol('FUNCTION', name='⋅', arity=2, infix=True)
