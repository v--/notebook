from ....parsing import parse_type
from ...alphabet import SortName
from ...signature import HolSignature, NonLogicalConstantSymbol, SortSymbol


ARITHMETIC_SIGNATURE = HolSignature(SortSymbol(SortName.INDIVIDUAL))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('0', parse_type('ι', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('S⁺', parse_type('(ι → ι)', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('~', parse_type('(ι → ι)', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('+', parse_type('(ι → (ι → ι))', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('×', parse_type('(ι → (ι → ι))', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('≤', parse_type('(ι → (ι → ο))', ARITHMETIC_SIGNATURE)))
