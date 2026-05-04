# ruff: noqa: E222

from notebook.math.lambda_.terms import Constant
from notebook.math.lambda_.types import BaseType

from .alphabet import LogicalConstantName
from .signature import LogicalConstantSymbol, LogicalTypeSymbol, SortSymbol


prop = BaseType(LogicalTypeSymbol('ο'))
individual = BaseType(SortSymbol('ι'))

verum =         Constant(LogicalConstantSymbol(LogicalConstantName.VERUM))
falsum =        Constant(LogicalConstantSymbol(LogicalConstantName.FALSUM))
negation =      Constant(LogicalConstantSymbol(LogicalConstantName.NEGATION))
conjunction =   Constant(LogicalConstantSymbol(LogicalConstantName.CONJUNCTION))
disjunction =   Constant(LogicalConstantSymbol(LogicalConstantName.DISJUNCTION))
conditional =   Constant(LogicalConstantSymbol(LogicalConstantName.CONDITIONAL))
biconditional = Constant(LogicalConstantSymbol(LogicalConstantName.BICONDITIONAL))
equality =      Constant(LogicalConstantSymbol(LogicalConstantName.EQUALITY))
forall =        Constant(LogicalConstantSymbol(LogicalConstantName.FORALL))
exists =        Constant(LogicalConstantSymbol(LogicalConstantName.EXISTS))
