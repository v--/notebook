from collections.abc import Mapping

from ...alphabet import BinaryConnective, LatticeConnective, PropConstantSymbol
from ...signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol


# The symbols we use here differ from those used in the monograph because Unicode is more restricted than the symbols we can conjure up in (La)TeX
BOOLEAN_ALGEBRA_SIGNATURE = FormalLogicSignature(
    FunctionSymbol('⫪', arity=0),
    FunctionSymbol('⫫', arity=0),
    FunctionSymbol('⫬', arity=1, notation='CONDENSED'),
    FunctionSymbol('⩓', arity=2, notation='INFIX'),
    FunctionSymbol('⩔', arity=2, notation='INFIX'),
    PredicateSymbol('≤', arity=2, notation='INFIX'),
    PredicateSymbol('≥', arity=2, notation='INFIX')
)


FORMULA_CONSTANT_TO_TERM_CONSTANT: Mapping[PropConstantSymbol, FunctionSymbol] = {
    PropConstantSymbol.VERUM: BOOLEAN_ALGEBRA_SIGNATURE.get_function_symbol('⫪'),
    PropConstantSymbol.FALSUM: BOOLEAN_ALGEBRA_SIGNATURE.get_function_symbol('⫫'),
}


TERM_CONSTANT_TO_FORMULA_CONSTANT = {tc: fc for fc, tc in FORMULA_CONSTANT_TO_TERM_CONSTANT.items()}


FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE: Mapping[LatticeConnective, FunctionSymbol] = {
    BinaryConnective.CONJUNCTION: BOOLEAN_ALGEBRA_SIGNATURE.get_function_symbol('⩓'),
    BinaryConnective.DISJUNCTION: BOOLEAN_ALGEBRA_SIGNATURE.get_function_symbol('⩔'),
}


TERM_CONNECTIVE_TO_FORMULA_CONNECTIVE = {tc: fc for fc, tc in FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE.items()}
