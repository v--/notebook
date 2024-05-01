import abc
import itertools
from collections.abc import Iterable
from typing import NamedTuple, override

from ...support.iteration import string_accumulator
from ...support.unicode import to_superscript
from ..fol.formulas import Formula
from .exceptions import NaturalDeductionError
from .rules import Rule
from .schemas import FormulaPlaceholder
from .substitution import UniformSubstitution, build_substitution
from .system import NaturalDeductionSystem


class MarkedFormula(NamedTuple):
    formula: Formula
    marker: str


class ProofTree(abc.ABC):
    system: NaturalDeductionSystem
    conclusion: Formula

    @abc.abstractmethod
    def iter_open_assumptions(self) -> 'Iterable[MarkedFormula]':
        ...


class AssumptionTree(ProofTree):
    marker: str

    def __init__(self, system: NaturalDeductionSystem, assumption: Formula, marker: str) -> None:
        self.system = system
        self.conclusion = assumption
        self.marker = marker

    @override
    def iter_open_assumptions(self) -> Iterable[MarkedFormula]:
        yield MarkedFormula(self.conclusion, self.marker)

    def __str__(self) -> str:
        return f'[{self.conclusion}]{to_superscript(self.marker)}\n'


def assume(system: NaturalDeductionSystem, assumption: Formula, marker: str) -> AssumptionTree:
    return AssumptionTree(system, assumption, marker)


class RuleApplicationTree(ProofTree):
    rule: Rule
    substitution: UniformSubstitution
    subtrees: list[ProofTree]

    def __init__(self, system: NaturalDeductionSystem, rule: Rule, substitution: UniformSubstitution, subtrees: list[ProofTree]) -> None:
        assert len(rule.premises) == len(subtrees)

        for premise, subtree in zip(rule.premises, subtrees):
            assert substitution.apply_to(premise.main) == subtree.conclusion

        self.system = system
        self.conclusion = substitution.apply_to(rule.conclusion)
        self.rule = rule
        self.substitution = substitution
        self.subtrees = subtrees

    @override
    def iter_open_assumptions(self) -> Iterable[MarkedFormula]:
        for premise, subtree in zip(self.rule.premises, self.subtrees):
            for open_assumption in subtree.iter_open_assumptions():
                if premise.discharge is None or self.substitution.apply_to(premise.discharge) != open_assumption.formula:
                    yield open_assumption

    def iter_assumptions_closed_at_step(self) -> Iterable[MarkedFormula]:
        for premise, subtree in zip(self.rule.premises, self.subtrees):
            if premise.discharge is None:
                continue

            for open_assumption in subtree.iter_open_assumptions():
                if self.substitution.apply_to(premise.discharge) == open_assumption.formula:
                    yield open_assumption

    @string_accumulator()
    def __str__(self) -> Iterable[str]:
        subtree_strings = list(map(str, self.subtrees))
        markers = [ass.marker for ass in set(self.iter_assumptions_closed_at_step())]
        conclusion_str = str(self.conclusion)

        subtree_matrix = list(reversed(list(
            itertools.zip_longest(
                *(reversed(s.splitlines()) for s in subtree_strings),
                fillvalue=''
            )
        )))

        col_widths = [max(map(len, col)) for col in zip(*subtree_matrix)]

        line_length = max(
            sum(col_widths) + (len(col_widths) - 1) * 4,
            len(conclusion_str)
        )

        marker_prefix = (1 + 3 * (len(markers) - 1) + 1) if len(markers) > 0 else 0

        for line in subtree_matrix:
            yield ' ' * marker_prefix

            for j, cell in enumerate(line):
                if j < len(col_widths) - 1 and any(c != '' for c in line[j + 1:]):
                    yield cell.ljust(col_widths[j] + 4, ' ')
                else:
                    yield cell

            yield '\n'

        for i, marker in enumerate(markers):
            if i > 0:
                yield ', '

            yield marker

        if len(markers) > 0:
            yield ' '

        yield '_' * line_length
        yield ' '
        yield self.rule.name
        yield '\n'
        yield ' ' * (marker_prefix + (line_length - len(conclusion_str)) // 2)
        yield conclusion_str
        yield '\n'


def apply(system: NaturalDeductionSystem, rule_name: str, *args: ProofTree, **kwargs: Formula) -> RuleApplicationTree:
    rule = system[rule_name]
    assert len(args) == len(rule.premises)

    substitution = UniformSubstitution({
        FormulaPlaceholder(key): value for key, value in kwargs.items()
    })

    for subtree, premise in zip(args, rule.premises):
        premise_substitution = build_substitution(premise.main, subtree.conclusion)
        assert premise_substitution is not None
        new_substitution = substitution & premise_substitution
        assert new_substitution is not None
        substitution = new_substitution

    return RuleApplicationTree(
        system,
        rule=rule,
        substitution=substitution,
        subtrees=list(args)
    )
