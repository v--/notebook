from collections.abc import Iterable
from typing import NamedTuple, Protocol, override

from ..fol.formulas import Formula
from .proof_tree_renderer import AssumptionRenderer, ProofTreeRenderer, RuleApplicationRenderer
from .rules import Rule
from .schemas import FormulaPlaceholder
from .substitution import UniformSubstitution, build_substitution
from .system import NaturalDeductionSystem


class MarkedFormula(NamedTuple):
    formula: Formula
    marker: str


class ProofTree(Protocol):
    system: NaturalDeductionSystem
    conclusion: Formula

    def build_renderer(self) -> ProofTreeRenderer:
        ...

    def iter_open_assumptions(self) -> Iterable[MarkedFormula]:
        ...


class AssumptionTree(ProofTree):
    system: NaturalDeductionSystem
    conclusion: Formula
    marker: str

    def __init__(self, system: NaturalDeductionSystem, assumption: Formula, marker: str) -> None:
        self.system = system
        self.conclusion = assumption
        self.marker = marker

    @override
    def iter_open_assumptions(self) -> Iterable[MarkedFormula]:
        yield MarkedFormula(self.conclusion, self.marker)

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion), self.marker)

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(system: NaturalDeductionSystem, assumption: Formula, marker: str) -> AssumptionTree:
    return AssumptionTree(system, assumption, marker)


class RuleApplicationTree(ProofTree):
    system: NaturalDeductionSystem
    conclusion: Formula
    rule: Rule
    substitution: UniformSubstitution
    subtrees: list[ProofTree]

    def __init__(
        self,
        system: NaturalDeductionSystem,
        rule: Rule,
        substitution: UniformSubstitution,
        subtrees: list[ProofTree]
    ) -> None:
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

    def _iter_assumptions_closed_at_step(self) -> Iterable[MarkedFormula]:
        for premise, subtree in zip(self.rule.premises, self.subtrees):
            if premise.discharge is None:
                continue

            for open_assumption in subtree.iter_open_assumptions():
                if self.substitution.apply_to(premise.discharge) == open_assumption.formula:
                    yield open_assumption

    def get_marker_context(self) -> Iterable[MarkedFormula]:
        return sorted(
            set(self._iter_assumptions_closed_at_step()),
            key=lambda assumption: (str(assumption.formula), assumption.marker)
        )

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            [assumption.marker for assumption in self.get_marker_context()],
            self.rule.name,
            [subtree.build_renderer() for subtree in self.subtrees]
        )

    def __str__(self) -> str:
        return self.build_renderer().render()


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
