from ...exceptions import NotebookCodeError
from .rules import InferenceRule


class UnknownInferenceRuleError(NotebookCodeError):
    def __init__(self, rule: InferenceRule) -> None:
        super().__init__(f'Unrecognized inference rule {str(rule)!r}')
