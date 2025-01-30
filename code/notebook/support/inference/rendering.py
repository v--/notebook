from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol, override

from ..iteration import string_accumulator
from ..unicode import to_superscript


SUBTREE_DISTANCE = 4


class InferenceTreeRenderer(Protocol):
    conclusion: str

    def get_base_width(self) -> int:
        ...

    def get_prefix_width(self) -> int:
        ...

    def get_suffix_width(self) -> int:
        ...

    def get_total_width(self) -> int:
        ...

    def get_total_height(self) -> int:
        ...

    def render_line(self, i: int) -> str:
        ...

    def render(self) -> str:
        ...


@dataclass(frozen=True)
class AssumptionRenderer(InferenceTreeRenderer):
    conclusion: str
    marker: str | None = None

    @override
    def get_base_width(self) -> int:
        if self.marker is None:
            return len(self.conclusion) + 2

        return len(self.conclusion) + len(self.marker) + 2

    @override
    def get_prefix_width(self) -> int:
        return 0

    @override
    def get_suffix_width(self) -> int:
        return 0

    @override
    def get_total_width(self) -> int:
        return self.get_base_width()

    @override
    def get_total_height(self) -> int:
        return 1

    @override
    def render_line(self, i: int) -> str:
        assert i == 0

        if self.marker is None:
            return str(self.conclusion)

        return f'[{self.conclusion}]{to_superscript(self.marker)}'

    @override
    def render(self) -> str:
        return self.render_line(0) + '\n'


@dataclass(frozen=True)
class RuleApplicationRenderer(InferenceTreeRenderer):
    conclusion: str
    markers: Sequence[str]
    rule_name: str
    subtrees: Sequence[InferenceTreeRenderer]

    def get_total_subtree_width(self) -> int:
        width = 0

        for j, subtree in enumerate(self.subtrees):
            if j > 0:
                width += SUBTREE_DISTANCE

            width += subtree.get_total_width()

        return width

    def get_subtree_prefix_width(self) -> int:
        if len(self.subtrees) == 0:
            return 0

        return self.subtrees[0].get_prefix_width()

    def get_subtree_suffix_width(self) -> int:
        if len(self.subtrees) == 0:
            return 0

        return self.subtrees[-1].get_suffix_width()

    def get_trimmed_subtree_width(self) -> int:
        return self.get_total_subtree_width() - self.get_subtree_prefix_width() - self.get_subtree_suffix_width()

    @override
    def get_base_width(self) -> int:
        return max(len(self.conclusion), self.get_trimmed_subtree_width())

    def get_marker_prefix_width(self) -> int:
        if len(self.markers) == 0:
            return 0

        width = len(self.markers[0])

        for marker in self.markers[1:]:
            width += len(', ') + len(marker)

        return width

    @override
    def get_prefix_width(self) -> int:
        marker_prefix_width = self.get_marker_prefix_width()
        base_prefix_width = marker_prefix_width + 1 if len(self.markers) > 0 else 0

        return max(
            base_prefix_width,
            self.get_subtree_prefix_width()
        )

    @override
    def get_suffix_width(self) -> int:
        if len(self.subtrees) == 0:
            return 1 + len(self.rule_name)

        return max(
            1 + len(self.rule_name),
            self.get_subtree_suffix_width()
        )

    @override
    def get_total_height(self) -> int:
        if len(self.subtrees) == 0:
            return 2

        return max(subtree.get_total_height() for subtree in self.subtrees) + 2

    @override
    def get_total_width(self) -> int:
        return self.get_prefix_width() + self.get_base_width() + self.get_suffix_width()

    def iter_sublines(self, i: int) -> Iterable[str]:
        total_height = self.get_total_height()
        assert 0 <= i < total_height

        for subtree in self.subtrees:
            subtree_height = subtree.get_total_height()
            offset = total_height - 2 - subtree_height

            if i - offset >= 0:
                yield subtree.render_line(i - offset)
            else:
                yield ''

    @override
    @string_accumulator()
    def render_line(self, i: int) -> Iterable[str]:
        total_height = self.get_total_height()
        assert 0 <= i < total_height

        if i == total_height - 1:
            yield ' ' * (self.get_prefix_width() + (self.get_base_width() - len(self.conclusion)) // 2)
            yield self.conclusion
            return

        if i == total_height - 2:
            yield ', '.join(self.markers)

            if len(self.markers) > 0:
                yield ' '

            yield '_' * self.get_base_width()
            yield ' '
            yield self.rule_name
            return

        yield ' ' * (self.get_prefix_width() - self.get_subtree_prefix_width())

        base_width = self.get_base_width()
        trimmed_subtree_width = self.get_trimmed_subtree_width()

        if trimmed_subtree_width < base_width:
            yield ' ' * ((base_width - trimmed_subtree_width) // 2)

        sublines = list(self.iter_sublines(i))

        for j, (subtree, subline) in enumerate(zip(self.subtrees, sublines, strict=True)):
            yield subline

            if sum(map(len, sublines[j + 1:])) > 0:
                subtree_width = subtree.get_total_width()
                yield ' ' * (SUBTREE_DISTANCE + subtree_width - len(subline))

    @override
    @string_accumulator()
    def render(self) -> Iterable[str]:
        for i in range(self.get_total_height()):
            yield self.render_line(i)
            yield '\n'
