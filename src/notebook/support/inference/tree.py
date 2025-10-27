from typing import Protocol, runtime_checkable

from .rendering import InferenceTreeRenderer


@runtime_checkable
class InferenceTree[ConclusionT, AssumptionMapT](Protocol):
    conclusion: ConclusionT

    def get_assumption_map(self) -> AssumptionMapT:
        ...

    def build_renderer(self) -> InferenceTreeRenderer:
        ...
