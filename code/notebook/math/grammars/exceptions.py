from ...exceptions import NotebookCodeError


class GrammarError(NotebookCodeError):
    pass


class UnknownSymbolError(GrammarError):
    pass


class TokenizationError(GrammarError):
    pass


class ParserError(GrammarError):
    pass
