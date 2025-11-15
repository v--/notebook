from collections.abc import Collection, Iterable, Mapping
from typing import override

from ....support.substitution import AbstractSubstitution
from ..formulas import Formula, FormulaWithSubstitution, QuantifierFormula
from ..terms import Term, Variable
from ..variables import get_formula_free_variables, get_term_variables, new_variable


class LogicSubstitution(AbstractSubstitution[Variable, Term]):
    variable_mapping: Mapping[Variable, Term]

    def __init__(self, *, variable_mapping: Mapping[Variable, Term] | None = None) -> None:
        self.variable_mapping = variable_mapping or {}

    @override
    def generate_fresh_variable(self, blacklist: Collection[Variable]) -> Variable:
        return new_variable(blacklist)

    @override
    def substitute_variable(self, var: Variable) -> Term:
        return self.variable_mapping.get(var, var)

    def iter_free_in_substituted(self, formula: Formula) -> Iterable[Variable]:
        for var in get_formula_free_variables(formula):
            yield from get_term_variables(self.substitute_variable(var))

    def get_modified_quantifier_variable(self, formula: QuantifierFormula) -> Variable:
        blacklist = set(self.iter_free_in_substituted(formula))

        if formula.var in blacklist:
            return self.generate_fresh_variable(blacklist)

        return formula.var

    @override
    def modify_at(self, var: Variable, replacement: Term) -> LogicSubstitution:
        return LogicSubstitution(variable_mapping={**self.variable_mapping, var: replacement})


def infer_substitution(spec: FormulaWithSubstitution) -> LogicSubstitution:
    if spec.sub:
        return LogicSubstitution(variable_mapping={spec.sub.src: spec.sub.dest})

    return LogicSubstitution()
