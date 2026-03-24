from .symbol import LogicalConstantSymbol


verum = LogicalConstantSymbol('H⊤')
falsum = LogicalConstantSymbol('H⊥')
negation = LogicalConstantSymbol('H¬')
conjunction = LogicalConstantSymbol('H∧')
disjunction = LogicalConstantSymbol('H∨')
conditional = LogicalConstantSymbol('H→')
biconditional = LogicalConstantSymbol('H↔')
equality = LogicalConstantSymbol('H=')
forall = LogicalConstantSymbol('H∀')
exists = LogicalConstantSymbol('H∃')
