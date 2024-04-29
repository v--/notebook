import abc
from collections.abc import Iterable
from dataclasses import dataclass
from typing import NamedTuple, override

import rich.tree

from ...support.rich import RichTreeMixin
from ...support.unicode import to_superscript
from ..fol.formulas import Formula
from .rules import Rule
from .substitutions import UniformSubstitution


@dataclass
class NaturalDeductionSystem:
    rules: frozenset[Rule]


class MarkedFormula(NamedTuple):
    formula: Formula
    marker: str


class ProofTree(abc.ABC, RichTreeMixin):
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

    @override
    def build_rich_tree(self) -> rich.tree.Tree:
        return rich.tree.Tree(f'\\[{self.conclusion}]{to_superscript(self.marker)}')


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

    @override
    def build_rich_tree(self) -> rich.tree.Tree:
        markers = [ass.marker for ass in self.iter_assumptions_closed_at_step()]

        if len(markers) > 0:
            tree = rich.tree.Tree(f'({self.rule.name} closing {", ".join(markers)}) {self.conclusion}')
        else:
            tree = rich.tree.Tree(f'({self.rule.name}) {self.conclusion}')

        for subtree in self.subtrees:
            tree.add(subtree.build_rich_tree())

        return tree
