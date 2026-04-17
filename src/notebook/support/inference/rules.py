from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .alphabet import ImproperInferenceRuleSymbol


if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass(frozen=True)
class InferenceRuleEntry[MainT, AttachmentT = MainT]:
    main: MainT
    attachments: Sequence[AttachmentT] = field(default_factory=list)

    def __str__(self) -> str:
        if len(self.attachments) == 0:
            return str(self.main)

        return ' '.join(f'[{att}]' for att in self.attachments) + ' ' + str(self.main)


@dataclass(frozen=True)
class InferenceRule[ConclusionT, PremiseT = ConclusionT]:
    name: str
    premises: Sequence[PremiseT]
    conclusion: ConclusionT

    def without_name(self) -> str:
        if len(self.premises) > 0:
            premise_str = ', '.join(map(str, self.premises))
            return f'{premise_str} {ImproperInferenceRuleSymbol.SEQUENT} {self.conclusion}'

        return f'{ImproperInferenceRuleSymbol.SEQUENT} {self.conclusion}'

    def __str__(self) -> str:
        return f'({self.name}) {self.without_name()}'

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.premises), self.conclusion))
