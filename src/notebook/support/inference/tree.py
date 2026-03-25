from typing import TYPE_CHECKING, Protocol, runtime_checkable


if TYPE_CHECKING:
    from collections.abc import Collection

    from .rendering import InferenceTreeRenderer


@runtime_checkable
class InferenceTree[ConclusionT, AssumptionT](Protocol):
    conclusion: ConclusionT

    def get_cumulative_assumptions(self) -> Collection[AssumptionT]:
        ...

    def build_renderer(self) -> InferenceTreeRenderer:
        ...
