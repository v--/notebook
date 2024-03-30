from ..exceptions import NotebookCodeError


class GrammarError(NotebookCodeError):
    pass


class TokenizationError(GrammarError):
    pass


class ParsingError(GrammarError):
    pass
