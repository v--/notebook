from collections.abc import Iterable, Sequence
from typing import Protocol, override

from ....support.inference_tree_renderer import AssumptionRenderer, InferenceTreeRenderer, RuleApplicationRenderer
from ..formulas import Formula
from ..instantiation import SchemaInstantiation, build_instantiation, instantiate_schema
from ..parsing import parse_formula_placeholder, parse_marker
from .markers import MarkedFormula, Marker
from .rules import NaturalDeductionRule
from .system import NaturalDeductionSystem


class ProofTree(Protocol):
    system: NaturalDeductionSystem
    conclusion: Formula

    def build_renderer(self) -> InferenceTreeRenderer:
        ...

    def iter_open_assumptions(self) -> Iterable[MarkedFormula]:
        ...


class AssumptionTree(ProofTree):
    system: NaturalDeductionSystem
    conclusion: Formula
    marker: Marker

    def __init__(self, system: NaturalDeductionSystem, assumption: Formula, marker: Marker) -> None:
        self.system = system
        self.conclusion = assumption
        self.marker = marker

    @override
    def iter_open_assumptions(self) -> Iterable[MarkedFormula]:
        yield MarkedFormula(self.conclusion, self.marker)

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion), str(self.marker))

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(system: NaturalDeductionSystem, assumption: Formula, marker: str) -> AssumptionTree:
    return AssumptionTree(system, assumption, parse_marker(marker))


class RuleApplicationTree(ProofTree):
    system: NaturalDeductionSystem
    conclusion: Formula
    rule: NaturalDeductionRule
    instantiation: SchemaInstantiation
    subtrees: Sequence[ProofTree]

    def __init__(
        self,
        system: NaturalDeductionSystem,
        rule: NaturalDeductionRule,
        instantiation: SchemaInstantiation,
        subtrees: Sequence[ProofTree]
    ) -> None:
        assert len(rule.premises) == len(subtrees)

        for premise, subtree in zip(rule.premises, subtrees, strict=True):
            assert instantiate_schema(premise.main, instantiation) == subtree.conclusion

        self.system = system
        self.conclusion = instantiate_schema(rule.conclusion, instantiation)
        self.rule = rule
        self.instantiation = instantiation
        self.subtrees = subtrees

    @override
    def iter_open_assumptions(self) -> Iterable[MarkedFormula]:
        for premise, subtree in zip(self.rule.premises, self.subtrees, strict=True):
            for open_assumption in subtree.iter_open_assumptions():
                if premise.discharge is None or instantiate_schema(premise.discharge, self.instantiation) != open_assumption.formula:
                    yield open_assumption

    def _iter_assumptions_closed_at_step(self) -> Iterable[MarkedFormula]:
        for premise, subtree in zip(self.rule.premises, self.subtrees, strict=True):
            if premise.discharge is None:
                continue

            for open_assumption in subtree.iter_open_assumptions():
                if instantiate_schema(premise.discharge, self.instantiation) == open_assumption.formula:
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
            [str(assumption.marker) for assumption in self.get_marker_context()],
            self.rule.name,
            [subtree.build_renderer() for subtree in self.subtrees]
        )

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(system: NaturalDeductionSystem, rule_name: str, *args: ProofTree, **kwargs: Formula) -> RuleApplicationTree:
    rule = system[rule_name]
    assert len(args) == len(rule.premises)

    instantiation = SchemaInstantiation({
        parse_formula_placeholder(key): value for key, value in kwargs.items()
    })

    for subtree, premise in zip(args, rule.premises, strict=True):
        premise_substitution = build_instantiation(premise.main, subtree.conclusion)
        assert premise_substitution is not None
        new_substitution = instantiation | premise_substitution
        assert new_substitution is not None
        instantiation = new_substitution

    return RuleApplicationTree(
        system,
        rule=rule,
        instantiation=instantiation,
        subtrees=args
    )
