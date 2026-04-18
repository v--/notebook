from typing import TYPE_CHECKING

from ..exceptions import NotebookSupportError


if TYPE_CHECKING:
    from .rules import InferenceRule


class InferenceRuleError(NotebookSupportError):
    pass


class UnknownInferenceRuleError(InferenceRuleError):
    def __init__(self, rule: InferenceRule) -> None:
        super().__init__(f'Unrecognized inference rule {str(rule)!r}')
