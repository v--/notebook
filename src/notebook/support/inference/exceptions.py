from ..exceptions import NotebookSupportError
from .rules import InferenceRule


class UnknownInferenceRuleError(NotebookSupportError):
    def __init__(self, rule: InferenceRule) -> None:
        super().__init__(f'Unrecognized inference rule {str(rule)!r}')
