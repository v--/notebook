from typing import Protocol, runtime_checkable
lazy from collections.abc import Collection

lazy from .rendering import InferenceTreeRenderer


@runtime_checkable
class InferenceTree[ConclusionT, AssumptionT](Protocol):
    conclusion: ConclusionT

    def get_cumulative_assumptions(self) -> Collection[AssumptionT]:
        ...

    def build_renderer(self) -> InferenceTreeRenderer:
        ...
