from notebook.math.lambda_.hol.alphabet import SortName
from notebook.math.lambda_.hol.signature import HolSignature, NonLogicalConstantSymbol, SortSymbol
from notebook.math.lambda_.parsing import parse_type


ARITHMETIC_SIGNATURE = HolSignature(SortSymbol(SortName.INDIVIDUAL))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('0', parse_type('ι', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('S⁺', parse_type('(ι → ι)', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('~', parse_type('(ι → ι)', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('+', parse_type('(ι → (ι → ι))', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('×', parse_type('(ι → (ι → ι))', ARITHMETIC_SIGNATURE)))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('≤', parse_type('(ι → (ι → ο))', ARITHMETIC_SIGNATURE)))
